# Tomlify - A simple tool to convert JSON files to TOML format.
# Author: ars7236
# Version: 1.5.0
# License: GNU General Public License v3.0

import json
import os
import sys
import tomli_w

PROGRAM_NAME = "Tomlify"
VERSION = "v2.0.0"
AUTHOR = "ars7236"

def print_info():
    print(f"{PROGRAM_NAME} {VERSION}")
    print(f"Created by: {AUTHOR}\n")

def print_help_info_new():
    print_info()
    print("Usage: python tomlify.py <input_json_file> [output_toml_file]")
    print("If output_toml_file is not provided, it will default to the input file name with a .toml extension.")

def print_help_info_old():
    print_info()
    print("How to use it:")
    print("<content.json> is your input json file you want to convert")
    print("<content.toml> is the output toml file")
    print("Usage:")
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
    if "@version" in clean_data:
        top_meta["@version"] = clean_data.pop("@version")
    else:
        top_meta["@version"] = "1.0.0"  # Default version if not present
    if not top_meta:
        top_meta = None  # If no top meta fields, set to None

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
        "# This toml file was converted and formatted in Tomlify program by ARS7236\n"
        "# Tomlify version: 2.0.0\n"
        "# Build date: 2026-08-20\n"
        "# This file is generated from a JSON file and may not be perfect. Please check the output for any issues.\n"
        "# If you find any issues, please report them to the author on github.\n"
        "# For more information, visit: https://github.com/ARS7236/Tomlify/README.md\n"
        "# This file is intended for use with Nulls' Brawl Mods and may not be compatible with other tools(like BSML by lilmuff1 on github).\n"
        "# If you are using this file with Nulls' Brawl Mod, please ensure that you have the latest version of the nulls brawl installed.\n"
        "# Tomlify is not responsible for any issues that may arise from using this file with other tools.\n"
        "# If you are using this file with other tools, please ensure that you have the latest version of those tools installed.\n"
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
        print_info()
    elif sys.argv[1] in ("-h", "--help"):
        print_help_info_new()
    elif sys.argv[0].endswith("tomlify.py"):
        print_help_info_old()
    else:
        input_file = sys.argv[1]
        base_name, _ = os.path.splitext(input_file)
        output_file = sys.argv[2] if len(sys.argv) > 2 else f"{base_name}.toml"
        convert_json_to_toml(input_file, output_file)