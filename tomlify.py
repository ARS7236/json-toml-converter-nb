import json
import os
import sys
import tomli_w

PROGRAM_NAME = "JSON to TOML Converter"
VERSION = "v1.0.0"
AUTHOR = "ars7236"

def print_help_info():
    print(f"{PROGRAM_NAME} {VERSION}")
    print(f"Created by: {AUTHOR}\n")
    print("How to use it:")
    print("<content.json> is your input json file you want to convert")
    print("<content.toml> is you want to output the converted toml file")
    print("usage:")
    print("tomlifier.exe <content.json> <content.toml>\n")

def clean_nulls(data):
    if isinstance(data, dict):
        return {k: clean_nulls(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [clean_nulls(v) for v in data if v is not None]
    return data

def convert_json_to_toml(json_path: str, output_toml_path: str) -> None:
    if not os.path.exists(json_path):
        print(f"Error: Target file '{json_path}' was not found.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.pop("$schema", None)
    clean_data = clean_nulls(data)

    # 1. Extract scalar fields for the very top (@author, @gv)
    top_meta = {}
    if "@author" in clean_data:
        top_meta["@author"] = clean_data.pop("@author")
    if "@gv" in clean_data:
        top_meta["@gv"] = clean_data.pop("@gv")

    # 2. Extract title and description tables
    title_data = {"@title": clean_data.pop("@title")} if "@title" in clean_data else {}
    desc_data = {"@description": clean_data.pop("@description")} if "@description" in clean_data else {}

    # 3. Serialize each section separately
    meta_toml = tomli_w.dumps(top_meta) if top_meta else ""
    title_toml = tomli_w.dumps(title_data) if title_data else ""
    desc_toml = tomli_w.dumps(desc_data) if desc_data else ""
    remaining_toml = tomli_w.dumps(clean_data) if clean_data else ""

    # 4. Assemble final file structure
    header = (
        "# This content.toml was created with Aurora bot by ARS7236\n"
        "# Use schema: https://ext.nulls.gg/mods/schema/schema.json\n\n"
    )

    final_content = header
    if meta_toml:
        final_content += meta_toml + "\n"
    if title_toml:
        final_content += title_toml + "\n"
    if desc_toml:
        final_content += desc_toml + "\n"
    if remaining_toml:
        final_content += remaining_toml

    # 5. Save to output
    with open(output_toml_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"Successfully converted '{json_path}' -> '{output_toml_path}'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help_info()
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "content.toml"
        convert_json_to_toml(input_file, output_file)