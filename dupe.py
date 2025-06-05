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

button_color = "#8a2be2"
active_color = "#a259ff"
enabled_color = "#d3a9ff"

selected_tab = ctk.StringVar(value="Combat")
feature_states = {}
feature_settings = {}

# Загрузка настроек
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

# Сохранение настроек
def save_settings():
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(feature_settings, f, indent=2)

load_settings()

frame_tabs = ctk.CTkFrame(app, fg_color="transparent")
frame_tabs.pack(pady=10)

def switch_tab(name):
    selected_tab.set(name)
    update_tabs()
    show_tab(name)

tabs = {}
tab_names = ["Combat", "Visual", "List", "Movement", "Others"]

for tab in tab_names:
    btn = ctk.CTkButton(frame_tabs, text=tab, width=win_width // 6, height=25,
                        fg_color=button_color,
                        hover_color=active_color,
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

    if name in ["Aimbot", "Magic Bullet"]:
        fov = sett.get("fov", 90)
        dist = sett.get("distance", 100)
        return f"{name} {on_off} FOV: {fov} Dst: {dist}"
    elif name == "ESP":
        opacity = sett.get("opacity", 70)
        return f"{name} {on_off} Opacity: {opacity}%"
    elif name == "ESP Storage":
        opacity = sett.get("opacity", 50)
        return f"{name} {on_off} Opacity: {opacity}%"
    elif name == "Player List":
        count = sett.get("count", 10)
        return f"{name} {on_off} Count: {count}"
    elif name == "Chest Finder":
        radius = sett.get("radius", 100)
        return f"{name} {on_off} Radius: {radius}"
    elif name == "Mob Radar":
        radius = sett.get("radius", 100)
        return f"{name} {on_off} Radius: {radius}"
    elif name == "Speed Hack":
        speed = sett.get("speed", 2)
        return f"{name} {on_off} Speed: {speed}x"
    elif name == "NoClip":
        enabled = sett.get("enabled", False)
        return f"{name} {on_off} Enabled: {'Yes' if enabled else 'No'}"
    elif name == "Fly":
        speed = sett.get("speed", 1)
        return f"{name} {on_off} Speed: {speed}x"
    elif name == "x2 Dupe Resource":
        multiplier = sett.get("multiplier", 2)
        return f"{name} {on_off} x{multiplier}"
    else:
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

    if feature_name not in feature_settings:
        defaults = {
            "Aimbot": {"fov": 90, "distance": 100},
            "Magic Bullet": {"fov": 90, "distance": 100},
            "ESP": {"opacity": 70},
            "ESP Storage": {"opacity": 50},
            "Player List": {"count": 10},
            "Chest Finder": {"radius": 100},
            "Mob Radar": {"radius": 100},
            "Speed Hack": {"speed": 2},
            "NoClip": {"enabled": False},
            "Fly": {"speed": 1},
            "x2 Dupe Resource": {"multiplier": 2},
        }
        feature_settings[feature_name] = defaults.get(feature_name, {})

    sett = feature_settings[feature_name]

    def create_label_spinbox(parent, text, key, from_, to, increment=1, is_bool=False):
        ctk.CTkLabel(parent, text=text).pack(pady=(10, 0))
        if is_bool:
            var = tk.BooleanVar(value=sett.get(key, False))
            chk = ctk.CTkCheckBox(parent, text="", variable=var)
            chk.pack()
            return var
        else:
            var = tk.IntVar(value=sett.get(key, from_))
            spin = ttk.Spinbox(parent, from_=from_, to=to, increment=increment, textvariable=var, width=10)
            spin.pack()
            return var

    vars_dict = {}

    if feature_name in ["Aimbot", "Magic Bullet"]:
        vars_dict["fov"] = create_label_spinbox(popup, "FOV (угол):", "fov", 10, 180, 1)
        vars_dict["distance"] = create_label_spinbox(popup, "Distance (дальность):", "distance", 10, 500, 5)
    elif feature_name in ["ESP", "ESP Storage"]:
        vars_dict["opacity"] = create_label_spinbox(popup, "Opacity (%):", "opacity", 0, 100, 5)
    elif feature_name == "Player List":
        vars_dict["count"] = create_label_spinbox(popup, "Count:", "count", 1, 100, 1)
    elif feature_name in ["Chest Finder", "Mob Radar"]:
        vars_dict["radius"] = create_label_spinbox(popup, "Radius:", "radius", 10, 500, 10)
    elif feature_name == "Speed Hack":
        vars_dict["speed"] = create_label_spinbox(popup, "Speed multiplier:", "speed", 1, 10, 1)
    elif feature_name == "NoClip":
        vars_dict["enabled"] = create_label_spinbox(popup, "Enabled:", "enabled", 0, 1, 1, is_bool=True)
    elif feature_name == "Fly":
        vars_dict["speed"] = create_label_spinbox(popup, "Speed multiplier:", "speed", 1, 10, 1)
    elif feature_name == "x2 Dupe Resource":
        vars_dict["multiplier"] = create_label_spinbox(popup, "Multiplier:", "multiplier", 1, 10, 1)

    def save_and_close():
        for key, var in vars_dict.items():
            if isinstance(var, tk.BooleanVar):
                feature_settings[feature_name][key] = var.get()
            else:
                try:
                    feature_settings[feature_name][key] = int(var.get())
                except Exception:
                    pass
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
        # Нужно чтобы toggle_feature получил кнопку, передадим через замыкание:
        btn.configure(command=lambda n=feature_name, b=btn: toggle_feature(n, b))
        btn.bind("<Button-3>", lambda e, n=feature_name: on_right_click(e, n))

switch_tab(selected_tab.get())

# --- Оверлей с красным кругом ---

circle_diameter = 100
overlay = tk.Toplevel()
overlay.overrideredirect(True)  # Без рамок
overlay.attributes("-topmost", True)
pos_x = (screen_width - circle_diameter) // 2
pos_y = (screen_height - circle_diameter) // 2
overlay.geometry(f"{circle_diameter}x{circle_diameter}+{pos_x}+{pos_y}")
overlay.attributes("-transparentcolor", "white")
overlay.config(bg="white")

canvas = tk.Canvas(overlay, width=circle_diameter, height=circle_d
