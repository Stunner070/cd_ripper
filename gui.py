import os
import customtkinter as ctk
from tkinter import filedialog
import ripper_core

class RipperApp(ctk.CTk):
    def __init__(self, base_dir):
        super().__init__()
        
        self.base_dir = base_dir
        self.cd_drives = []
        self.selected_drive_index = -1
        self.is_ripping = False
        
        self.title("Antigravity CD Ripper")
        self.geometry("600x500")
        self.minsize(500, 400)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        
        # Status Frame
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="Detecting CD Drives...", font=ctk.CTkFont(size=16, weight="bold"))
        self.status_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Track Overview Frame
        self.track_frame = ctk.CTkFrame(self)
        self.track_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.track_frame.grid_columnconfigure(0, weight=1)
        
        self.track_label = ctk.CTkLabel(self.track_frame, text="Track Overview:", font=ctk.CTkFont(weight="bold"))
        self.track_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.track_box = ctk.CTkTextbox(self.track_frame, height=80, state="disabled")
        self.track_box.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        # Output Directory Frame
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.output_frame.grid_columnconfigure(1, weight=1)
        
        self.output_label = ctk.CTkLabel(self.output_frame, text="Output Directory:")
        self.output_label.grid(row=0, column=0, padx=10, pady=10)
        
        # Default to user's Music folder
        default_out = os.path.join(os.path.expanduser("~"), "Music")
        self.output_var = ctk.StringVar(value=default_out)
        self.output_entry = ctk.CTkEntry(self.output_frame, textvariable=self.output_var, state="readonly")
        self.output_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")
        
        self.browse_btn = ctk.CTkButton(self.output_frame, text="Browse", width=80, command=self.browse_output)
        self.browse_btn.grid(row=0, column=2, padx=(0, 10), pady=10)
        
        # Rip Button
        self.rip_btn = ctk.CTkButton(self, text="Rip CD to MP3", font=ctk.CTkFont(size=18, weight="bold"), height=50, command=self.start_rip)
        self.rip_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.rip_btn.configure(state="disabled")
        
        # Log Box
        self.log_box = ctk.CTkTextbox(self, state="disabled")
        self.log_box.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="nsew")
        
        self.log_message("Application started. Waiting for CD...")
        
        # Start background polling for CD drives
        self.poll_drives()
        
    def log_message(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        
    def browse_output(self):
        folder = filedialog.askdirectory(initialdir=self.output_var.get())
        if folder:
            self.output_var.set(folder)
            
    def poll_drives(self):
        if not self.is_ripping:
            self.cd_drives = ripper_core.get_cd_drives()
            if not self.cd_drives:
                self.status_label.configure(text="No CD/DVD drive detected.", text_color="gray")
                self.rip_btn.configure(state="disabled")
                self.selected_drive_index = -1
                self.update_track_box("No CD/DVD drive detected.")
            else:
                # We'll just use the first detected CD drive for simplicity
                drive_path = self.cd_drives[0]
                self.selected_drive_index = 0
                has_cd, num_tracks, tracks = ripper_core.has_audio_cd(drive_path)
                
                if has_cd:
                    self.status_label.configure(text=f"Drive {drive_path} - Audio CD found ({num_tracks} tracks)", text_color="#28a745")
                    self.rip_btn.configure(state="normal")
                    
                    track_names = [os.path.basename(t) for t in tracks]
                    self.update_track_box("\n".join(track_names))
                else:
                    self.status_label.configure(text=f"Drive {drive_path} - Please insert an Audio CD", text_color="#ffc107")
                    self.rip_btn.configure(state="disabled")
                    self.update_track_box("Waiting for Audio CD...")
                    
        # Poll again after 2 seconds
        self.after(2000, self.poll_drives)
        
    def update_track_box(self, text):
        self.track_box.configure(state="normal")
        self.track_box.delete("1.0", "end")
        self.track_box.insert("1.0", text)
        self.track_box.configure(state="disabled")
        
    def start_rip(self):
        if self.selected_drive_index == -1:
            return
            
        self.is_ripping = True
        self.rip_btn.configure(state="disabled", text="Ripping in progress...")
        self.browse_btn.configure(state="disabled")
        self.status_label.configure(text="Ripping...", text_color="#17a2b8")
        
        out_dir = self.output_var.get()
        self.log_message(f"Starting rip to {out_dir}")
        
        # Execute ripping in background
        ripper_core.start_ripping(
            base_dir=self.base_dir,
            drive_index=self.selected_drive_index,
            output_dir=out_dir,
            log_callback=self.safe_log,
            on_complete=self.on_rip_complete
        )
        
    def safe_log(self, msg):
        # Update log from background thread safely
        self.after(0, self.log_message, msg)
        
    def on_rip_complete(self):
        self.after(0, self._handle_rip_complete)
        
    def _handle_rip_complete(self):
        self.is_ripping = False
        self.rip_btn.configure(state="normal", text="Rip CD to MP3")
        self.browse_btn.configure(state="normal")
        self.poll_drives() # Force a poll right now to update status

if __name__ == "__main__":
    app = RipperApp(os.path.dirname(os.path.abspath(__file__)))
    app.mainloop()
