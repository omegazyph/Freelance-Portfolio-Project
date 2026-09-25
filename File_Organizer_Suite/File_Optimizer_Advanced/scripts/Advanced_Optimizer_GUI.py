"""
Date:           2026-01-05
Script Name:    Advanced_Optimizer_GUI.py
Author:         omegazyph
Updated:        2026-02-25
Description:    A professional-grade file organizer with a Windows 11 UI.
                Features real-time move monitoring and embedded assets.
"""

import os
import sys
import shutil
import logging
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

# ---------------------------------------------------------
# PATH LOGIC (MAKES SURE THE LOGO WORKS IN THE EXE)
# ---------------------------------------------------------

def resource_path(relative_path):
    """
    Standard fix for PyInstaller. When this becomes an EXE, 
    files are unpacked to a temp folder (_MEIPASS). This finds them.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_app_root():
    """
    Decides where to put user files (logs/config).
    If it's an EXE, we put them in the same folder as the EXE.
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    # If running in VSCode, go up one level from 'scripts'
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define our working directories
APP_ROOT = get_app_root()
LOG_DIR = os.path.join(APP_ROOT, 'logs')
CONFIG_DIR = os.path.join(APP_ROOT, 'config')

# Create folders if they aren't there yet
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

# ---------------------------------------------------------
# BACK-END LOGIC (THE HEAVY LIFTING)
# ---------------------------------------------------------

# Set up the activity log
log_path = os.path.join(LOG_DIR, 'file_moves.log')
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filemode='a' 
)

def get_categories():
    """Loads the file grouping rules from the JSON config."""
    config_path = os.path.join(CONFIG_DIR, 'config.json')
    
    # Default sorting rules
    default_rules = {
        'Documents':   ['.pdf', '.doc', '.docx', '.txt', '.xlsx'],
        'Images':      ['.jpg', '.jpeg', '.png', '.gif', '.svg'],
        'Videos':      ['.mp4', '.mov', '.avi'],
        'Compressed':  ['.zip', '.rar', '.7z'],
        'Dev_Files':   ['.py', '.sh', '.js', '.html', '.json'],
        'Apps':        ['.exe', '.msi', '.bat']
    }
    
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            json.dump(default_rules, f, indent=4)
        return default_rules
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception:
        return default_rules

def organize_files():
    """The main move process."""
    folder = folder_path_var.get()
    
    if not folder or folder == "No folder selected":
        messagebox.showwarning("Wait!", "You need to pick a folder first.")
        return

    rules = get_categories()
    
    # Reset the live monitor box
    monitor_display.config(state="normal")
    monitor_display.delete("1.0", "end")
    
    try:
        # Get all files, but don't try to move the program itself!
        current_exe = os.path.basename(sys.executable)
        all_files = [f for f in os.listdir(folder) 
                     if os.path.isfile(os.path.join(folder, f)) and f != current_exe]
        
        if not all_files:
            status_text.set("Status: Nothing to clean up!")
            return

        progress_bar['maximum'] = len(all_files)
        count = 0
        
        for file in all_files:
            ext = os.path.splitext(file)[1].lower()
            target_subfolder = "Misc_Others"
            
            # Figure out where this file belongs
            for cat_name, extensions in rules.items():
                if ext in extensions:
                    target_subfolder = cat_name
                    break
            
            # Path setup
            final_dir = os.path.join(folder, target_subfolder)
            os.makedirs(final_dir, exist_ok=True)
            
            source = os.path.join(folder, file)
            destination = os.path.join(final_dir, file)

            # Move the file (shutil handles the work)
            shutil.move(source, destination)
            count += 1
            
            # UI Updates: Progress bar and scrolling text
            progress_bar['value'] = count
            monitor_display.insert("end", f"✔ Moved: {file} → {target_subfolder}\n")
            monitor_display.see("end")
            app.update_idletasks()
            logging.info(f"Moved {file} to {target_subfolder}")

        status_text.set(f"Status: Finished! Moved {count} files.")
        messagebox.showinfo("Done", f"I've organized {count} files for you.")
        progress_bar['value'] = 0
        
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")
    finally:
        monitor_display.config(state="disabled")

# ---------------------------------------------------------
# FRONT-END (GUI DESIGN)
# ---------------------------------------------------------

app = tk.Tk()
app.title("File Optimizer Pro")
app.geometry("900x650")
app.configure(bg="#F3F3F3") # Windows 11 Light Grey

folder_path_var = tk.StringVar(value="No folder selected")
status_text = tk.StringVar(value="Status: Ready to work")

# --- SIDEBAR ---
sidebar = tk.Frame(app, bg="#EBEBEB", width=250)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

# Load the logo (looking inside the internal assets)
logo_path = resource_path(os.path.join('assets', 'logo.png'))
if os.path.exists(logo_path):
    try:
        raw_img = Image.open(logo_path)
        resized = raw_img.resize((150, 150), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(resized)
        logo_label = tk.Label(sidebar, image=logo_img, bg="#EBEBEB")
        logo_label.image = logo_img # Garbage collection fix
        logo_label.pack(pady=35)
    except Exception:
        tk.Label(sidebar, text="OPTIMIZER", font=("Segoe UI", 12, "bold"), bg="#EBEBEB").pack(pady=40)
else:
    tk.Label(sidebar, text="OPTIMIZER", font=("Segoe UI", 12, "bold"), bg="#EBEBEB").pack(pady=40)

# Sidebar Buttons
def add_btn(txt, cmd):
    tk.Button(sidebar, text=txt, font=("Segoe UI", 10), bg="#EBEBEB", relief="flat", 
              anchor="w", padx=30, pady=12, cursor="hand2", command=cmd).pack(fill="x")

add_btn("📁 Choose Folder", lambda: folder_path_var.set(filedialog.askdirectory() or folder_path_var.get()))
add_btn("⚙️ Open Settings", lambda: os.startfile(CONFIG_DIR))
add_btn("📄 Check Logs", lambda: os.startfile(log_path))

# --- MAIN VIEW ---
main = tk.Frame(app, bg="#F3F3F3", padx=45, pady=35)
main.pack(side="right", fill="both", expand=True)

tk.Label(main, text="Organize Files", font=("Segoe UI Variable Display", 26, "bold"), bg="#F3F3F3").pack(anchor="w")
tk.Label(main, text="Select a directory to sort files into smart categories.", 
         font=("Segoe UI", 10), bg="#F3F3F3", fg="#666666").pack(anchor="w", pady=(0, 25))

# Path Box
path_card = tk.Frame(main, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
path_card.pack(fill="x", pady=10)
tk.Label(path_card, textvariable=folder_path_var, font=("Segoe UI", 10), bg="white", fg="#0067C0", padx=15, pady=20).pack(anchor="w")

# Live Feed Box
tk.Label(main, text="Live Activity Monitor", font=("Segoe UI", 9, "bold"), bg="#F3F3F3", fg="#666666").pack(anchor="w", pady=(15, 5))
feed_frame = tk.Frame(main, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
feed_frame.pack(fill="both", expand=True)

monitor_display = tk.Text(feed_frame, height=12, bg="#FBFBFB", relief="flat", font=("Consolas", 9), state="disabled", padx=10, pady=10)
monitor_display.pack(fill="both", expand=True, padx=5, pady=5)

# Progress and Action
tk.Label(main, textvariable=status_text, font=("Segoe UI", 9), bg="#F3F3F3", fg="#666666").pack(anchor="w", pady=(20, 5))
progress_bar = ttk.Progressbar(main, orient="horizontal", mode="determinate")
progress_bar.pack(fill="x", pady=(0, 30))

tk.Button(main, text="Start Optimization", command=organize_files, bg="#0067C0", fg="white", 
          font=("Segoe UI", 12, "bold"), relief="flat", height=2, cursor="hand2").pack(fill="x")

app.mainloop()