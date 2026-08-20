# Tomlify
## A tool that converts JSON files to TOML and TOML files to JSON

This tool is intended for Null's Brawl Mods modders who need to convert their `content.json` files to `content.toml`, or convert TOML files back to JSON.

I know, that's useless and why would you needed it, but who want's it? 
(me just because im bored).

Current version is 2.5.0 Deep Cavern.

## How to use it
- Download `tomlify.exe` from latest [release](https://github.com/ARS7236/json-toml-converter-nb/releases).
- Place the executable in the same folder as the file you want to convert, or provide file paths explicitly.

### JSON to TOML
The output file is optional. If omitted, a `.toml` file is created next to the input JSON file.
```
tomlify.exe tomlify <content.json> [content.toml]
```

### TOML to JSON
The output file is optional. If omitted, a `.json` file is created next to the input TOML file.
```text
tomlify.exe jsonify <content.toml> [content.json]
```

For help, use `tomlify.exe --help tomlify` or `tomlify.exe --help jsonify`.

## Build
To build the tool on your PC, use the included `build.py` script. Keep the script, the entry point, and the `modules` folder together:
- `build.py`
- tomlify.py
- `modules/json_to_toml.py`
- `modules/toml_to_json.py`

The build script uses PyInstaller and includes both converter modules in the executable. It places the finished `tomlify.exe` in the project root and removes temporary build files.

Open a command prompt in the project folder and run:
```
py build.py
```
You can also double-click `build.py` to start the build.
And done with the build. (^_^)
