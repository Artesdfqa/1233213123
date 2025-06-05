import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("NearKiller")
app.wm_attributes("-topmost", True)
app.wm_attributes("-alpha", 0.95)

# Получаем размеры экрана
root_tk = tk.Tk()
screen_width = root_tk.winfo_screenwidth()
screen_height = root_tk.winfo_screenheight()
root_tk.destroy()

# Размеры окна ~1/4 экрана, немного меньше (90%)
win_width = int(screen_width / 4 * 0.9)
win_height = int(screen_height / 4 * 0.9)

# Разместим окно в правом нижнем углу
pos_x = screen_width - win_width - 20  # отступ 20px от края экрана справа
pos_y = screen_height - win_height - 50  # отступ 50px снизу

app.geometry(f"{win_width}x{win_height}+{pos_x}+{pos_y}")

button_color = "#8a2be2"
active_color = "#a259ff"
enabled_color = "#d3a9ff"  # светлый фиолетовый

selected_tab = ctk.StringVar(value="Combat")
feature_states = {}

# Верхняя панель вкладок
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

# Панель с кнопками функций под вкладками
frame_buttons = ctk.CTkFrame(app, fg_color="transparent")
frame_buttons.pack(fill="both", expand=True, pady=10, padx=10)

def clear_buttons():
    for widget in frame_buttons.winfo_children():
        widget.destroy()

def toggle_feature(name, button):
    current = feature_states.get(name, False)
    feature_states[name] = not current
    if not current:
        button.configure(fg_color=enabled_color, text=f"{name} [ON]")
    else:
        button.configure(fg_color=button_color, text=f"{name} [OFF]")

def on_right_click(event, feature_name):
    menu = tk.Menu(app, tearoff=0)
    menu.add_command(label=f"Настроить {feature_name}", command=lambda: open_settings(feature_name))
    menu.tk_popup(event.x_root, event.y_root)

def open_settings(feature_name):
    popup = ctk.CTkToplevel(app)
    popup.title(f"Настройки {feature_name}")
    popup.geometry("300x150")
    ctk.CTkLabel(popup, text=f"Здесь можно настроить {feature_name}").pack(pady=20)
    popup.wm_attributes("-topmost", True)

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
        btn = ctk.CTkButton(frame_buttons, text=f"{name} [OFF]",
                            fg_color=button_color,
                            hover_color=active_color,
                            height=25,
                            width=win_width - 40,
                            anchor="w")
        btn.pack(pady=5, fill="x")
        btn.configure(command=lambda n=name, b=btn: toggle_feature(n, b))
        btn.bind("<Button-3>", lambda e, n=name: on_right_click(e, n))
        feature_states[name] = False

switch_tab("Combat")
app.mainloop()
