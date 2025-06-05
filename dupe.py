import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("420x540")
app.title("NearKiller")
app.wm_attributes("-topmost", True)
app.wm_attributes("-alpha", 0.95)

button_color = "#8a2be2"
active_color = "#a259ff"
enabled_color = "#d3a9ff"  # светлый фиолетовый

selected_tab = ctk.StringVar(value="Combat")
feature_states = {}  # для отслеживания состояния

# Верхняя панель вкладок
frame_tabs = ctk.CTkFrame(app, fg_color="transparent")
frame_tabs.pack(pady=15)

def switch_tab(name):
    selected_tab.set(name)
    update_tabs()
    show_tab(name)

tabs = {}
tab_names = ["Combat", "Visual", "List", "Movement", "Others"]

for tab in tab_names:
    btn = ctk.CTkButton(frame_tabs, text=tab, width=75, height=32,
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

# Основной контент (текст/информация)
frame_main = ctk.CTkFrame(app, corner_radius=15)
frame_main.pack(fill="both", expand=True, padx=20, pady=(10, 60))  # Отступ снизу больше чтобы не было перекрытия

# Нижняя панель с кнопками функций (в ряд)
frame_buttons = ctk.CTkFrame(app, fg_color="transparent")
frame_buttons.pack(side="bottom", fill="x", padx=20, pady=10)

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

def show_tab(tab_name):
    clear_frame()
    ctk.CTkLabel(frame_main, text=f"=== {tab_name} ===", font=("Arial", 20)).pack(pady=10)
    
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
        # В Others кнопка не входит в общий список функций
        btn = ctk.CTkButton(frame_buttons, text="x2 Dupe Resource", command=fake_dupe)
        btn.pack(side="left", padx=5)
        return

    # Создаём кнопки функций горизонтально
    for name in features:
        btn = ctk.CTkButton(frame_buttons, text=f"{name} [OFF]",
                            fg_color=button_color,
                            hover_color=active_color,
                            width=110,
                            command=lambda n=name, b=None: None)  # заглушка, ниже заменим
        btn.pack(side="left", padx=5)
        # Переписываем команду с правильной ссылкой на кнопку
        btn.configure(command=lambda n=name, b=btn: toggle_feature(n, b))
        feature_states[name] = False

def fake_dupe():
    popup = ctk.CTkToplevel(app)
    popup.title("x2 Dupe Resource")
    popup.geometry("300x100")
    ctk.CTkLabel(popup, text="Ресурсы теперь визуально удвоены!\n(только на экране)").pack(pady=20)
    popup.wm_attributes("-topmost", True)

switch_tab("Combat")
app.mainloop()
