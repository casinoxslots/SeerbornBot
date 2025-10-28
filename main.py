# === main.py ===
# Основной файл Telegram-бота Seerborn
# Версия: этап 1 — базовые команды /start и /help

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

# --- загрузка переменных окружения из .env ---
# .env должен содержать строку вида:
# BOT_TOKEN=твой_токен_от_BotFather
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- команда /start ---
# Приветствие и проверка, что бот работает
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👁 Привет, я SeerbornBot.\n"
        "Готов следовать твоим шагам по пути познания.\n"
        "Введи /help, чтобы увидеть команды."
    )

# --- команда /help ---
# Выводит краткую справку по командам
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📜 Команды:\n"
        "/start — запустить бота\n"
        "/help — краткая справка\n"
        "\nДелаем всё поэтапно. Дальше — маленькая фича 😉"
    )
    await update.message.reply_text(text)


# --- точка входа ---
if __name__ == "__main__":
    # создаём приложение Telegram-бота
    app = Application.builder().token(BOT_TOKEN).build()

    # === регистрация хэндлеров ===
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))

    # === запуск бота ===
    print("✅ SeerbornBot запущен... (локальный режим)")
    app.run_polling()
