import os
import ctypes
import glob
import urllib.request
import zipfile
import subprocess
import threading

FREAC_URL = "https://github.com/enzo1982/freac/releases/download/v1.1.7/freac-1.1.7-windows-x64.zip"

def get_cd_drives():
    """Returns a list of CD drive paths (e.g. ['D:\\'])"""
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if bitmask & 1:
            drive_path = f"{letter}:\\"
            if ctypes.windll.kernel32.GetDriveTypeW(drive_path) == 5: # DRIVE_CDROM
                drives.append(drive_path)
        bitmask >>= 1
    return drives

def has_audio_cd(drive_path):
    """Checks if the given drive has an audio CD by looking for .cda files."""
    cda_files = glob.glob(os.path.join(drive_path, '*.cda'))
    return len(cda_files) > 0, len(cda_files), cda_files

def ensure_freac(base_dir, log_callback=None):
    """Ensures freaccmd.exe is downloaded and available."""
    bin_dir = os.path.join(base_dir, 'bin')
    os.makedirs(bin_dir, exist_ok=True)
    
    found_freac = None
    for root, dirs, files in os.walk(bin_dir):
        if 'freaccmd.exe' in files:
            found_freac = os.path.join(root, 'freaccmd.exe')
            break
            
    if found_freac:
        return found_freac
        
    if log_callback: log_callback("freaccmd.exe not found. Downloading fre:ac...")
    zip_path = os.path.join(bin_dir, 'freac.zip')
    
    urllib.request.urlretrieve(FREAC_URL, zip_path)
    
    if log_callback: log_callback("Download complete. Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(bin_dir)
        
    os.remove(zip_path)
    
    for root, dirs, files in os.walk(bin_dir):
        if 'freaccmd.exe' in files:
            found_freac = os.path.join(root, 'freaccmd.exe')
            break
            
    if found_freac:
        if log_callback: log_callback(f"Successfully configured fre:ac.")
        return found_freac
    else:
        raise FileNotFoundError("Could not find freaccmd.exe after extraction.")

def rip_cd_thread(freac_path, drive_index, output_dir, log_callback, on_complete):
    try:
        # -e LAME: Encode using LAME MP3 encoder
        # -d output_dir: Save files to the specified directory
        # -p pattern: Format the output filename and directory structure
        # -cddb: Try to fetch metadata automatically
        # -cd index: The 0-based index of the CD drive
        # -track all: Rip all tracks
        cmd = [
            freac_path,
            "-e", "LAME",
            "-d", output_dir,
            "-p", "<artist> - <album>\\<track> - <title>",
            "-cddb",
            "-cd", str(drive_index),
            "-t", "all"
        ]
        
        if log_callback:
            log_callback(f"Executing extraction...")
            
        # creationflags=0x08000000 suppresses the popup console window on Windows
        CREATE_NO_WINDOW = 0x08000000
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True, 
            creationflags=CREATE_NO_WINDOW
        )
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output and log_callback: 
                log_callback(output.strip())
                
        rc = process.poll()
        if rc == 0:
            if log_callback: log_callback("Ripping completed successfully!")
        else:
            if log_callback: log_callback(f"Ripping failed with return code {rc}.")
            
    except Exception as e:
        if log_callback: log_callback(f"Error during ripping: {str(e)}")
    finally:
        if on_complete:
            on_complete()

def start_ripping(base_dir, drive_index, output_dir, log_callback, on_complete):
    """Starts the ripping process in a background thread."""
    try:
        freac_path = ensure_freac(base_dir, log_callback)
        t = threading.Thread(target=rip_cd_thread, args=(freac_path, drive_index, output_dir, log_callback, on_complete), daemon=True)
        t.start()
    except Exception as e:
        if log_callback: log_callback(f"Initialization error: {str(e)}")
        if on_complete: on_complete()
