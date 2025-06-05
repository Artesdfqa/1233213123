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
enabled_color = "#d3a9ff"  # светлый фиолетовый, заметнее

selected_tab = ctk.StringVar(value="Combat")
feature_states = {}  # для отслеживания состояния

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

frame_main = ctk.CTkFrame(app, corner_radius=15)
frame_main.pack(fill="both", expand=True, padx=20, pady=10)

def clear_frame():
    for widget in frame_main.winfo_children():
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
    
    if tab_name == "Combat":
        ctk.CTkLabel(frame_main, text="⚔ Combat", font=("Arial", 18)).pack(pady=10)
        make_feature_button("Aimbot")
        make_feature_button("Magic Bullet")
    
    elif tab_name == "Visual":
        ctk.CTkLabel(frame_main, text="👁 Visual", font=("Arial", 18)).pack(pady=10)
        make_feature_button("ESP")
        make_feature_button("ESP Storage")
    
    elif tab_name == "List":
        ctk.CTkLabel(frame_main, text="📋 List", font=("Arial", 18)).pack(pady=10)
        make_feature_button("Player List")
        make_feature_button("Chest Finder")
        make_feature_button("Mob Radar")
    
    elif tab_name == "Movement":
        ctk.CTkLabel(frame_main, text="🏃 Movement", font=("Arial", 18)).pack(pady=10)
        make_feature_button("Speed Hack")
        make_feature_button("NoClip")
        make_feature_button("Fly")
    
    elif tab_name == "Others":
        ctk.CTkLabel(frame_main, text="⚙ Others", font=("Arial", 18)).pack(pady=10)
        ctk.CTkButton(frame_main, text="x2 Dupe Resource", command=fake_dupe).pack(pady=5)

def make_feature_button(name):
    btn = ctk.CTkButton(frame_main, text=f"{name} [OFF]",
                        fg_color=button_color,
                        hover_color=active_color,
                        command=lambda: toggle_feature(name, btn))
    btn.pack(pady=5)
    feature_states[name] = False

def fake_dupe():
    popup = ctk.CTkToplevel(app)
    popup.title("x2 Dupe Resource")
    popup.geometry("300x100")
    ctk.CTkLabel(popup, text="Ресурсы теперь визуально удвоены!\n(только на экране)").pack(pady=20)
    popup.wm_attributes("-topmost", True)

switch_tab("Combat")
app.mainloop()
