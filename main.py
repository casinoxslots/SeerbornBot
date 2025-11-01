# -*- coding: utf-8 -*-
# ✅ Полная поддержка русских символов и логирование ошибок

import sys
import os
import io
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# --- Принудительно задаём кодировку UTF-8 для всех системных потоков ---
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["LANG"] = "ru_RU.UTF-8"
os.environ["LC_ALL"] = "ru_RU.UTF-8"

# --- Загружаем .env файл ---
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("❌ Не найден BOT_TOKEN в .env")
if not OPENAI_API_KEY:
    raise ValueError("❌ Не найден OPENAI_API_KEY в .env")

# --- Инициализация клиента OpenAI ---
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Функция логирования ошибок в файл ---
def log_error(message: str):
    with open("logs.txt", "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

# --- Команда /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔮 Привет, я SeerbornBot. Готов заглянуть за грань?")

# --- Обработка сообщений ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print(f"[Пользователь]: {user_message}")

    try:
        # Отправляем запрос в OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты мистический, саркастичный и умный ИИ по имени Seerborn."},
                {"role": "user", "content": user_message}
            ]
        )

        ai_response = completion.choices[0].message.content.strip()
        print(f"[Seerborn]: {ai_response}")

        # Отправляем ответ пользователю
        await update.message.reply_text(ai_response)

    except Exception as e:
        error_text = f"⚠️ Ошибка: {str(e)}"
        await update.message.reply_text(error_text)
        log_error(error_text)

# --- Основная функция ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 SeerbornBot запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()

