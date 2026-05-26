# 💿 Antigravity CD Ripper

> [!NOTE]
> This project is **100% free to use**, **fully vibecoded**, and **open for anyone** to improve, fork, or customize! Feel free to open issues, submit pull requests, or tweak it to your heart's content.

A lightweight, premium-looking desktop application for Windows to rip Audio CDs into MP3 files. Built with Python and **CustomTkinter** for a modern, sleek dark-themed GUI, it automates the process of extracting digital audio using the powerful **fre:ac** (Free Audio Converter) command-line tool.

---

## 📥 Download & Run (No Coding Required!)

If you just want to rip your CDs and don't want to deal with code, Python, or terminal commands, you can download the ready-to-run Windows application immediately:

1. **Download**: Go to the **Releases** section of this repository and download the latest `cd_ripper.exe` file. Or download it here: https://github.com/Stunner070/cd_ripper/releases/download/Full_Release_EXE/cd_ripper.exe
2. **Launch**: Double-click `cd_ripper.exe` to open the application!

> [!IMPORTANT]
> **⚠️ Windows SmartScreen Alert:**
> Because this is an open-source, indie-compiled program, Windows might show a blue warning popup saying *"Windows protected your PC"* when you first launch it.
> *   **To run it**: Click **"More info"** on the popup, and then click **"Run anyway"**. This warning is completely normal for hobbyist software and will only ask you once!
>
> **⚡ First-Run Auto Setup:**
> On the very first run, the app will automatically create a `bin/` directory right next to `cd_ripper.exe` and download the necessary `fre:ac` converter engine (approx. 15MB). This takes only a few seconds, and once completed, the app will open instantly on all future launches!

---



## ✨ Features

- **💿 Automatic CD Drive Detection**: Dynamically scans for connected CD/DVD/Blu-ray drives and detects when an Audio CD is inserted.
- **⚡ Zero-Config External Tool Setup**: No need to download anything manually! The app automatically downloads and configures the `fre:ac` cmd tool in the background when first run.
- **🎨 Modern Dark Mode GUI**: A sleek, fluid user interface designed using `customtkinter` with glassmorphic accents and high responsiveness.
- **🔄 Non-Blocking Background Operations**: Runs the ripping process in a separate background thread so the GUI remains completely interactive and never freezes.
- **📂 Smart Audio Compression**: Encodes tracks to high-quality MP3 format using the industry-standard **LAME MP3 Encoder**.
- **📝 Live Logs**: A real-time log box showing the exact command execution, extraction steps, and encoding progress.

---

## 🛠️ Prerequisites

- **Operating System**: Windows (required for CD drive detection APIs and automatic tool configuration).
- **Python**: Python 3.8 or newer (make sure to select the **"Add Python to PATH"** option during installation).

---

## 🚀 Easy Setup Guide

Follow these simple steps to get the CD Ripper up and running on your machine:

### Step 1: Clone or Download the Repo

Open your terminal or command prompt and clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/cd_ripper.git
cd cd_ripper
```

*(Alternatively, you can click **Code -> Download ZIP** on GitHub, extract the folder, and open your terminal inside that folder).*

### Step 2: Set Up a Virtual Environment (Recommended)

Creating a virtual environment keeps your Python dependencies isolated and clean:

```powershell
# Create the virtual environment
python -m venv .venv

# Activate it (on Windows Powershell)
.venv\Scripts\Activate.ps1

# Or on Command Prompt (CMD)
.venv\Scripts\activate.bat
```

### Step 3: Install Required Libraries

Install the GUI packages and libraries defined in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 4: Run the App!

Start the CD Ripper by executing:

```bash
python cd_ripper.py
```

Once the window opens, insert an Audio CD. The app will detect it, fetch the tracks, and let you select an output folder before clicking **Rip CD to MP3**!

---

## 📂 Project Structure

- `cd_ripper.py` - The application entry point.
- `gui.py` - CustomTkinter application definition, layout, and event handlers.
- `ripper_core.py` - Core logic for drive scanning, auto-downloading `fre:ac`, and invoking background threads.
- `requirements.txt` - Python dependencies (CustomTkinter).
- `bin/` *(Auto-generated on run)* - Where `fre:ac` is downloaded and run from.

---

## 🔧 Troubleshooting

### ❌ `_tkinter.TclError: Can't find a usable init.tcl`
If you encounter this error on startup, it means your Python installation is missing the necessary Tk/Tcl script libraries or their environment variables are misconfigured. 

#### Quick Fix:
1. **Repair/Reinstall Python**: 
   - Download the official Python installer for your version from [python.org](https://www.python.org/downloads/).
   - Run the installer, select **Modify**, and make sure **tcl/tk and IDLE** is checked.
   - Proceed with the installation/repair.
2. **Manually set Environment Variables**:
   If the repair doesn't fix it, you can point Windows to where your Tcl files are located:
   - Search for "Environment Variables" in the Windows Search menu.
   - Add a new **User Variable** named `TCL_LIBRARY` and set its value to your Tcl path, e.g.:
     `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python313\tcl\tcl8.6`
   - Add another **User Variable** named `TK_LIBRARY` and set its value to your Tk path, e.g.:
     `C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python313\tcl\tk8.6`
   - Restart your terminal/VS Code and try running `python cd_ripper.py` again.

### ❌ CD Drive not detected
- Ensure that the CD/DVD drive is properly plugged in and recognized by Windows Explorer (should have a drive letter like `D:\` or `E:\`).
- Ensure there is a physical Audio CD inserted in the tray. Note that standard data CDs, DVDs, or empty discs will not show track lists.

---

## 📦 How to Build a Standalone `.exe` (For Releases)

If you want to share this app with non-coders (or run it yourself without having Python installed), you can package it into a single, double-clickable Windows `.exe` file.

Due to known bugs in Python 3.13's virtual environment setup on Windows, a standard `pyinstaller` command might fail to include `tkinter` (resulting in `ModuleNotFoundError: No module named 'tkinter'`). To make building easy and bug-free, a helper script `build_exe.py` is included!

### Step 1: Install PyInstaller
Ensure your virtual environment is active, and install PyInstaller:
```bash
pip install pyinstaller
```

### Step 2: Build the Executable
Run the custom builder script:
```bash
python build_exe.py
```

This helper script automatically:
1. Locates the correct Tcl/Tk system folders on your machine.
2. Injects the required environment paths to ensure `tkinter` is bundled successfully.
3. Automatically deletes old cache files so you get a clean build.
4. Compiles the app with standard parameters (`--noconsole`, `--onefile`, `--collect-all customtkinter`).

### Step 3: Find your `.exe`
Once the builder script prints `SUCCESS!`:
1. Open the newly created `dist/` folder in your project directory.
2. Inside, you will find `cd_ripper.exe`.
3. You can copy this `cd_ripper.exe` anywhere (like your Desktop) and run or share it directly!

> [!TIP]
> When you first run `cd_ripper.exe`, it will automatically create a `bin/` directory right next to itself and download `fre:ac` into it. After the first run, it will launch instantly without any download delays!

---

## 📄 License

This project is open-source and licensed under the MIT License.
