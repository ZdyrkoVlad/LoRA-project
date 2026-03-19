#!/usr/bin/env python
# coding: utf-8

# In[13]:


# JY, - Import dictionaries
# Import OWLReady
import owlready2
from owlready2 import *
from itertools import chain
import rdflib
#import sparql
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
graph = default_world.as_rdflib_graph()

# Import Pandas, Numpy
import pandas as pd
from pprint import pprint
import numpy as np
import re
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


print('ok - import dictionaries')


# In[15]:


import owlready2
from owlready2 import *
from itertools import chain
import rdflib
#import sparql
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import FOAF, XSD
graph = default_world.as_rdflib_graph()

onto = get_ontology("http://test.org/onto.owl")

with onto:
     
    class Food(Thing):
        pass
    class Vegetable(Food):
        pass
    class Fruit(Food):
        pass
    class Meat(Food):
        pass  
    class Fish(Food):
        pass
    class Grain(Food):
        pass
    class Dairy(Food):
        pass    
    
    class Tool(Thing):
        pass
    class Kitchenware(Tool):
        pass
    class Tableware(Tool):
        pass

    
    class Taste(Thing):
        pass
    class Country(Thing):
        pass
    class Color(Thing):
        pass   
    class Nutrition(Thing):
        pass  
    class Function(Thing):
        pass 
    class Shape(Thing):
        pass 
    
     
    class original_from(ObjectProperty):
        domain    = [Food]
        range     = [Country]
    class has_taste(ObjectProperty):
        domain    = [Food]
        range     = [Taste]
    class has_child_food(ObjectProperty):
        domain = [Food]
        range  = [Food]
    class has_color(ObjectProperty):
        domain    = [Food]
        range     = [Color]    
    class has_nutrition(ObjectProperty):
        domain    = [Food]
        range     = [Nutrition] 
        
    class has_function(ObjectProperty):
        domain    = [Tool]
        range     = [Function] 
    class has_shape(ObjectProperty):
        domain    = [Tool]
        range     = [Shape] 
    class has_sub_function(ObjectProperty):
        domain = [Tool]
        range  = [Tool]
        
           
        
    juicy = Taste('juicy')
    sweet = Taste('sweet')
    sour = Taste('sour')
    bitter = Taste('bitter')
    salty = Taste('salty')
    spicy = Taste('spicy')
    fruity = Taste('fruity')
    grassy = Taste('grassy')
    woody = Taste('woody')
    pungent = Taste('pungent')
    meaty = Taste('meaty')
    fishy = Taste('fishy')
    tangy = Taste('tangy')
    
    
    australia = Country('australia')
    new_zealand = Country('new_zealand')
    china = Country('china')
    canada = Country('canada')
    mexica = Country('mexica')
    america = Country('america')
    europe = Country('europe')
    asia = Country('asia')
    egypt = Country('egypt')
    india = Country('india')
    
    green = Color('green')
    red = Color('red')
    yellow = Color('yellow')
    white = Color('white')
    purple = Color('purple')
    
    protein = Nutrition('protein')
    fat = Nutrition('fat')
    
    fry = Function('fry')
    boil = Function('boil')
    drinking = Function('drinking')
    poking = Function('poking')
    stabbing = Function('stabbing')
    cutting = Function('cutting')
    servefood = Function('servefood')
    
    
    long = Shape('long')
    round = Shape('round')
    circular = Shape('circular')
    solid = Shape('solid')
    liquid = Shape('liquid')
    

    tomato = Vegetable("tomato", has_shape=[round], has_color=[red], has_taste=[juicy, sweet], original_from=[america])
    broccoli = Vegetable("broccoli", has_color=[green], has_taste=[juicy, sweet])
    bean = Vegetable("bean", has_color=[green], original_from=[australia, new_zealand]) 
    chilli = Vegetable("chilli", has_taste=[spicy], has_color=[green, red, yellow], original_from=[america])
    carrot = Vegetable("carrot", has_shape=[long], has_color=[yellow], has_taste=[woody])
    capsicum = Vegetable("capsicum", has_taste=[spicy], has_color=[green, red, yellow], original_from=[america])
    cucumber = Vegetable("cucumber", has_shape=[long], has_color=[green], has_taste=[juicy], original_from=[india])
    squash = Vegetable("squash", has_shape=[long], has_color=[green])
    cabbage = Vegetable("cabbage", has_taste=[sweet])
    ginger = Vegetable("ginger", has_taste=[pungent], original_from=[asia])
    garlic = Vegetable("garlic", has_color=[white], has_taste=[pungent], original_from=[asia])
    leek = Vegetable("leek", has_taste=[pungent], original_from=[australia, new_zealand])
    lettuce = Vegetable("lettuce", has_shape=[round], has_color=[green], original_from=[egypt])
    mushroom = Vegetable("mushroom", has_color=[white])
    onion = Vegetable("onion", has_shape=[round], has_color=[yellow, purple], has_taste=[pungent], original_from=[australia, new_zealand])
    potato = Vegetable("potato", has_taste=[sweet], original_from=[america])
    pumpkin = Vegetable("pumpkin", has_taste=[sweet],has_color=[yellow], original_from=[mexica])
    parsley = Vegetable("parsley", has_color=[green], original_from=[mexica])
    green_onion = Vegetable("green_onion", has_shape=[long], has_color=[white, green], has_taste=[pungent], original_from=[australia, new_zealand]) 
    eggplant= Vegetable("eggplant", has_shape=[long], has_color=[purple], has_taste=[sweet] )
    asparagus= Vegetable("asparagus", has_shape=[long], has_color=[green], has_taste=[sweet])
    pepper = Vegetable("pepper", has_color=[green, red, yellow], has_taste=[spicy])
    
    
    orange = Fruit("orange", has_color=[yellow], has_for_taste=[sweet, sour, juicy])
    apple = Fruit("apple", has_color=[green, red], has_for_taste=[sweet], original_from=[america])
    banana = Fruit("banana", has_shape=[long], has_color=[yellow], has_for_taste=[sweet])
    lemon = Fruit("lemon", has_color=[yellow], has_taste=[sweet, sour, juicy], original_from=[china])
    plum = Fruit("plum", has_color=[purple], has_taste=[sweet, sour, juicy], original_from=[china])
    lime = Fruit("lime", has_color=[green], has_taste=[sweet, sour, juicy], original_from=[china])

    
    melon = Fruit("melon", has_taste=[sweet])
    kiwifruit = Fruit("kiwifruit", has_shape=[round], has_color=[green], original_from=[new_zealand])
    strawberry = Fruit("strawberry", has_color=[red], has_taste=[sweet])
    raspberry = Fruit("raspberry", has_color=[red], has_taste=[sweet])
    pineapple = Fruit("pineapple", has_color=[yellow], has_taste=[sweet])
    mandarin = Fruit("mandarin", has_color=[yellow], has_taste=[sweet, juicy])
    avocado = Fruit("avocado", has_shape=[round], has_color=[green], has_taste=[grassy], original_from=[america])
    watermelon = Fruit("watermelon", has_color=[green, red], has_taste=[sweet, juicy])
    grape = Fruit("grape", has_color=[green, red], has_taste=[juicy, sweet])
    cherry = Fruit("cherry", has_color=[red], has_taste=[sweet])
    pear = Fruit("pear", has_shape=[round], has_color=[green, yellow], has_taste=[juicy, sweet])
   

    green_apple = Fruit("green_apple", has_color=[green], has_taste=[sweet], original_from=[america])
    red_apple = Fruit("red_apple", has_color=[red], has_taste=[sweet], original_from=[america])

    apple = Fruit("apple", has_child_food=[red_apple])
    apple = Fruit("apple", has_child_food=[green_apple])
    
    beaf = Meat("beaf", has_taste=[meaty], has_color=[red])
    chicken = Meat("chicken", has_taste=[meaty], has_color=[white])
    lamb = Meat("lamb", has_taste=[meaty], has_color=[red])
    pork = Meat("pork", has_taste=[meaty], has_color=[red])
    
    salmon = Fish("salmon", has_taste=[fishy], has_nutrition=[fat, protein])
    shrimp = Fish("shrimp", has_taste=[fishy], has_nutrition=[protein])
    squid = Fish("squid", has_taste=[fishy], has_nutrition=[protein])
    fillet = Fish("fillet", has_taste=[fishy], has_nutrition=[fat, protein])
    
    egg = Dairy("egg", has_nutrition=[protein])
    yoghurt = Dairy("yoghurt", has_taste=[sweet], has_nutrition=[protein])
    cheese = Dairy("cheese", has_nutrition=[protein, fat])
    milk = Dairy("milk", has_nutrition=[protein, fat], has_taste = [sweet])
    
    rice = Grain("rice", has_shape=[round, long])
    noodle = Grain("noodle", has_shape=[long])
    pasta = Grain("pasta", has_shape=[round, long])
    bread = Grain("bread", has_shape=[long], has_taste=[tangy])
    corn = Grain("corn", has_color=[yellow], original_from=[america])
    
    
    pan = Kitchenware('pan', has_function=[fry], has_color=[red])   
    pot = Kitchenware('pot', has_function=[boil], has_color=[red])  
    chopping_board = Kitchenware('chopping_board', has_function=[cutting])  

    spoon = Tableware('spoon', has_function=[drinking])
    fork = Tableware('fork', has_function=[poking, stabbing])
    knife = Tableware('knife', has_function=[cutting])
    plate = Tableware('plate', has_function=[servefood], has_shape=[circular])

    plate = Tableware('plate', has_function=[servefood], has_shape=[circular], has_sub_function=[chopping_board])

  
    print('ok-onto1')


# In[19]:


print(list(onto.individuals()))


# In[25]:


# JY, - First part - Unroll ontology 
# --- First method set, recursive methods to turn objects and relations into some sort of consistent format ---
# --- Output: list of tuples to represent the entity and all its relationships including a depth tracker ---

# recursive method to get class hierarchy
def get_types_hierarchy(x):
    if issubclass(x, Thing):
        # to filter out Thing's, uncomment below
        # if x is not Thing:
        return [x, *get_types_hierarchy(x.__bases__[0])]
    return []

# gets a tuple representing a relationship (recursive with get_object_pairs)
def get_relation_pairs(o, depth=1):
    if depth>=10:
        print('Warning, depth of 10 hit, check for cycles')
        return []
    return [('relation', p, get_object_pairs(getattr(o, p._name), depth=depth+1)) 
    for p in o.get_properties() if ObjectPropertyClass]

# gets a tuple representing a pair of objects (recursive with get_relation_pairs), [0, 1, 2, 3] = [entity, types, x, relation_pairs]
def get_object_pairs(objects, limit_domain=[], depth=1):
    return [(
        'entity',
        get_types_hierarchy(type(x)),
        x,
        get_relation_pairs(x, depth))
        for x in objects 
        if len(limit_domain)==0 or any([isinstance(x, y) for y in limit_domain])]


# --- JY - Get ready to build a table from unrolled ontology. 
# --- Second method set, recursive method sets to unroll the hierarchy, ---
# --- Output: collapsed list of dicts with each level of entity/relationship numbered as e1/r1, e2/r2 etc. ---

# works with dictify to flatten out the hierarchy to a one-dict per entity/relationship combination including recurse
def dict_collapse(e, depth=1):
    has_relationships = len(e[3])>0
    if has_relationships:
        return [{f'e{depth}': e[0:3], f'r{depth}': r[0:2], 'n': dictify(r[2], depth+1)} for r in e[3]]
    else:
        return [{f'e{depth}': e[0:3], f'r{depth}': None, 'n': []}]

# removes the "n" column which is used to indicate another level of recursion
def drop_n(d):
    return {k:v for k,v in d.items() if k!='n'}

# helper to flatten nested lists, put two sublists into a combined list. 
def flatten(l):
    return list(chain.from_iterable(l))

# Removes a single level of recursion then calls itself again
def flatten_dicts(dict_list):
    # handle case of no next level and case of having a next level then recurse
    recursed_set = [{**drop_n(e), **n} for e in dict_list for n in e['n']]
    if any(['n' in e for e in recursed_set]):
        recursed_set = flatten_dicts(recursed_set)
    return recursed_set + \
        [drop_n(e) for e in dict_list if len(e['n'])==0]

# controller method to orchestrate the other 2
def dictify(object_pairs, depth=1):
    if depth >= 10:
        print('Warning, depth of 10 hit, check for cycles')
        return []
    collapsed_dicts = flatten([dict_collapse(e, depth) for e in object_pairs])
    return flatten_dicts(collapsed_dicts)

# --- JY Build the table 
# --- Third method set, no more recursion, these methods are just helpful to coerce to a table-like format, could easily write your own methods instead :) ---
# --- Output: dictionary with an entity or list of classes per column making it easier to filter and work with ---

# convert the whole ontology to a table format
from collections import ChainMap
def tablify(object_tuple_dict):
    def generate_entity_dict(k, v):
        if v is None:
            return {}
        elif v[0]=='entity':
            return {f'{k}_classes': v[1], f'{k}_entity': v[2]}
        else:
            return {f'{k}_relation': v[1]}
        
    return [dict(ChainMap(*[generate_entity_dict(k,v) for k,v in x.items()])) for x in object_tuple_dict]

# convert all the entities and classes to strings for easy sentence generation
def stringify_table(dict_table_format):
    return [{k: [x.name for x in v] if isinstance(v, list) else v._name for k,v in x.items()} for x in dict_table_format]

print('ok-Unroll Ontology Functions')
# --- Actually using the above methods! ---


# In[27]:


# these 2 do the main bulk of the work, you could happily write a function to process object_tuple_dict directly
object_pairs = get_object_pairs(onto.individuals(), [onto.Food])
object_tuple_dict = dictify(object_pairs)

# or use these to get a table sort of format that we can do further processing on to generate questions!
dict_table_format = tablify(object_tuple_dict)
string_table = stringify_table(dict_table_format)

table_cols_threelevels = ['e1_classes', 'e1_entity', 'r1_relation', 'e2_classes', 'e2_entity', 'r2_relation', 'e3_classes', 'e3_entity']

string_df = pd.DataFrame(string_table)[table_cols_threelevels]
print('Table: string_df, Onto: Food')
string_df[0:10]


# In[30]:


# these 2 do the main bulk of the work, you could happily write a function to process object_tuple_dict directly
object_pairs = get_object_pairs(onto.individuals(), [onto.Food])
object_tuple_dict = dictify(object_pairs)

# or use these to get a table sort of format that we can do further processing on to generate questions!
dict_table_format = tablify(object_tuple_dict)
string_table = stringify_table(dict_table_format)

# can make an entity df with the individuals/classes if you want to access properties and inspect them, etc.
# entity_df = pd.DataFrame(dict_table_format)
# entity_df.explode('e2_classes').explode('e1_classes')
table_cols_threelevels = ['e1_classes', 'e1_entity', 'r1_relation', 'e2_classes', 'e2_entity', 'r2_relation', 'e3_classes', 'e3_entity']

# or can make a string df use the "string_table" for sentence generation purposes
string_df1 = pd.DataFrame(string_table)[table_cols_threelevels].fillna('').query("r1_relation!=''")
print('print ok-Table0: string_df1. fillna ''and r1_relation is not null')
string_df1


# In[127]:


# Print some test questions

exp = string_df1.explode('e2_classes').explode('e1_classes').drop(columns=['e1_entity']).drop_duplicates(subset=[
        'e1_classes',
        'r1_relation',
        'e2_classes',
        'e2_entity'
    ]).reset_index(drop=True)

exp


# In[109]:


# Generate some test questions with
questions = 'What ' + exp.e1_classes.str.cat(
    sep=' ',
    others=[
        exp.r1_relation,
        exp.e2_entity
    ]
)

pprint(f'{len(questions)} questions in total')
pprint(questions)


# In[125]:


exp.head()


# In[121]:


# Generate Answers Code
# class_name    # relation_name     # entity_name
# Food        has_child_food      orange
# graph = default_world.as_rdflib_graph()


def query_ontology(class_name, relation_name, entity_name):

    query = "PREFIX onto: <" + onto.base_iri + """> SELECT ?s
    WHERE {""" + f"""
        ?s onto:{relation_name} onto:{entity_name} .
    """ + '}'
    r1 = list(graph.query_owlready(query))
    return r1

def get_ontology_answer(class_name, relation_name, entity_name, not_modifier=False):
    if not_modifier:
        query = "PREFIX onto: <" + onto.base_iri + """> SELECT ?s 
        WHERE {
            ?s rdf:type ?type. ?type rdfs:subClassOf+ onto:Food . 
            FILTER NOT EXISTS { """  + f""" ?s onto:{relation_name} onto:{entity_name} . """ + \
            """} FILTER NOT EXISTS {?s rdfs:subClassOf ?t . } }""" 
        r2 = list(graph.query_owlready(query)) 
        return r2 
    else:
        results:list = query_ontology(class_name, relation_name, entity_name)
        return results


# def compute_logical_relation(a1, a1_operator, a2, a2_operator):
#     result = []

#     # a1,a2,a3 = [set() if a == 'not_answer' else set(a) for a in [a1,a2,a3]]
#     # a1, a2, a3 = set(a1), set(a2), set(a3)
#     a1, a2  = set(a1), set(a2)
#     if a1_operator == 'and':
#         result1 = a1.intersection(a2)
#     else:
#         result1 = a1.union(a2)

#     return result

# The below code is to add a null into the table. 
#     if len(result) == 0:
#         return np.nan
#     return list(result)


# 	e1_classes	r1_relation	e2_classes	e2_entity	r2_relation	e3_classes	e3_entity
# 0	Vegetable	has_color	Color	red	

from itertools import chain
#a1 = c3e.apply(lambda row: get_ontology_answer(row.e1_classes, row.r1_relation_x, row.e2_entity_x, row.not_x), axis=1)
a1 = exp.apply(lambda row: get_ontology_answer(row.e1_classes, row.r1_relation, row.e2_entity), axis=1)
# filter_function = lambda item: item if isinstance(item, str) else [str(it) for it in item[0]]
# flatten1  = [filter_function(val) for val in a1]
# print(flatten1)

# qadb1['a1'] = flatten1



# a2 = qadb1.apply(lambda row: get_ontology_answer(row.e1_classes, row.r1_relation_y, row.e2_entity_y, row.not_y), axis=1)
# filter_function = lambda item: item if isinstance(item, str) else [str(it) for it in item[0]]
# flatten2  = [filter_function(val) for val in a2] 
# qadb1['a2'] = flatten2


# a3 = qadb1.apply(lambda row: get_ontology_answer(row.e1_classes, row.r1_relation, row.e2_entity), axis=1)
# filter_function = lambda item: item if isinstance(item, str) else [str(it) for it in item[0]]
# flatten3  = [filter_function(val) for val in a3] 
# qadb1['a3'] = flatten3

#c3e['fa'] = c3e.apply(lambda row: compute_logical_relation(row.a1, row.combine_x,  row.a2, row.combine_y, row.a3), axis=1)
# ?qadb1['fa'] = qadb1.apply(lambda row: compute_logical_relation(row.a1, row.combine_x,  row.a2, row.combine_y, row.a3), axis=1)

print('Answer:')
# c3e.head(500)
# qadb1.head(50)


# In[ ]:





# In[139]:


print(a1[0])
exp.iloc[[0]]


# In[146]:


if len(exp) == len(questions): 
    print('Yar')


# In[171]:


answers = pd.Series(a1)
base_path = os.getcwd()


# In[175]:


questions.to_csv(os.path.join(base_path, 'questions.txt'), index=False, header=False)
answers.to_csv(os.path.join(base_path, 'answers.txt'), index=False, header=False)
qa_df = pd.DataFrame({
    'question': questions,
    'answer': answers
})
qa_df.to_csv(os.path.join(base_path, 'qa_dataset.csv'), index=False)


# In[ ]:




