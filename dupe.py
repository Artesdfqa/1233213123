import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("500x540")
app.title("NearKiller")
app.wm_attributes("-topmost", True)
app.wm_attributes("-alpha", 0.95)

button_color = "#8a2be2"
active_color = "#a259ff"
enabled_color = "#d3a9ff"  # светлый фиолетовый

selected_tab = ctk.StringVar(value="Combat")
feature_states = {}

# Верхняя панель вкладок — кнопки маленькие по высоте, длинные по ширине
frame_tabs = ctk.CTkFrame(app, fg_color="transparent")
frame_tabs.pack(pady=15)

def switch_tab(name):
    selected_tab.set(name)
    update_tabs()
    show_tab(name)

tabs = {}
tab_names = ["Combat", "Visual", "List", "Movement", "Others"]

for tab in tab_names:
    btn = ctk.CTkButton(frame_tabs, text=tab, width=90, height=25,
                        fg_color=button_color,
                        hover_color=active_color,
                        command=lambda t=tab: switch_tab(t))
    btn.pack(side="left", padx=5)
    tabs[tab] = btn

def update_tabs():
    for name, btn in tabs.items():
        if selected_tab.get() == name:
            btn.configure(fg_color=active_color)
        else:
            btn.configure(fg_color=button_color)

# Основной фрейм с двумя колонками: слева контент, справа панель с кнопками
frame_content = ctk.CTkFrame(app)
frame_content.pack(fill="both", expand=True, padx=20, pady=10)

# Левая часть — контент
frame_main = ctk.CTkFrame(frame_content, corner_radius=15)
frame_main.pack(side="left", fill="both", expand=True, padx=(0, 10))

# Правая часть — панель с кнопками
frame_right = ctk.CTkFrame(frame_content, fg_color="transparent", width=140)
frame_right.pack(side="right", fill="y")

frame_buttons = ctk.CTkFrame(frame_right, fg_color="transparent")
frame_buttons.pack(fill="both", expand=True, pady=5, padx=5)

def clear_frame():
    for widget in frame_main.winfo_children():
        widget.destroy()
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
    clear_frame()
    
    features = []
    if tab_name == "Combat":
        features = ["Aimbot", "Magic Bullet"]
    elif tab_name == "Visual":
        features = ["ESP", "ESP Storage"]
    elif tab_name == "List":
        features = ["Player List", "Chest Finder", "Mob Radar"]
    elif tab_name == "Movement":
        features = ["Speed Hack", "NoClip", "Fly"]
    elif tab_name == "Others":
        btn = ctk.CTkButton(frame_buttons, text="x2 Dupe Resource", width=130, height=25,
                            fg_color=button_color, hover_color=active_color,
                            command=fake_dupe)
        btn.pack(pady=3, fill="x")
        btn.bind("<Button-3>", lambda e: on_right_click(e, "x2 Dupe Resource"))
        return

    for name in features:
        btn = ctk.CTkButton(frame_buttons, text=f"{name} [OFF]",
                            fg_color=button_color,
                            hover_color=active_color,
                            height=25,
                            width=130,
                            anchor="w")
        btn.pack(pady=3, fill="x")
        btn.configure(command=lambda n=name, b=btn: toggle_feature(n, b))
        btn.bind("<Button-3>", lambda e, n=name: on_right_click(e, n))
        feature_states[name] = False

def fake_dupe():
    popup = ctk.CTkToplevel(app)
    popup.title("x2 Dupe Resource")
    popup.geometry("300x100")
    ctk.CTkLabel(popup, text="Ресурсы теперь визуально удвоены!\n(только на экране)").pack(pady=20)
    popup.wm_attributes("-topmost", True)

switch_tab("Combat")
app.mainloop()
