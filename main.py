# -*- coding: utf-8 -*-
"""
SeerbornBot — Telegram-бот с OpenAI.
Исправлена кодировка и добавлены комментарии для стабильной работы на Linux (UTF-8).
"""

import os
import sys
import io
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# --------------------------------------------------------
# 💡 Исправление проблемы ASCII / UTF-8 в терминале и логах
# --------------------------------------------------------
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='ignore')

# --------------------------------------------------------
# 🔐 Загружаем токены и API-ключи из .env
# --------------------------------------------------------
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка наличия токенов
if not BOT_TOKEN:
    raise ValueError("❌ Не найден BOT_TOKEN в .env")
if not OPENAI_API_KEY:
    raise ValueError("❌ Не найден OPENAI_API_KEY в .env")

# --------------------------------------------------------
# 🤖 Инициализация OpenAI клиента
# --------------------------------------------------------
client = OpenAI(api_key=OPENAI_API_KEY)

# --------------------------------------------------------
# 🪄 Команда /start — приветствие
# --------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔮 Привет, я SeerbornBot. Готов заглянуть за грань?")

# --------------------------------------------------------
# 💬 Обработка всех обычных сообщений
# --------------------------------------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Отправляем сообщение пользователю в OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Ты мистический, умный и немного саркастичный ИИ по имени Seerborn. "
                               "Отвечай кратко, с атмосферой тайн и иронии."
                },
                {"role": "user", "content": user_message}
            ]
        )

        # Получаем ответ ИИ
        ai_response = completion.choices[0].message.content.strip()

        # --------------------------------------------------------
        # 🛠 Исправление кодировки и очистка текста
        # --------------------------------------------------------
        # Перекодировка в UTF-8, чтобы убрать спецсимволы, не поддерживаемые Telegram
        ai_response = ai_response.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
        # Убираем символы за пределами Unicode (например, битые эмодзи)
        ai_response = ''.join(ch for ch in ai_response if ord(ch) < 0x110000)

        # Отправляем ответ пользователю
        await update.message.reply_text(ai_response)

    except Exception as e:
        # Ловим любые ошибки (например, если Telegram не принимает символ)
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")
        print(f"[Ошибка] {e}")

# --------------------------------------------------------
# 🚀 Основная функция запуска бота
# --------------------------------------------------------
def main():
    print("🤖 SeerbornBot запускается...")

    # Создаем приложение Telegram
    app = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем команды и обработчики сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен. Ожидание сообщений...")
    app.run_polling()

# --------------------------------------------------------
# 🔥 Точка входа
# --------------------------------------------------------
if __name__ == "__main__":
    main()
