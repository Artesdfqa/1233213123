import customtkinter as ctk

# Настройки интерфейса
ctk.set_appearance_mode("dark")  # Темная тема

# Основной класс приложения
class NearKillerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NearKiller")
        self.geometry("400x300")
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.9)  # Полупрозрачность

        self.active_tab = None

        # Основной фрейм
        self.main_frame = ctk.CTkFrame(self, fg_color="#1e1e2e")
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Панель вкладок
        self.tab_frame = ctk.CTkFrame(self.main_frame, fg_color="#1e1e2e")
        self.tab_frame.pack(side="top", fill="x")

        # Область меню
        self.menu_frame = ctk.CTkFrame(self.main_frame, fg_color="#1e1e2e")
        self.menu_frame.pack(side="top", fill="both", expand=True, pady=10)

        # Вкладки и их содержимое
        self.tabs = {
            "Combat": ["Aimbot", "Magic Bullet"],
            "Visual": ["ESP", "ESP Storage"],
            "List": ["Player List", "Item List"],
            "Movement": ["Speed Hack", "Teleport"]
        }

        self.tab_buttons = {}

        for tab in self.tabs:
            btn = ctk.CTkButton(
                self.tab_frame,
                text=tab,
                command=lambda t=tab: self.show_menu(t),
                fg_color="transparent",
                text_color="#ffffff",
                hover_color="#9933ff",
                border_color="#8000ff",
                border_width=2
            )
            btn.pack(side="left", padx=5, pady=5)
            self.tab_buttons[tab] = btn

        self.show_menu("Combat")  # По умолчанию открыть Combat

    def show_menu(self, tab_name):
        for t, btn in self.tab_buttons.items():
            if t == tab_name:
                btn.configure(fg_color="#8000ff", text_color="#ffffff")
            else:
                btn.configure(fg_color="transparent", text_color="#ffffff")

        # Очистка предыдущих виджетов меню
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        # Отображение новых пунктов меню
        for item in self.tabs[tab_name]:
            checkbox = ctk.CTkCheckBox(
                self.menu_frame,
                text=item,
                text_color="#ffffff",
                fg_color="#8000ff",
                hover_color="#9933ff",
                border_color="#8000ff",
                checkmark_color="#ffffff"
            )
            checkbox.pack(anchor="w", padx=15, pady=5)

# Запуск
if __name__ == "__main__":
    app = NearKillerApp()
    app.mainloop()
