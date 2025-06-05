import tkinter as tk
import customtkinter as ctk
import json
import os

SETTINGS_FILE = "settings.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Главное окно
app = ctk.CTk()
app.title("Minecraft Style Menu")
app.geometry("400x400")
app.resizable(False, False)
app.configure(bg="#2b2b2b")

# Фоновый круг для 360-градусного аимбота
screen = tk.Tk()
screen.withdraw()
screen_width = screen.winfo_screenwidth()
screen_height = screen.winfo_screenheight()

circle_overlay = tk.Toplevel()
circle_overlay.overrideredirect(True)
circle_overlay.attributes("-topmost", True)
circle_overlay.attributes("-transparentcolor", "white")
circle_overlay.config(bg="white")

circle_diameter = 200
pos_x = (screen_width - circle_diameter) // 2
pos_y = (screen_height - circle_diameter) // 2
circle_overlay.geometry(f"{circle_diameter}x{circle_diameter}+{pos_x}+{pos_y}")

canvas = tk.Canvas(circle_overlay, width=circle_diameter, height=circle_diameter, bg="white", highlightthickness=0)
canvas.pack()
canvas.create_oval(2, 2, circle_diameter - 2, circle_diameter - 2, outline="red", width=3)

# Функции для UI
font_settings = ("Consolas", 13)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

settings = load_settings()

# Фейковые опции
options = ["ESP", "X-Ray", "Fullbright", "Chest Finder", "Fly", "Speed Hack"]
option_vars = {}

for opt in options:
    var = tk.BooleanVar(value=settings.get(opt, False))
    chk = ctk.CTkCheckBox(app, text=opt, variable=var, font=font_settings)
    chk.pack(pady=5)
    option_vars[opt] = var

def save_and_exit():
    for key, var in option_vars.items():
        settings[key] = var.get()
    save_settings(settings)
    app.destroy()
    circle_overlay.destroy()

exit_btn = ctk.CTkButton(app, text="Save & Exit", command=save_and_exit, font=font_settings)
exit_btn.pack(pady=20)

app.mainloop()
