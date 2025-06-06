import customtkinter as ctk
import tkinter as tk
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

# Загрузка настроек из файла
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

# Сохранение настроек в файл
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
    # Для Aimbot и Magic Bullet добавляем FOV и Distance
    if name in ["Aimbot", "Magic Bullet"]:
        sett = feature_settings.get(name, {})
        fov = sett.get("fov", 90)
        dist = sett.get("distance", 100)
        return f"{name} {on_off} FOV: {fov} Dst: {dist}"
    else:
        return f"{name} {on_off}"

def toggle_feature(name, button):
    current = feature_states.get(name, False)
    feature_states[name] = not current
    button.configure(fg_color=enabled_color if not current else button_color,
                     text=get_feature_display_text(name))
    save_settings()

def on_right_click(event, feature_name):
    menu = tk.Menu(app, tearoff=0)
    menu.add_command(label=f"Настроить {feature_name}", command=lambda: open_settings(feature_name))
    menu.tk_popup(event.x_root, event.y_root)

def open_settings(feature_name):
    popup = ctk.CTkToplevel(app)
    popup.title(f"Настройки {feature_name}")
    popup.geometry("300x200")
    popup.wm_attributes("-topmost", True)

    if feature_name not in feature_settings:
        feature_settings[feature_name] = {"fov": 90, "distance": 100}

    sett = feature_settings[feature_name]

    def save_and_close():
        try:
            fov_val = int(entry_fov.get())
            dist_val = int(entry_distance.get())
            if fov_val < 0 or dist_val < 0:
                raise ValueError
        except ValueError:
            error_label.configure(text="Введите положительные числа!")
            return
        sett["fov"] = fov_val
        sett["distance"] = dist_val
        save_settings()
        update_buttons_text()
        popup.destroy()

    ctk.CTkLabel(popup, text="FOV (угол):").pack(pady=(15, 0))
    entry_fov = ctk.CTkEntry(popup)
    entry_fov.pack(pady=5)
    entry_fov.insert(0, str(sett.get("fov", 90)))

    ctk.CTkLabel(popup, text="Distance (дальность):").pack(pady=(15, 0))
    entry_distance = ctk.CTkEntry(popup)
    entry_distance.pack(pady=5)
    entry_distance.insert(0, str(sett.get("distance", 100)))

    error_label = ctk.CTkLabel(popup, text="", text_color="red")
    error_label.pack()

    btn_save = ctk.CTkButton(popup, text="Сохранить", command=save_and_close)
    btn_save.pack(pady=15)

def update_buttons_text():
    for widget in frame_buttons.winfo_children():
        text = widget.cget("text")
        # Получаем имя функции без статуса и параметров
        name = text.split()[0]
        if name in feature_states:
            widget.configure(text=get_feature_display_text(name))

def show_tab(tab_name):
    clear_buttons()
    if tab_name == "Combat":
        features = ["Aimbot", "Magic Bullet"]
    elif tab_name == "Visual":
        features = ["ESP", "ESP Storage"]
    elif tab_name == "List":
        features = ["Player List", "Chest Finder", "Mob Radar"]
    elif tab_name == "Movement":
        features = ["Speed Hack", "NoClip", "Fly"]
    elif tab_name == "Others":
        features = ["x2 Dupe Resource"]
    else:
        features = []

    for name in features:
        btn = ctk.CTkButton(frame_buttons, text=get_feature_display_text(name),
                            fg_color=button_color,
                            hover_color=active_color,
                            height=25,
                            width=win_width - 40,
                            anchor="w")
        btn.pack(pady=5, fill="x")
        btn.configure(command=lambda n=name, b=btn: toggle_feature(n, b))
        btn.bind("<Button-3>", lambda e, n=name: on_right_click(e, n))
        if name not in feature_states:
            feature_states[name] = False

switch_tab("Combat")
app.mainloop()
