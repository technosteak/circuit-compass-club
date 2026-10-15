import os
import time
import subprocess
import requests

# Настройки Telegram (при необходимости обнови токен/айди)
BOT_TOKEN = "8915738942:AAGQYQPCYX8fRAMvMb4gKALpT0Ot82pIGrI"
ADMIN_ID = 5199807862
REPO_DIR = "/var/www/technosteak"

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": ADMIN_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except:
        pass

def save_and_build():
    try:
        # Твоя основная логика сборки и коммита
        os.chdir(REPO_DIR)
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Clean solid database, restore blue UI and burger [skip ci]"])
        subprocess.run(["git", "push", "origin", "main"])
        
        # Успешный отчет
        send_telegram("✅ <b>TechnoSteak:</b> Каталог успешно обновлен и отправлен на GitHub!")
    except Exception as e:
        send_telegram(f"⚠️ <b>TechnoSteak Error:</b> <code>{e}</code>")

if __name__ == "__main__":
    send_telegram("🚀 <b>TechnoSteak Daemon запущен!</b> Работаем в непрерывном режиме (каждые 30 минут).")
    while True:
        save_and_build()
        # Ждем 30 минут (1800 секунд) до следующего запуска
        time.sleep(1800)
