# LoRA Project — OWL Ontology QA Generation

## Convert notebook to Python script

```bash
jupyter nbconvert --to script simple_QA_generation.ipynb
```

## Convert .py to ipynb
pip install p2j
```bash
p2j myscript.py
```

---

## `simple_QA_generation_classes.py`

Generates question-answer pairs from OWL ontologies.  
Automatically detects two modes:

| Mode | Description |
|------|-------------|
| **Standard** | Ontology has true named individuals (e.g. `food_basic.owl`) |
| **OWL Full** | Classes act as individuals via punning (e.g. `wine_3.rdf`) |

### Usage

```bash
# Default — loads food_basic.owl
python simple_QA_generation_classes.py

# Load any OWL/RDF ontology by passing the filename as an argument
python simple_QA_generation_classes.py food_basic.owl
python simple_QA_generation_classes.py wine_3.rdf
python simple_QA_generation_classes.py my_ontology.owl



#Generate complex question and answer max 4 logic combination

python complex_logic_QA_generation_classes.py food_basic.owl 1000 4
```

### Output files

Output files are named after the ontology (without extension) and saved in the current working directory:

| File | Description |
|------|-------------|
| `qa_dataset_<name>.csv` | Full Q&A dataset with `question` and `answer` columns |
| `questions_<name>.txt` | One question per line |
| `answers_<name>.txt` | One answer per line (comma-separated if multiple) |

**Examples:**

| Ontology argument | Output files |
|---|---|
| `food_basic.owl` | `qa_dataset_food_basic.csv`, `questions_food_basic.txt`, `answers_food_basic.txt` |
| `wine_3.rdf` | `qa_dataset_wine_3.csv`, `questions_wine_3.txt`, `answers_wine_3.txt` |

### Requirements

```bash
pip install owlready2 pandas rdflib SPARQLWrapper numpy
```

---

## Legacy script output

```bash
python simple_QA_generation.py
```

Output: `qa_dataset.csv`

---

## `LLM_integration.py`

Connects to a local LLM (e.g., via LM Studio or Ollama using an OpenAI-compatible API) to convert raw, logical questions into natural language.

### Features:
- **Inputs:** Accepts either a `.txt` file (one question per line) or a `.csv` file (must contain a `question` column).
- **Processing:** Prompts the local LLM to rewrite logical strings (e.g. `What Vegetable has_taste woody`) into normal human-readable English.
- **Outputs:** If a `.csv` is provided, it safely replaces ONLY the `question` column with the LLM's output and saves a new copy of the dataset.

### Usage

Run the script by passing the target file as an argument:

```bash
# Process a CSV file
python LLM_integration.py qa_dataset_food_basic.csv

# Process a TXT file
python LLM_integration.py questions_food_basic.txt
```

**Outputs:**
When you pass a CSV, a new file will be automatically generated with the `_LLM_processed` suffix:
`qa_dataset_food_basic_LLM_processed.csv`
