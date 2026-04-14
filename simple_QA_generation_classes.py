# simple_QA_generation_classes.py
# Generates questions and answers based on OWL Full ontology CLASSES.
# Supports two modes automatically:
#   1. Ontologies with True INDIVIDUALS (e.g. food_basic.owl / wine_3.rdf with named individuals)
#   2. OWL Full PUNNING: classes serve as individuals (e.g. wine ontology in OWL Full)
#
# Usage:
#   python simple_QA_generation_classes.py                  # defaults to food_basic.owl
#   python simple_QA_generation_classes.py wine_3.rdf       # any OWL/RDF ontology

import sys
import os
import re
from itertools import chain
from collections import ChainMap

import owlready2
from owlready2 import *
import rdflib
from rdflib import Graph, RDF, RDFS, OWL, URIRef
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# ─────────────────────────────────────────────
# 0. Command-line argument: path to ontology file
# ─────────────────────────────────────────────

onto_file = sys.argv[1] if len(sys.argv) > 1 else 'food_basic.owl'
onto_uri  = f'file://{onto_file}' if not onto_file.startswith('file://') else onto_file
print(f'Loading ontology: {onto_file}')

# ─────────────────────────────────────────────
# 1. Load ontology
# ─────────────────────────────────────────────

onto  = get_ontology(onto_uri).load()
graph = default_world.as_rdflib_graph()

print(f'Classes ({len(list(onto.classes()))}):', list(onto.classes()))
print(f'Individual count (owlready2): {len(list(onto.individuals()))}')


# ─────────────────────────────────────────────
# 2. Detect mode: TRUE INDIVIDUALS vs OWL Full PUNNING
# ─────────────────────────────────────────────
# OWL Full punning: classes are also used as individuals.
# owlready2 returns 0 individuals OR only class-punned entities.
# Solution: if true individual count is 0, switch to OWL Full mode.

def get_true_individuals(onto):
    """Returns only genuine (non-class) individuals of the ontology."""
    class_iris = {cls.iri for cls in onto.classes()}
    return [
        ind for ind in onto.individuals()
        if not hasattr(ind, 'iri') or ind.iri not in class_iris
    ]

true_individuals = get_true_individuals(onto)
print(f'True individuals (excluding class-individuals): {len(true_individuals)}')

OWL_FULL_MODE = len(true_individuals) == 0
print(f'Mode: {"OWL Full (class-as-individual punning)" if OWL_FULL_MODE else "Standard (true individuals)"}')


# ─────────────────────────────────────────────
# 3. Helper functions (standard mode)
# ─────────────────────────────────────────────

def _sparql_base(onto):
    """
    Returns the IRI prefix that matches how owlready2 stores triples in rdflib.
    For file:// ontologies, owlready2 stores relative IRIs (without 'file://').
    For http:// ontologies, the full IRI is kept — owlready2 adds ## internally for classes.
    """
    iri = onto.base_iri
    if iri.startswith('file://'):
        return iri[len('file://'):]
    return iri

def get_types_hierarchy(x):
    if issubclass(x, Thing):
        return [x, *get_types_hierarchy(x.__bases__[0])]
    return []

def get_relation_pairs(o, depth=1):
    if depth >= 10:
        print('Warning: depth 10 reached, check for cycles')
        return []
    return [
        ('relation', p, get_object_pairs(getattr(o, p._name), depth=depth + 1))
        for p in o.get_properties() if ObjectPropertyClass
    ]

def get_object_pairs(objects, limit_domain=[], depth=1):
    return [
        (
            'entity',
            get_types_hierarchy(type(x)),
            x,
            get_relation_pairs(x, depth)
        )
        for x in objects
        if len(limit_domain) == 0 or any([isinstance(x, y) for y in limit_domain])
    ]

def dict_collapse(e, depth=1):
    has_relationships = len(e[3]) > 0
    if has_relationships:
        return [{f'e{depth}': e[0:3], f'r{depth}': r[0:2], 'n': dictify(r[2], depth + 1)} for r in e[3]]
    else:
        return [{f'e{depth}': e[0:3], f'r{depth}': None, 'n': []}]

def drop_n(d):
    return {k: v for k, v in d.items() if k != 'n'}

def flatten(l):
    return list(chain.from_iterable(l))

def flatten_dicts(dict_list):
    recursed_set = [{**drop_n(e), **n} for e in dict_list for n in e['n']]
    if any(['n' in e for e in recursed_set]):
        recursed_set = flatten_dicts(recursed_set)
    return recursed_set + [drop_n(e) for e in dict_list if len(e['n']) == 0]

def dictify(object_pairs, depth=1):
    if depth >= 10:
        print('Warning: depth 10 reached, check for cycles')
        return []
    collapsed_dicts = flatten([dict_collapse(e, depth) for e in object_pairs])
    return flatten_dicts(collapsed_dicts)

def tablify(object_tuple_dict):
    def generate_entity_dict(k, v):
        if v is None:
            return {}
        elif v[0] == 'entity':
            return {f'{k}_classes': v[1], f'{k}_entity': v[2]}
        else:
            return {f'{k}_relation': v[1]}
    return [dict(ChainMap(*[generate_entity_dict(k, v) for k, v in x.items()])) for x in object_tuple_dict]

def stringify_table(dict_table_format):
    return [
        {k: [x.name for x in v] if isinstance(v, list) else v._name for k, v in x.items()}
        for x in dict_table_format
    ]

print('ok - ontology expansion functions loaded')


# ─────────────────────────────────────────────
# 4a. STANDARD MODE: Build string_df1 via owlready2 individuals
# ─────────────────────────────────────────────

# Schema predicates to exclude in OWL Full mode
_SCHEMA_PREDS = {
    str(RDF.type), str(RDFS.subClassOf), str(OWL.equivalentClass),
    str(OWL.disjointWith), str(OWL.differentFrom), str(OWL.inverseOf),
    str(OWL.sameAs), str(OWL.onProperty), str(OWL.allValuesFrom),
    str(OWL.someValuesFrom), str(OWL.hasValue), str(OWL.intersectionOf),
    str(OWL.unionOf), str(OWL.complementOf), str(OWL.oneOf),
    str(RDFS.range), str(RDFS.domain), str(RDFS.subPropertyOf),
    'http://www.w3.org/2002/07/owl#subPropertyOf',
}

def _local_name(uri_str):
    """Extracts the local name from a URI (after # or last /)."""
    return uri_str.split('##')[-1].split('#')[-1].split('/')[-1]

def build_owl_full_df(onto, graph):
    """
    OWL Full mode: extracts class→relation→class triples directly from the RDF graph.
    Includes only semantic object properties (not schema/OWL-structural predicates).

    Returns a DataFrame with columns:
        e1_classes, r1_relation, e2_classes, e2_entity
    """
    base = onto.base_iri

    # owlready2 stores ## (double hash) for classes in http-based ontologies
    base_variants = [base, base + '#']

    def starts_with_base(uri_str):
        return any(uri_str.startswith(b) for b in base_variants)

    # Build name→class lookup dict for resolving parent class
    class_by_name = {cls.name: cls for cls in onto.classes()}

    def get_superclass_name(entity_name):
        """Returns the most specific parent class of entity according to the hierarchy."""
        cls = class_by_name.get(entity_name)
        if cls is None:
            return entity_name
        # Find the first parent class that exists in the ontology and is not Thing
        for base_cls in cls.__mro__:
            if base_cls is cls:
                continue
            if hasattr(base_cls, 'name') and base_cls.name in class_by_name:
                return base_cls.name
        return entity_name

    rows = []
    for s, p, o in graph:
        s_s, p_s, o_s = str(s), str(p), str(o)
        if not (starts_with_base(s_s) and starts_with_base(o_s)):
            continue
        if p_s in _SCHEMA_PREDS:
            continue
        # Also filter schema predicates by local name
        p_local = _local_name(p_s)
        if p_local in {'disjointWith', 'differentFrom', 'sameAs', 'equivalentClass',
                       'inverseOf', 'subPropertyOf', 'type', 'subClassOf',
                       'range', 'domain', 'onProperty', 'intersectionOf',
                       'allValuesFrom', 'someValuesFrom', 'hasValue',
                       'unionOf', 'complementOf', 'oneOf', 'equivalentProperty'}:
            continue

        s_name = _local_name(s_s)
        o_name = _local_name(o_s)

        # Subject class: most specific parent in the hierarchy
        s_class = get_superclass_name(s_name)

        rows.append({
            'e1_entity':    s_name,
            'e1_classes':   s_class,
            'r1_relation':  p_local,
            'e2_entity':    o_name,
            'e2_classes':   _local_name(o_s),
        })

    if not rows:
        raise ValueError(
            'OWL Full mode: no semantic class→relation→class triples found.\n'
            'Make sure the ontology uses object properties between classes.'
        )

    df = pd.DataFrame(rows).drop_duplicates().reset_index(drop=True)
    return df


# ─────────────────────────────────────────────
# 4. Build relation table depending on detected mode
# ─────────────────────────────────────────────

table_cols = [
    'e1_classes', 'e1_entity', 'r1_relation',
    'e2_classes', 'e2_entity', 'r2_relation',
    'e3_classes', 'e3_entity'
]

if not OWL_FULL_MODE:
    # ── Standard mode ──────────────────────────
    object_pairs      = get_object_pairs(true_individuals, [])
    object_tuple_dict = dictify(object_pairs)
    dict_table_format = tablify(object_tuple_dict)
    string_table      = stringify_table(dict_table_format)

    string_df1 = (
        pd.DataFrame(string_table)
        .reindex(columns=table_cols, fill_value='')
        .fillna('')
        .query("r1_relation != ''")
    )
else:
    # ── OWL Full mode ──────────────────────────
    owl_full_df = build_owl_full_df(onto, graph)
    # Build string_df1 in a compatible format
    string_df1 = owl_full_df.reindex(columns=table_cols, fill_value='').fillna('')
    string_df1 = string_df1[string_df1['r1_relation'] != ''].reset_index(drop=True)

print(f'string_df1: {len(string_df1)} rows')
print(string_df1.head(10).to_string())


# ─────────────────────────────────────────────
# 5. Build the 'exp' table based on CLASSES
#    Use only the leaf (most specific) class,
#    not the full hierarchy [Vegetable, Food, Thing].
# ─────────────────────────────────────────────

string_df1['e1_class_leaf'] = string_df1['e1_classes'].apply(
    lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x
)

exp = (
    string_df1
    .assign(e1_classes=string_df1['e1_class_leaf'])
    .drop(columns=['e1_entity', 'e1_class_leaf'])
    .drop_duplicates(subset=['e1_classes', 'r1_relation', 'e2_entity'])
    .reset_index(drop=True)
)

print(f'\nClass-based table: {len(exp)} rows')
print(exp.head(10).to_string())


# ─────────────────────────────────────────────
# 6. Generate questions
# ─────────────────────────────────────────────

questions = 'What ' + exp.e1_classes.str.cat(
    sep=' ',
    others=[exp.r1_relation, exp.e2_entity]
)

print(f'\n{len(questions)} questions generated')
print(questions[:10].to_string())


# ─────────────────────────────────────────────
# 7. Generate answers via SPARQL / RDF graph
#    Automatically selects the strategy based on the detected mode.
# ─────────────────────────────────────────────

def query_ontology_standard(class_name, relation_name, entity_name):
    """
    Standard mode: finds true individuals via rdfs:subClassOf* filter.
    owlready2 stores relative file:// IRIs without the 'file://' prefix.
    """
    base = _sparql_base(onto)
    query = (
        f'PREFIX onto: <{base}> '
        'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> '
        'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
        'SELECT ?s WHERE { '
        f'  ?s rdf:type ?type . '
        f'  ?type rdfs:subClassOf* onto:{class_name} . '
        f'  ?s onto:{relation_name} onto:{entity_name} . '
        '  FILTER NOT EXISTS { ?s rdfs:subClassOf ?x . } '
        '}'
    )
    return list(graph.query_owlready(query))


def _entity_uri(name):
    """
    Builds the URI for an entity/class in wine-style ontologies.
    owlready2 stores classes/entities with double ## for http-based ontologies.
    Example: http://...wine##BancroftChardonnay
    """
    base = onto.base_iri
    if base.startswith('file://'):
        return URIRef(base.replace('file://', '') + name)
    return URIRef(base + '#' + name)   # single # + extra # = ##


def _prop_uri(name):
    """
    Builds the URI for an object property in wine-style ontologies.
    owlready2 stores object properties with a single # for http-based ontologies.
    Example: http://...wine#locatedIn
    """
    base = onto.base_iri
    if base.startswith('file://'):
        return URIRef(base.replace('file://', '') + name)
    return URIRef(base + name)   # base already ends with #


def query_ontology_owl_full(class_name, relation_name, entity_name):
    """
    OWL Full mode: finds subjects directly in the rdflib graph.
    Properties have single-# IRIs; entities have double-## IRIs.
    """
    class_uri  = _entity_uri(class_name)
    rel_uri    = _prop_uri(relation_name)
    entity_uri = _entity_uri(entity_name)

    results = []
    for s, _, o in graph.triples((None, rel_uri, entity_uri)):
        if _is_subclass_of(s, class_uri):
            results.append(s)
    return results


def _is_subclass_of(entity_uri, class_uri):
    """Recursively checks whether entity is a subclass of class (including itself)."""
    if entity_uri == class_uri:
        return True
    for _, _, superclass in graph.triples((entity_uri, RDFS.subClassOf, None)):
        if not isinstance(superclass, rdflib.BNode):
            if _is_subclass_of(superclass, class_uri):
                return True
    return False


def query_ontology(class_name, relation_name, entity_name):
    """Unified entry point: selects the correct strategy automatically."""
    if OWL_FULL_MODE:
        return query_ontology_owl_full(class_name, relation_name, entity_name)
    return query_ontology_standard(class_name, relation_name, entity_name)


def get_ontology_answer(class_name, relation_name, entity_name, not_modifier=False):
    if not_modifier:
        if OWL_FULL_MODE:
            class_uri  = _entity_uri(class_name)
            rel_uri    = _prop_uri(relation_name)
            entity_uri = _entity_uri(entity_name)
            # All subclasses of class_name that do NOT have rel → entity
            results = []
            for cls in onto.classes():
                cls_uri = _entity_uri(cls.name)
                if _is_subclass_of(cls_uri, class_uri):
                    has_rel = any(True for _ in graph.triples((cls_uri, rel_uri, entity_uri)))
                    if not has_rel:
                        results.append(cls_uri)
            return results
        else:
            base = _sparql_base(onto)
            query = (
                f'PREFIX onto: <{base}> '
                'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> '
                'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
                'SELECT ?s WHERE { '
                f'  ?s rdf:type ?type . '
                f'  ?type rdfs:subClassOf* onto:{class_name} . '
                f'  FILTER NOT EXISTS {{ ?s onto:{relation_name} onto:{entity_name} . }} '
                '  FILTER NOT EXISTS { ?s rdfs:subClassOf ?x . } '
                '}'
            )
            return list(graph.query_owlready(query))
    else:
        return query_ontology(class_name, relation_name, entity_name)


def format_answer(result_list):
    """Converts OWL query results into a readable list of entity names."""
    names = []
    for item in result_list:
        obj = item[0] if isinstance(item, (list, tuple)) else item
        if hasattr(obj, 'name'):
            names.append(obj.name)
        else:
            names.append(_local_name(str(obj)))
    return names if names else []


# Generate answers
print('\nGenerating answers...')
a1 = exp.apply(
    lambda row: query_ontology(row.e1_classes, row.r1_relation, row.e2_entity),
    axis=1
)
answers_formatted = a1.apply(format_answer)


# ─────────────────────────────────────────────
# 8. Save results
# ─────────────────────────────────────────────

qa_df = pd.DataFrame({
    'question': questions.reset_index(drop=True),
    'answer':   answers_formatted.reset_index(drop=True)
})

base_path = os.getcwd()
onto_stem = os.path.splitext(os.path.basename(onto_file))[0]   # e.g. "wine_3" or "food_basic"

qa_df.to_csv(os.path.join(base_path, f'qa_dataset_{onto_stem}.csv'), index=False)
questions.to_csv(os.path.join(base_path, f'questions_{onto_stem}.txt'), index=False, header=False)
answers_formatted.apply(
    lambda x: ', '.join(x) if isinstance(x, list) else str(x)
).to_csv(os.path.join(base_path, f'answers_{onto_stem}.txt'), index=False, header=False)

print(f'\nSaved {len(qa_df)} question-answer pairs')
print(f'Files: qa_dataset_{onto_stem}.csv, questions_{onto_stem}.txt, answers_{onto_stem}.txt')
print('\nFirst 10 pairs:')
for _, row in qa_df.head(10).iterrows():
    print(f"  Q: {row['question']}")
    print(f"  A: {row['answer']}")
    print()
