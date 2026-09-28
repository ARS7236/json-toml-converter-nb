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

        try:
            with open(toml_path, "r", encoding="utf-8") as f:
                data = tomllib.loads(f.read())
        except Exception as e:
            print(f"Error: Failed to read '{toml_path}': {e}")
            return

        # Restore the JSON layout used by the JSON-to-TOML converter.
        ordered_data = {}
        ordered_data["$schema"] = "https://ext.nulls.gg/mods/schema/schema.json"
        for key in ("@title", "@description", "@author", "@gv", "@version"):
            if key in data:
                ordered_data[key] = data.pop(key)
        ordered_data.update(data)

        # Convert to JSON with pretty printing
        json_content = json.dumps(ordered_data, indent=2, ensure_ascii=False)

        final_content = json_content

        # 5. Save to output
        with open(output_json_path, "w", encoding="utf-8") as f:
            f.write(final_content)

        print(f"Successfully converted '{toml_path}' -> '{output_json_path}'")
