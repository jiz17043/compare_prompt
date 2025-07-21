import json
import csv
from openai import OpenAI
from config import OPENAI_MODEL, TEMPERATURE
from evaluation.test_runner import run_test_code
from evaluation.metrics import is_valid_python

# Create OpenAI client
client = OpenAI()

# Load functions and prompts
with open("data/functions.json") as f:
    functions = json.load(f)

with open("prompts/unit_test_prompts.json") as f:
    prompts = json.load(f)

# Output results
with open("outputs/responses.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["function_id", "prompt_id", "valid_syntax", "returncode", "stderr", "generated_test"])

    for func in functions:
        for prompt_id, template in prompts.items():
            prompt = template.format(**func)

            # Updated usage
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=TEMPERATURE
            )

            test_code = response.choices[0].message.content
            valid = is_valid_python(test_code)
            result = run_test_code(func["function_code"], test_code)

            writer.writerow([
                func["id"], prompt_id, valid,
                result["returncode"], result["stderr"], test_code.strip().replace("\n", "\\n")
            ])
