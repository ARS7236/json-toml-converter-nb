import os
import sys
import subprocess
import shutil
import glob

# Locate pyinstaller.exe dynamically
scripts_dir = os.path.join(sys.prefix, "Scripts")
user_scripts_dir = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Python", f"Python{sys.version_info.major}{sys.version_info.minor}", "Scripts")

pyinstaller_path = os.path.join(user_scripts_dir, "pyinstaller.exe")

if not os.path.exists(pyinstaller_path):
    pyinstaller_path = os.path.join(scripts_dir, "pyinstaller.exe")

if not os.path.exists(pyinstaller_path):
    print("Could not find pyinstaller.exe automatically.")
    print("Reinstalling PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--force-reinstall", "pyinstaller"])

# Execute the build command
cmd = [pyinstaller_path, "--onefile", "--name=tomlifier", "tomlify.py"]
print(f"Running command: {' '.join(cmd)}")
subprocess.run(cmd)

# find any exe files in the dist directory
dist_dir = os.path.join(os.getcwd(), "dist")
exe_files = glob.glob(os.path.join(dist_dir, "*.exe"))

# moving exe to the root directory
for exe in exe_files:
    filename = os.path.basename(exe)
    shutil.move(exe, os.path.join(os.getcwd(), filename))

if not exe_files:
    print("No .exe files found in the dist directory. Please check the build process for errors.")
elif len(exe_files) > 1:
    print("Multiple .exe files found in the dist directory. Please check the dist folder.")
else:
    print(f"Build completed successfully. Executable created: {os.path.basename(exe_files[0])}")

# cleanup
if os.path.exists("build"):
    shutil.rmtree("build")

if os.path.exists("dist"):
    shutil.rmtree("dist")

if os.path.exists("tomlifier.spec"):
    os.remove("tomlifier.spec")