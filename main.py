# -*- coding: utf-8 -*-
# Указываем кодировку файла, чтобы поддерживать русские символы

import sys
import os
from dotenv import load_dotenv               # для загрузки переменных из .env
from telegram import Update                  # библиотека Telegram API
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI                    # клиент для работы с OpenAI API

# --- Настройка вывода в консоль под UTF-8 (важно для серверов Linux) ---
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

# --- Загружаем переменные окружения из .env ---
load_dotenv()

# Получаем токены из .env
BOT_TOKEN = os.getenv("BOT_TOKEN")            # Токен Telegram-бота
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Ключ OpenAI

# --- Проверяем наличие токенов ---
if not BOT_TOKEN:
    raise ValueError("❌ Не найден BOT_TOKEN в .env")
if not OPENAI_API_KEY:
    raise ValueError("❌ Не найден OPENAI_API_KEY в .env")

# --- Инициализация клиента OpenAI ---
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Команда /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветственное сообщение при вводе /start"""
    await update.message.reply_text("🔮 Привет, я SeerbornBot. Готов заглянуть за грань?")

# --- Обработка всех текстовых сообщений ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получает сообщение пользователя и отправляет ответ через OpenAI"""
    user_message = update.message.text

    try:
        # --- Отправляем запрос в OpenAI ---
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # модель OpenAI
            messages=[
                {"role": "system", "content": "Ты мистический, саркастичный и умный ИИ по имени Seerborn."},
                {"role": "user", "content": user_message}
            ]
        )

        # --- Извлекаем ответ модели ---
        ai_response = completion.choices[0].message.content

        # --- Отправляем ответ пользователю ---
        await update.message.reply_text(ai_response.encode('utf-8').decode('utf-8'))

    except Exception as e:
        # --- Отправляем пользователю сообщение об ошибке ---
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

# --- Основная функция ---
def main():
    """Запуск Telegram-бота"""
    app = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд и сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 SeerbornBot запущен...")
    app.run_polling()  # постоянный опрос Telegram-сервера

# --- Точка входа ---
if __name__ == "__main__":
    main()
