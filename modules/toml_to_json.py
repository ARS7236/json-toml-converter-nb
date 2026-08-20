import json
import os
import sys

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


class TOMLToJSONConverter:
    def convert_toml_to_json(self, toml_path: str, output_json_path: str) -> None:
        if not os.path.exists(toml_path):
            print(f"Error: Target file '{toml_path}' was not found.")
            return

        with open(toml_path, "r", encoding="utf-8") as f:
            data = tomllib.loads(f.read())

        # Add schema reference
        data["$schema"] = "https://ext.nulls.gg/mods/schema/schema.json"

        # Convert to JSON with pretty printing
        json_content = json.dumps(data, indent=2, ensure_ascii=False)

        final_content = json_content

        # 5. Save to output
        with open(output_json_path, "w", encoding="utf-8") as f:
            f.write(final_content)

        print(f"Successfully converted '{toml_path}' -> '{output_json_path}'")
