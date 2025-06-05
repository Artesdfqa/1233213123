import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")  # Более подходящий стиль под Minecraft

app = ctk.CTk()
app.title("NearKiller Minecraft Edition")
app.geometry("600x400")
app.resizable(False, False)

# Заголовок как в Minecraft
title_label = ctk.CTkLabel(app, text="NearKiller", font=("Minecraft", 28, "bold"), text_color="#00ff00")
title_label.pack(pady=20)

# Панель с вкладками
notebook = ttk.Notebook(app)
notebook.pack(expand=True, fill='both', padx=10, pady=10)

style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook', background='#2e2e2e', borderwidth=0)
style.configure('TNotebook.Tab', background='#1e1e1e', foreground='white', font=('Minecraft', 10))
style.map('TNotebook.Tab', background=[('selected', '#3e3e3e')])

# Создание вкладок
categories = ["Combat", "Visual", "List", "Movement", "Others"]
tabs = {}

for category in categories:
    frame = ttk.Frame(notebook, style='TFrame')
    notebook.add(frame, text=category)
    tabs[category] = frame

# Пример кнопок как в Minecraft GUI
minecraft_font = ("Minecraft", 10)

def add_feature_button(parent, text):
    btn = ctk.CTkButton(parent, text=text, font=minecraft_font, fg_color="#4caf50",
                        hover_color="#45a049", corner_radius=5, height=30)
    btn.pack(pady=5, padx=10, fill="x")

# Добавление примеров кнопок
add_feature_button(tabs["Combat"], "Aimbot [OFF]")
add_feature_button(tabs["Combat"], "Magic Bullet [OFF]")
add_feature_button(tabs["Visual"], "ESP [OFF]")
add_feature_button(tabs["List"], "Player List [OFF]")
add_feature_button(tabs["Movement"], "Speed Hack [OFF]")
add_feature_button(tabs["Others"], "x2 Dupe Resource [OFF]")

app.mainloop()
