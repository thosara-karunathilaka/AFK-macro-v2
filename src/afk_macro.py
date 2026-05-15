import threading
import time
import random
import keyboard
import pydirectinput
from tkinter import messagebox
import customtkinter as ctk
import json
import os
import sys

# Gaming Theme Colors
BG_COLOR = "#09090b"
FRAME_COLOR = "#18181b"
ACCENT_COLOR = "#06b6d4" # Cyan
TEXT_COLOR = "#e4e4e7"
START_COLOR = "#10b981" # Emerald Green
START_HOVER = "#059669"
STOP_COLOR = "#ef4444" # Red
STOP_HOVER = "#dc2626"
FONT_FAMILY = "Consolas"

# Configure CustomTkinter appearance
ctk.set_appearance_mode("Dark")

# Global flags
is_running = False
macro_thread = None

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

SETTINGS_FILE = os.path.join(application_path, "settings.json")
start_hotkey = "f9"
stop_hotkey = "f10"
bucket_hotkey = "b"
tankard_hotkey = "9"
weapon1_hotkey = "1"
weapon2_hotkey = "2"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def save_settings(start_k, stop_k, bucket_k, tankard_k, w1_k, w2_k):
    with open(SETTINGS_FILE, "w") as f:
        json.dump({
            "start_key": start_k.lower(), 
            "stop_key": stop_k.lower(), 
            "bucket_key": bucket_k.lower(),
            "tankard_key": tankard_k.lower(),
            "weapon1_key": w1_k.lower(),
            "weapon2_key": w2_k.lower()
        }, f)

def log_activity(msg):
    try:
        app.after(0, _update_log, msg)
    except Exception:
        pass

def _update_log(msg):
    activity_log.configure(state="normal")
    timestamp = time.strftime("%H:%M:%S")
    activity_log.insert("end", f"[{timestamp}] {msg}\n")
    activity_log.see("end")
    activity_log.configure(state="disabled")

def human_sleep(base_time):
    global is_running, stop_hotkey
    jitter = random.uniform(-0.03, 0.08)
    total_sleep = max(0.01, base_time + jitter)
    
    end_time = time.time() + total_sleep
    while time.time() < end_time:
        if not is_running:
            break
        try:
            if keyboard.is_pressed(stop_hotkey):
                stop_macro()
                break
        except Exception:
            pass
        time.sleep(0.05)

def run_macro():
    global is_running, bucket_hotkey, tankard_hotkey, weapon1_hotkey, weapon2_hotkey
    log_activity("Macro sequence initialized.")
    time.sleep(1)
    
    while is_running:
        keys = ['w', 'a', 's', 'd']
        random.shuffle(keys)
        
        for key in keys:
            if not is_running:
                break
            
            try:
                log_activity(f"Moving: [{key.upper()}]")
                pydirectinput.keyDown(key)
                
                if random.random() < 0.9:
                    log_activity("Action: Jump")
                    pydirectinput.press('space')
                    
                human_sleep(0.5)
                if not is_running: break
                
                log_activity("Action: Bucket")
                pydirectinput.press(bucket_hotkey)
                human_sleep(0.1)
                if not is_running: break
                
                pydirectinput.mouseDown(button='left')
                human_sleep(0.1)
                pydirectinput.mouseUp(button='left')
                human_sleep(0.2)
                
                pydirectinput.mouseDown(button='right')
                human_sleep(0.1)
                pydirectinput.mouseUp(button='right')
                human_sleep(0.2)
                if not is_running: break
                
                log_activity("Action: Tankard")
                pydirectinput.press(tankard_hotkey)
                human_sleep(0.1)
                if not is_running: break
                
                pydirectinput.mouseDown(button='left')
                human_sleep(0.1)
                pydirectinput.mouseUp(button='left')
                human_sleep(0.2)
                
                pydirectinput.mouseDown(button='right')
                human_sleep(0.1)
                pydirectinput.mouseUp(button='right')
                human_sleep(0.2)
                if not is_running: break
                
                log_activity("Action: Swap Weapons")
                pydirectinput.press(weapon1_hotkey)
                human_sleep(0.2)
                if not is_running: break
                pydirectinput.press(weapon2_hotkey)
                human_sleep(0.3)
                
            finally:
                pydirectinput.keyUp(key)
                
            if not is_running: break
            human_sleep(0.5)
            
    log_activity("Macro sequence terminated.")

def update_ui_running():
    status_banner.configure(text="[ STATUS : ACTIVE ]", text_color=START_COLOR)
    status_label_sidebar.configure(text="STATUS: ACTIVE", text_color=START_COLOR)
    ui_start_button.configure(state="disabled")
    ui_stop_button.configure(state="normal")

def update_ui_stopped():
    status_banner.configure(text="[ STATUS : STANDBY ]", text_color=STOP_COLOR)
    status_label_sidebar.configure(text="STATUS: STANDBY", text_color=STOP_COLOR)
    ui_start_button.configure(state="normal")
    ui_stop_button.configure(state="disabled")

def start_macro():
    global is_running, macro_thread
    if not is_running:
        is_running = True
        app.after(0, update_ui_running)
        macro_thread = threading.Thread(target=run_macro, daemon=True)
        macro_thread.start()

def stop_macro():
    global is_running
    if is_running:
        is_running = False
        app.after(0, update_ui_stopped)

def on_closing():
    global is_running
    is_running = False
    app.destroy()

def apply_settings():
    global start_hotkey, stop_hotkey, bucket_hotkey, tankard_hotkey, weapon1_hotkey, weapon2_hotkey
    
    start_val = start_entry.get().strip().lower()
    stop_val = stop_entry.get().strip().lower()
    bucket_val = bucket_entry.get().strip().lower()
    tankard_val = tankard_entry.get().strip().lower()
    w1_val = w1_entry.get().strip().lower()
    w2_val = w2_entry.get().strip().lower()
    
    if not start_val or not stop_val or not bucket_val or not tankard_val or not w1_val or not w2_val:
        messagebox.showerror("Error", "Keys cannot be empty!")
        return
        
    start_hotkey = start_val
    stop_hotkey = stop_val
    bucket_hotkey = bucket_val
    tankard_hotkey = tankard_val
    weapon1_hotkey = w1_val
    weapon2_hotkey = w2_val
    
    save_settings(start_hotkey, stop_hotkey, bucket_hotkey, tankard_hotkey, weapon1_hotkey, weapon2_hotkey)
    
    # Update UI bindings labels
    ui_start_button.configure(text=f"INITIALIZE ({start_hotkey.upper()})")
    ui_stop_button.configure(text=f"TERMINATE ({stop_hotkey.upper()})")
    log_activity(f"System Reconfigured. Start:[{start_hotkey.upper()}] Stop:[{stop_hotkey.upper()}]")
    
    try:
        keyboard.unhook_all()
    except:
        pass
        
    try:
        keyboard.on_press_key(start_hotkey, lambda _: start_macro())
        keyboard.on_press_key(stop_hotkey, lambda _: stop_macro())
    except Exception as e:
        messagebox.showwarning("Hotkey Error", f"Could not register hotkeys.\nError: {e}")
        
    show_dashboard()

def on_key_press(event, entry_widget):
    key = event.keysym.lower()
    key_map = {
        "control_l": "ctrl", "control_r": "ctrl",
        "alt_l": "alt", "alt_r": "alt",
        "shift_l": "shift", "shift_r": "shift",
        "return": "enter", "prior": "page up", "next": "page down",
        "escape": "esc", "caps_lock": "capslock"
    }
    key = key_map.get(key, key)
    if key == "tab":
        return "break"
        
    entry_widget.delete(0, 'end')
    entry_widget.insert(0, key)
    return "break"

# GUI Setup
app = ctk.CTk()
app.title("SoT :: AFK_CORE_v2 by ThosIYA")
app.geometry("800x550")
app.resizable(False, False)
app.configure(fg_color=BG_COLOR)

# Sidebar layout
sidebar = ctk.CTkFrame(app, width=220, corner_radius=0, fg_color=FRAME_COLOR, border_width=0)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

title_label = ctk.CTkLabel(sidebar, text="SOT AFK Macro", font=ctk.CTkFont(family=FONT_FAMILY, size=28, weight="bold"), text_color=ACCENT_COLOR)
title_label.pack(pady=(30, 0))
sub_title = ctk.CTkLabel(sidebar, text="by ThosIYA", font=ctk.CTkFont(family=FONT_FAMILY, size=12), text_color=TEXT_COLOR)
sub_title.pack(pady=(0, 40))

def show_dashboard():
    settings_frame.pack_forget()
    dashboard_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
    btn_nav_dash.configure(fg_color=ACCENT_COLOR, text_color=BG_COLOR)
    btn_nav_settings.configure(fg_color="transparent", text_color=TEXT_COLOR)

def show_settings():
    dashboard_frame.pack_forget()
    settings_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
    btn_nav_settings.configure(fg_color=ACCENT_COLOR, text_color=BG_COLOR)
    btn_nav_dash.configure(fg_color="transparent", text_color=TEXT_COLOR)

btn_nav_dash = ctk.CTkButton(sidebar, text="[ DASHBOARD ]", font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
                             command=show_dashboard, corner_radius=0, height=45, fg_color=ACCENT_COLOR, text_color=BG_COLOR, hover_color="#0891b2")
btn_nav_dash.pack(pady=5, padx=20, fill="x")

btn_nav_settings = ctk.CTkButton(sidebar, text="[ SETTINGS ]", font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
                                 command=show_settings, corner_radius=0, height=45, fg_color="transparent", text_color=TEXT_COLOR, hover_color=BG_COLOR)
btn_nav_settings.pack(pady=5, padx=20, fill="x")

status_label_sidebar = ctk.CTkLabel(sidebar, text="STATUS: STANDBY", font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"), text_color=STOP_COLOR)
status_label_sidebar.pack(side="bottom", pady=(0, 20))

copyright_label = ctk.CTkLabel(sidebar, text="© ThosIYA", font=ctk.CTkFont(family=FONT_FAMILY, size=10), text_color="gray40")
copyright_label.pack(side="bottom", pady=5)

# Main Container Frames
dashboard_frame = ctk.CTkFrame(app, fg_color=BG_COLOR, corner_radius=0)
settings_frame = ctk.CTkFrame(app, fg_color=BG_COLOR, corner_radius=0)

# --- DASHBOARD TAB ---
dash_top = ctk.CTkFrame(dashboard_frame, fg_color=FRAME_COLOR, corner_radius=0, border_width=1, border_color=ACCENT_COLOR)
dash_top.pack(fill="x", pady=(0, 20))

status_banner = ctk.CTkLabel(dash_top, text="[ STATUS : STANDBY ]", font=ctk.CTkFont(family=FONT_FAMILY, size=24, weight="bold"), text_color=STOP_COLOR)
status_banner.pack(pady=(25, 15))

btn_frame = ctk.CTkFrame(dash_top, fg_color="transparent")
btn_frame.pack(pady=(0, 25))

ui_start_button = ctk.CTkButton(btn_frame, text="INITIALIZE", font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"),
                             width=180, height=50, corner_radius=0, command=start_macro, 
                             fg_color=START_COLOR, text_color=BG_COLOR, hover_color=START_HOVER, border_width=2, border_color=START_COLOR)
ui_start_button.pack(side="left", padx=15)

ui_stop_button = ctk.CTkButton(btn_frame, text="TERMINATE", font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"),
                             width=180, height=50, corner_radius=0, command=stop_macro, 
                             fg_color=STOP_COLOR, text_color=BG_COLOR, hover_color=STOP_HOVER, border_width=2, border_color=STOP_COLOR, state="disabled")
ui_stop_button.pack(side="left", padx=15)

log_frame = ctk.CTkFrame(dashboard_frame, fg_color=FRAME_COLOR, corner_radius=0, border_width=1, border_color=ACCENT_COLOR)
log_frame.pack(fill="both", expand=True)

log_title = ctk.CTkLabel(log_frame, text=">> ACTIVITY LOG <<", font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"), text_color=ACCENT_COLOR)
log_title.pack(anchor="w", padx=15, pady=(10, 0))

activity_log = ctk.CTkTextbox(log_frame, font=ctk.CTkFont(family=FONT_FAMILY, size=13), fg_color=BG_COLOR, text_color=TEXT_COLOR, corner_radius=0, border_width=1, border_color="#27272a")
activity_log.pack(fill="both", expand=True, padx=15, pady=15)
activity_log.configure(state="disabled")

# --- SETTINGS TAB ---
settings_title = ctk.CTkLabel(settings_frame, text=">> KEYBIND CONFIGURATION <<", font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"), text_color=ACCENT_COLOR)
settings_title.pack(pady=(0, 20), anchor="w")

settings_grid = ctk.CTkFrame(settings_frame, fg_color=FRAME_COLOR, corner_radius=0, border_width=1, border_color=ACCENT_COLOR)
settings_grid.pack(fill="x", pady=0)

def create_input_row(parent, label_text, default_val):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(pady=10, fill="x", padx=40)
    lbl = ctk.CTkLabel(frame, text=label_text, width=150, anchor="w", font=ctk.CTkFont(family=FONT_FAMILY, size=14), text_color=ACCENT_COLOR)
    lbl.pack(side="left")
    entry = ctk.CTkEntry(frame, width=150, font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"), 
                         fg_color=BG_COLOR, border_color=ACCENT_COLOR, text_color=TEXT_COLOR, corner_radius=0, justify="center")
    entry.insert(0, default_val)
    entry.pack(side="right")
    entry.bind("<Key>", lambda e, w=entry: on_key_press(e, w))
    return entry

start_entry = create_input_row(settings_grid, "[START_KEY]:", "f9")
stop_entry = create_input_row(settings_grid, "[STOP_KEY]:", "f10")
bucket_entry = create_input_row(settings_grid, "[BUCKET_KEY]:", "b")
tankard_entry = create_input_row(settings_grid, "[TANKARD_KEY]:", "9")
w1_entry = create_input_row(settings_grid, "[WEAPON_1]:", "1")
w2_entry = create_input_row(settings_grid, "[WEAPON_2]:", "2")

apply_btn = ctk.CTkButton(settings_frame, text="APPLY & SAVE", font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"),
                          fg_color=ACCENT_COLOR, text_color=BG_COLOR, hover_color="#0891b2", corner_radius=0, 
                          border_width=2, border_color=ACCENT_COLOR, height=50, command=apply_settings)
apply_btn.pack(pady=30, fill="x", padx=40)

# Init
settings = load_settings()
if settings:
    start_hotkey = settings.get("start_key", "f9")
    stop_hotkey = settings.get("stop_key", "f10")
    bucket_hotkey = settings.get("bucket_key", "b")
    tankard_hotkey = settings.get("tankard_key", "9")
    weapon1_hotkey = settings.get("weapon1_key", "1")
    weapon2_hotkey = settings.get("weapon2_key", "2")
    
    start_entry.delete(0, 'end')
    start_entry.insert(0, start_hotkey)
    stop_entry.delete(0, 'end')
    stop_entry.insert(0, stop_hotkey)
    bucket_entry.delete(0, 'end')
    bucket_entry.insert(0, bucket_hotkey)
    tankard_entry.delete(0, 'end')
    tankard_entry.insert(0, tankard_hotkey)
    w1_entry.delete(0, 'end')
    w1_entry.insert(0, weapon1_hotkey)
    w2_entry.delete(0, 'end')
    w2_entry.insert(0, weapon2_hotkey)
    
    apply_settings()
else:
    # First time, show settings frame
    show_settings()

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
