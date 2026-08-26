# Tomlify - A simple tool to convert JSON files to TOML format or TOML files to JSON format.
# Author: ars7236
# Version: 2.5.2 - Deep Cavern[Hot Sea]
# License: GNU General Public License v3.0

import os
import sys
import modules.json_to_toml as JSONToTOMLConverter
import modules.toml_to_json as TOMLToJSONConverter

PROGRAM_NAME = "Tomlify"
VERSION = "v2.5.2 - Deep Cavern[Hot Sea]"
AUTHOR = "ars7236"
BUILD_DATE = "2026-08-26"

def print_info():
    print(f"{PROGRAM_NAME} {VERSION}")
    print(f"Created by: {AUTHOR}")
    print(f"Build date: {BUILD_DATE}")
    print("If you find any issues, please report them to the author on github.\n")
    print(f"Converted Toml file from {PROGRAM_NAME} is intended for use with Null's Brawl Mods and may not be compatible with other tools(like BSML by lilmuff1 on github).")
    print("If you are using converted toml file with Null's Brawl Mod, please ensure that you have the latest version of the nulls brawl installed.")
    print(f"{PROGRAM_NAME} is not responsible for any issues that may arise from using this file with other tools.")
    print("If you are using this file with other tools, please ensure that you have the latest version of those tools installed.\n")

def print_help_info_tomlify():
    print_info()
    print("How to use it:")
    print("<content.json> is your input json file you want to convert")
    print("<content.toml> is the output toml file")
    print("Usage:")
    print("tomlify.exe tomlify <content.json> [content.toml]\n")

def print_help_info_jsonify():
    print_info()
    print("How to use it:")
    print("<content.toml> is your input toml file you want to convert")
    print("<content.json> is the output json file")
    print("Usage:")
    print("tomlify.exe jsonify <content.toml> [content.json]\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_info()
    elif sys.argv[1] in ("-h", "--help") and ("tomlify" in sys.argv):
        print_help_info_tomlify()
    elif sys.argv[1] in ("-h", "--help") and ("jsonify" in sys.argv):
        print_help_info_jsonify()
    elif sys.argv[1] == "tomlify":
        if len(sys.argv) not in (3, 4):
            print_help_info_tomlify()
        else:
            json_path = sys.argv[2]
            base_name, _ = os.path.splitext(json_path)
            output_toml_path = sys.argv[3] if len(sys.argv) == 4 else f"{base_name}.toml"
            converter = JSONToTOMLConverter.JSONToTOMLConverter()
            converter.convert_json_to_toml(json_path, output_toml_path)
    elif sys.argv[1] == "jsonify":
        if len(sys.argv) not in (3, 4):
            print_help_info_jsonify()
        else:
            toml_path = sys.argv[2]
            base_name, _ = os.path.splitext(toml_path)
            output_json_path = sys.argv[3] if len(sys.argv) == 4 else f"{base_name}.json"
            converter = TOMLToJSONConverter.TOMLToJSONConverter()
            converter.convert_toml_to_json(toml_path, output_json_path)
    else:
        print_info()
        print("Error: Invalid command. Use 'tomlify' or 'jsonify'.")
        print("Use '-h' or '--help' for more information.")
