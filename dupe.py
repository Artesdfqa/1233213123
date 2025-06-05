import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("400x500")
app.title("NearKiller")
app.wm_attributes("-topmost", True)
app.wm_attributes("-alpha", 0.95)

# Стили
button_color = "#8a2be2"  # фиолетовый
active_color = "#a259ff"

selected_tab = ctk.StringVar(value="None")

# Верхнее меню
frame_top = ctk.CTkFrame(app)
frame_top.pack(pady=10)

def select_tab(name):
    selected_tab.set(name)
    update_tabs()

def update_tabs():
    for name, button in tabs.items():
        if selected_tab.get() == name:
            button.configure(fg_color=active_color)
        else:
            button.configure(fg_color=button_color)

tabs = {}
tab_names = ["Combat", "Visual", "List", "Movement", "Others"]
for tab in tab_names:
    tabs[tab] = ctk.CTkButton(frame_top, text=tab, command=lambda t=tab: select_tab(t), fg_color=button_color, width=70)
    tabs[tab].pack(side="left", padx=2)

# Контент вкладок
frame_content = ctk.CTkFrame(app)
frame_content.pack(fill="both", expand=True, pady=10)

# Все вкладки в словаре
tab_frames = {}

def clear_frame():
    for widget in frame_content.winfo_children():
        widget.destroy()

def show_tab(tab_name):
    clear_frame()
    if tab_name == "Combat":
        ctk.CTkLabel(frame_content, text="Combat Options").pack()
        ctk.CTkButton(frame_content, text="Aimbot").pack(pady=5)
        ctk.CTkButton(frame_content, text="Magic Bullet").pack(pady=5)
    elif tab_name == "Visual":
        ctk.CTkLabel(frame_content, text="Visual Options").pack()
        ctk.CTkButton(frame_content, text="ESP").pack(pady=5)
        ctk.CTkButton(frame_content, text="ESP Storage").pack(pady=5)
    elif tab_name == "Others":
        ctk.CTkLabel(frame_content, text="Other Features").pack()
        ctk.CTkButton(frame_content, text="x2 Dupe Resource", command=fake_dupe).pack(pady=5)
    else:
        ctk.CTkLabel(frame_content, text=f"{tab_name} content coming soon...").pack()

# Симуляция визуального x2 дюпа
def fake_dupe():
    popup = ctk.CTkToplevel(app)
    popup.title("x2 Dupe Resource")
    popup.geometry("300x100")
    ctk.CTkLabel(popup, text="Ресурсы теперь визуально удвоены!\n(только на экране)").pack(pady=20)
    popup.wm_attributes("-topmost", True)

# Обновление при переключении
def on_tab_change(*args):
    show_tab(selected_tab.get())

selected_tab.trace_add("write", on_tab_change)
select_tab("Combat")  # стартовая вкладка

app.mainloop()
