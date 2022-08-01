import json
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import requests
from datamodel_code_generator import InputFileType, generate

discovery_url = sys.argv[1]
output_filename = sys.argv[2]

# Load the input file from rest.json

# with open('rest.json') as f:
#    input_file = json.load(f)

input_file = requests.get(discovery_url).json()

# GCP puts the schemas in the "schemas" key,
# but they aren't in the proper JSON format.
# So we need to fix them up...


tempdir = TemporaryDirectory()

# save the current working directory
cwd = os.getcwd()

os.chdir(tempdir.name)

schemas = input_file["schemas"]


def recursive_replace_any(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "additionalProperties":
                if "type" in v and v["type"] == "any":
                    v["type"] = "object"

            recursive_replace_any(v)


recursive_replace_any(schemas)

aaa = json.dumps(schemas, indent=2)
print(aaa)

for name, schema in schemas.items():
    with open(f"{name}", "w") as f:
        schema["title"] = name
        json.dump(schema, f)

props = {}
for name in schemas.keys():

    props[name] = {"$ref": name}

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": props,
}

with TemporaryDirectory() as temporary_directory_name:
    temporary_directory = Path(temporary_directory_name)
    output = Path(temporary_directory / "model.py")
    generate(
        json.dumps(schema),
        input_file_type=InputFileType.JsonSchema,
        input_filename="schemas.json",
        output=output,
        snake_case_field=True,
        use_title_as_name=True,
        reuse_model=True,
    )
    model: str = output.read_text()

tempdir.cleanup()

# restore the current working directory
os.chdir(cwd)

# write the model to the output file
with open(output_filename, "w") as f:
    f.write(model)
