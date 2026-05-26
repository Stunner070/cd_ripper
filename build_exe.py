import os
import sys
import subprocess
import shutil

def main():
    print("=== Antigravity CD Ripper Executable Builder ===")
    
    # 1. Resolve base Python installation directory (where Tcl/Tk files are located)
    base_prefix = sys.base_prefix
    
    # 2. Construct standard Tcl/Tk paths for Python on Windows
    tcl_library = os.path.join(base_prefix, "tcl", "tcl8.6")
    tk_library = os.path.join(base_prefix, "tcl", "tk8.6")
    
    # Fallback search if version numbers differ
    if not os.path.exists(tcl_library):
        tcl_root = os.path.join(base_prefix, "tcl")
        if os.path.exists(tcl_root):
            for folder in os.listdir(tcl_root):
                if folder.startswith("tcl"):
                    tcl_library = os.path.join(tcl_root, folder)
                elif folder.startswith("tk"):
                    tk_library = os.path.join(tcl_root, folder)

    print(f"[*] Base Python Directory: {base_prefix}")
    print(f"[*] Found TCL_LIBRARY: {tcl_library}")
    print(f"[*] Found TK_LIBRARY: {tk_library}")
    
    # Check if paths exist, warn if not
    if not os.path.exists(tcl_library) or not os.path.exists(tk_library):
        print("[!] Warning: Could not locate Tcl/Tk libraries in the base Python directory.")
        print("    If compilation fails, make sure Python was installed with the 'tcl/tk and IDLE' option checked.")
    else:
        # Inject these paths into the environment so PyInstaller's Tkinter hooks find and bundle them
        os.environ["TCL_LIBRARY"] = tcl_library
        os.environ["TK_LIBRARY"] = tk_library
        print("[*] Environment variables injected successfully.")
    
    # 3. Clean up previous builds to avoid cache issues
    print("[*] Cleaning up old build/dist files...")
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
            except Exception as e:
                print(f"[!] Could not remove {folder}: {e}")
                
    spec_file = "cd_ripper.spec"
    if os.path.exists(spec_file):
        try:
            os.remove(spec_file)
        except Exception as e:
            print(f"[!] Could not remove {spec_file}: {e}")

    # 4. Define PyInstaller command
    cmd = [
        "pyinstaller",
        "--noconsole",
        "--onefile",
        "--collect-all", "customtkinter",
        "--hidden-import", "tkinter",
        "--hidden-import", "_tkinter",
        "cd_ripper.py"
    ]
    
    # 5. Run PyInstaller
    print(f"[*] Running command: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        print("\n[+] SUCCESS! Standalone executable created successfully.")
        print("[+] Your executable is located in: dist/cd_ripper.exe")
    except subprocess.CalledProcessError as e:
        print(f"\n[-] Error: PyInstaller build failed with exit code {e.returncode}")
        sys.exit(1)
    except FileNotFoundError:
        print("\n[-] Error: PyInstaller is not installed in this environment.")
        print("    Please run: pip install pyinstaller")
        sys.exit(1)

if __name__ == "__main__":
    main()
