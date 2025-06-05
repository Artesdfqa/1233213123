import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import json
import os

SETTINGS_FILE = "settings.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("NearKiller")
app.wm_attributes("-topmost", True)
app.wm_attributes("-alpha", 0.95)

root_tk = tk.Tk()
screen_width = root_tk.winfo_screenwidth()
screen_height = root_tk.winfo_screenheight()
root_tk.destroy()

win_width = int(screen_width / 4 * 0.9)
win_height = int(screen_height / 4 * 0.9)
pos_x = screen_width - win_width - 20
pos_y = screen_height - win_height - 50
app.geometry(f"{win_width}x{win_height}+{pos_x}+{pos_y}")

button_color = "#4c9141"
active_color = "#6bb46c"
enabled_color = "#b9e2b4"

selected_tab = ctk.StringVar(value="Combat")
feature_states = {}
feature_settings = {}

# Load settings
def load_settings():
    global feature_settings
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                feature_settings = json.load(f)
        except Exception:
            feature_settings = {}
    else:
        feature_settings = {}

# Save settings
def save_settings():
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(feature_settings, f, indent=2)

load_settings()

frame_tabs = ctk.CTkFrame(app, fg_color="transparent")
frame_tabs.pack(pady=10)

def switch_tab(name):
    selected_tab.set(name)
    update_tabs()
    update_buttons_text()

tabs = {}
tab_names = ["Combat", "Visual", "List", "Movement", "Others"]

for tab in tab_names:
    btn = ctk.CTkButton(frame_tabs, text=tab, width=win_width // 6, height=25,
                        fg_color=button_color, hover_color=active_color,
                        command=lambda t=tab: switch_tab(t))
    btn.pack(side="left", padx=3)
    tabs[tab] = btn

def update_tabs():
    for name, btn in tabs.items():
        if selected_tab.get() == name:
            btn.configure(fg_color=active_color)
        else:
            btn.configure(fg_color=button_color)

frame_buttons = ctk.CTkFrame(app, fg_color="transparent")
frame_buttons.pack(fill="both", expand=True, pady=10, padx=10)

def clear_buttons():
    for widget in frame_buttons.winfo_children():
        widget.destroy()

def get_feature_display_text(name):
    state = feature_states.get(name, False)
    on_off = "[ON]" if state else "[OFF]"
    sett = feature_settings.get(name, {})
    return f"{name} {on_off}"

def toggle_feature(name, button):
    current = feature_states.get(name, False)
    feature_states[name] = not current
    button.configure(fg_color=enabled_color if not current else button_color,
                     text=get_feature_display_text(name))
    save_settings()
    update_overlay_visibility()

def on_right_click(event, feature_name):
    menu = tk.Menu(app, tearoff=0)
    menu.add_command(label=f"Настроить {feature_name}", command=lambda: open_settings(feature_name))
    menu.tk_popup(event.x_root, event.y_root)

def open_settings(feature_name):
    popup = ctk.CTkToplevel(app)
    popup.title(f"Настройки {feature_name}")
    popup.geometry("320x250")
    popup.wm_attributes("-topmost", True)
    vars_dict = {}

    def save_and_close():
        save_settings()
        update_buttons_text()
        popup.destroy()

    btn_save = ctk.CTkButton(popup, text="Сохранить", command=save_and_close)
    btn_save.pack(pady=10)

def update_buttons_text():
    clear_buttons()
    current_tab = selected_tab.get()
    features_by_tab = {
        "Combat": ["Aimbot", "Magic Bullet"],
        "Visual": ["ESP", "ESP Storage"],
        "List": ["Player List", "Chest Finder", "Mob Radar"],
        "Movement": ["Speed Hack", "NoClip", "Fly"],
        "Others": ["x2 Dupe Resource"]
    }

    for feature_name in features_by_tab.get(current_tab, []):
        btn = ctk.CTkButton(frame_buttons, text=get_feature_display_text(feature_name), fg_color=button_color,
                            hover_color=active_color, command=lambda n=feature_name, b=None: toggle_feature(n, b))
        btn.pack(fill="x", pady=5)
        btn.configure(command=lambda n=feature_name, b=btn: toggle_feature(n, b))
        btn.bind("<Button-3>", lambda e, n=feature_name: on_right_click(e, n))

switch_tab(selected_tab.get())

# Overlay crosshair
crosshair_size = 40
center_x = (screen_width - crosshair_size) // 2
center_y = (screen_height - crosshair_size) // 2

overlay = tk.Toplevel()
overlay.overrideredirect(True)
overlay.attributes("-topmost", True)
overlay.attributes("-transparentcolor", "white")
overlay.geometry(f"{crosshair_size}x{crosshair_size}+{center_x}+{center_y}")
overlay.config(bg="white")

canvas = tk.Canvas(overlay, width=crosshair_size, height=crosshair_size, bg="white", highlightthickness=0)
canvas.pack()
center = crosshair_size // 2
canvas.create_line(center, 0, center, crosshair_size, fill="red", width=2)
canvas.create_line(0, center, crosshair_size, center, fill="red", width=2)

app.mainloop()
