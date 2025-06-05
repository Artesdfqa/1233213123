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
    btn_save.pack(pady=15)

