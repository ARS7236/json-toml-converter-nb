import os
import sys
import subprocess
import shutil
import glob

project_dir = os.path.dirname(os.path.abspath(__file__))
entry_point = os.path.join(project_dir, "tomlify.py")

# Run PyInstaller through the active Python environment.
pyinstaller_check = subprocess.run(
    [sys.executable, "-m", "PyInstaller", "--version"],
    cwd=project_dir,
)
if pyinstaller_check.returncode != 0:
    print("PyInstaller is not installed. Installing it now...")
    install_result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "pyinstaller"],
        cwd=project_dir,
    )
    if install_result.returncode != 0:
        raise SystemExit("Could not install PyInstaller.")

# Explicit hidden imports ensure both modules are bundled into the executable.
cmd = [
    sys.executable,
    "-m",
    "PyInstaller",
    "--onefile",
    "--clean",
    "--noconfirm",
    "--paths",
    project_dir,
    "--hidden-import",
    "modules.json_to_toml",
    "--hidden-import",
    "modules.toml_to_json",
    "--name",
    "tomlify",
    entry_point,
]
print(f"Running command: {' '.join(cmd)}")
build_result = subprocess.run(cmd, cwd=project_dir)
if build_result.returncode != 0:
    raise SystemExit("Build failed. See the PyInstaller output above.")

# find any exe files in the dist directory
dist_dir = os.path.join(project_dir, "dist")
exe_files = glob.glob(os.path.join(dist_dir, "*.exe"))

# moving exe to the root directory
for exe in exe_files:
    filename = os.path.basename(exe)
    shutil.move(exe, os.path.join(project_dir, filename))

if not exe_files:
    print("No .exe files found in the dist directory. Please check the build process for errors.")
elif len(exe_files) > 1:
    print("Multiple .exe files found in the dist directory. Please check the dist folder.")
else:
    print(f"Build completed successfully. Executable created: {os.path.basename(exe_files[0])}")

# cleanup
build_dir = os.path.join(project_dir, "build")
spec_file = os.path.join(project_dir, "tomlify.spec")

if os.path.exists(build_dir):
    shutil.rmtree(build_dir)

if os.path.exists(dist_dir):
    shutil.rmtree(dist_dir)

if os.path.exists(spec_file):
    os.remove(spec_file)