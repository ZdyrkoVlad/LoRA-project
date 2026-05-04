# %% [markdown]
# # Environment Setup and Basic LLM Test
# First, we import the necessary libraries and set up the client for the local LLM.
# 
# **Requirements:**
# `pip install openai pydantic`

# %%
import os
import sys
import csv
from openai import OpenAI

# If using Ollama, the default port is usually 11434. 
# If using LM Studio, change the port to 1234.
LOCAL_API_URL = "http://localhost:1234/v1" 
API_KEY = "no-api-key" # Local server doesn't validate this key

# Initialize the OpenAI client pointing to our local server
client = OpenAI(
    base_url=LOCAL_API_URL,
    api_key=API_KEY
)

# Specify the model name you have loaded in Ollama (e.g., "llama3", "mistral", or "phi3").
# If using LM Studio, the model name can often be left as "local-model".
MODEL_NAME = "gemma-4-e4b-it-mlx" 

# %% [markdown]
# ## Connection Check
# Let's verify that the local server is running and the model is available.

# %%
def check_model_connection():
    """
    Verifies if the local LLM server is accessible and prints the connection status.
    """
    try:
        models = client.models.list()
        model_ids = [m.id for m in models.data]
        print(f"✅ Successfully connected to local server at {LOCAL_API_URL}")
        print(f"📦 Available models: {model_ids}")
        
        if len(model_ids) > 0:
            print(f"🚀 Ready to use! (Target model: {MODEL_NAME})")
            return True
        else:
            print("⚠️ Server is reachable, but no models seem to be loaded.")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to the local server. Error: {e}")
        return False

# Run the connection check
is_connected = check_model_connection()
print("-" * 40)

# %% [markdown]
# ## Test Request for Question Generation
# Let's write a prompt to have the LLM generate a few questions in our specific format.

# %%
def get_examples_from_file(filepath: str, num_examples: int = 5) -> str:
    """
    Reads a few examples from the provided text file to use in the prompt.
    """
    examples = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= num_examples:
                    break
                if line.strip():
                    examples.append(line.strip())
        return "\n".join(examples)
    except FileNotFoundError:
        return "What Vegetable original_from america\nWhat Fruit has_taste sweet"

def generate_natural_questions_from_file(filepath: str) -> str:
    """
    Reads logical questions from a file (.txt or .csv) and converts them into 
    natural language questions using the local LLM.
    """
    try:
        question_data = ""
        if filepath.lower().endswith('.csv'):
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                questions = [row['question'].strip() for row in reader if 'question' in row]
                question_data = "\n".join(questions)
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                question_data = f.read().strip()
                
        if not question_data:
            return "❌ Error: No valid questions found in the file."
            
    except FileNotFoundError:
        return f"❌ Error: File '{filepath}' not found."
    except Exception as e:
        return f"❌ Error reading file: {e}"
    
    system_prompt = """Your task is to take the given text and format it as a question as close to natural language as possible.
You are given data in the following format:
What Vegetable has_taste woody
What Vegetable has_shape long

You need to remove all unnecessary characters, change the grammar so that these questions are as similar as possible to the text written by a normal person.
Output ONLY generated questions, one per line. No spoken placeholder."""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Convert the following logical questions into natural language:\n{question_data}"}
            ],
            temperature=0.1,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error during LLM API call: {e}"

# %% [markdown]
# ## Execute File Processing
# Testing the function on a provided file.

# %%
# Check if a filename was passed as a command-line argument
if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
    target_filepath = sys.argv[1]
else:
    # Default fallback
    target_filepath = "questions_food_basic.txt"

print(f"Processing file: {target_filepath}...\n")

try:
    if is_connected:
        natural_questions_str = generate_natural_questions_from_file(target_filepath)
        print("Generated Natural Language Questions:")
        print("-" * 40)
        print(natural_questions_str)
        
        # Save to new CSV if input was CSV
        if target_filepath.lower().endswith('.csv') and not natural_questions_str.startswith('❌ Error'):
            base_name, ext = os.path.splitext(target_filepath)
            new_filepath = f"{base_name}_LLM_processed{ext}"
            
            # Split the LLM output into a list of lines
            nl_questions = [line.strip() for line in natural_questions_str.split('\n') if line.strip()]
            
            # Read the original CSV rows
            with open(target_filepath, 'r', encoding='utf-8') as f:
                reader_obj = csv.DictReader(f)
                fieldnames = reader_obj.fieldnames
                rows = list(reader_obj)
            
            # Update the question column
            q_idx = 0
            for row in rows:
                if 'question' in row:
                    if q_idx < len(nl_questions):
                        row['question'] = nl_questions[q_idx]
                    q_idx += 1
            
            # Write to the new CSV
            if fieldnames:
                with open(new_filepath, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                
                print("-" * 40)
                print(f"✅ Saved processed dataset to: {new_filepath}")
                
                if len(nl_questions) != q_idx:
                    print(f"⚠️ Warning: Number of generated questions ({len(nl_questions)}) "
                          f"did not perfectly match the original questions count ({q_idx}).")
            else:
                print("⚠️ Error: CSV fieldnames not found.")

    else:
        print("⚠️ Skipping generation because the LLM server is not connected.")
except Exception as e:
    print(f"❌ Failed to process the file. Error: {e}")
