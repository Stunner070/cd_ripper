import os
import sys

# Optional: Disable some console outputs on Windows
if sys.platform == "win32":
    # Prevent creating a console window if run via pythonw.exe
    pass

import gui

def main():
    if getattr(sys, 'frozen', False):
        # Running as a compiled .exe
        base_dir = os.path.dirname(sys.executable)
    else:
        # Running in standard Python environment
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
    app = gui.RipperApp(base_dir)
    app.mainloop()

if __name__ == "__main__":
    main()
