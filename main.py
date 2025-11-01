# -*- coding: utf-8 -*-
import sys, os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# --- фиксим кодировки stdout/stderr ---
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# --- принудительно задаём системную кодировку ---
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["LANG"] = "ru_RU.UTF-8"
os.environ["LC_ALL"] = "ru_RU.UTF-8"

# --- загрузка токенов ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("❌ Не найден BOT_TOKEN в .env")
if not OPENAI_API_KEY:
    raise ValueError("❌ Не найден OPENAI_API_KEY в .env")

# --- инициализация OpenAI ---
client = OpenAI(api_key=OPENAI_API_KEY)

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔮 Привет, я SeerbornBot. Готов заглянуть за грань?")

# --- обработка сообщений ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты мистический, умный и немного саркастичный ИИ по имени Seerborn."},
                {"role": "user", "content": user_message}
            ]
        )

        ai_response = completion.choices[0].message.content.strip()
        ai_response = ai_response.encode('utf-8', errors='ignore').decode('utf-8')

        await update.message.reply_text(ai_response)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

# --- запуск ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 SeerbornBot запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
