# -*- coding: utf-8 -*-
"""
SeerbornBot — Telegram-бот с OpenAI.
Полностью исправлены ошибки ASCII при работе на Linux-серверах.
Добавлены комментарии ко всем важным участкам.
"""

import os
import sys
import io
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# =====================================================
# 🧩 1. Настройка вывода в UTF-8 (фикс ошибки 'ascii')
# =====================================================
# Принудительно задаем UTF-8 для стандартного вывода и ошибок.
# Это предотвращает сбои при логировании русских символов в консоль.
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# =====================================================
# 🔇 2. Отключаем встроенные логи Telegram
# =====================================================
# Telegram-бот библиотека по умолчанию пишет INFO-логи,
# которые могут содержать русские символы и ломать ASCII-вывод.
# Мы отключаем все, кроме критических сообщений.
logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.ERROR,  # ⚠️ только ошибки, без обычных логов
    encoding='utf-8'
)
logger = logging.getLogger("telegram")
logger.setLevel(logging.CRITICAL)  # Полностью глушим Telegram-логи

# =====================================================
# 🔐 3. Загружаем токены из .env
# =====================================================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверяем наличие переменных окружения
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не найден в .env")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY не найден в .env")

# Инициализируем OpenAI API
client = OpenAI(api_key=OPENAI_API_KEY)

# =====================================================
# 🧭 4. Команда /start
# =====================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Команда /start — приветственное сообщение пользователю.
    """
    try:
        await update.message.reply_text("🔮 Привет, я SeerbornBot. Готов заглянуть за грань?")
    except Exception as e:
        print(f"[Ошибка при отправке /start]: {e}")

# =====================================================
# 💬 5. Обработка сообщений пользователя
# =====================================================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Основной обработчик сообщений.
    Проверяет, что сообщение текстовое, и отправляет его в OpenAI.
    """
    # Проверяем, что сообщение существует и содержит текст
    if not update.message or not update.message.text:
        await update.effective_chat.send_message("😶 Я понимаю только текст. Попробуй написать словами.")
        return

    user_message = update.message.text.strip()

    try:
        # 🧠 Отправляем запрос в OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты мистический, саркастичный ИИ по имени Seerborn. Отвечай с атмосферой тайн и иронии."},
                {"role": "user", "content": user_message}
            ]
        )

        ai_response = completion.choices[0].message.content.strip()

        # 🧹 Удаляем неподдерживаемые символы (на всякий случай)
        safe_response = ai_response.encode('utf-8', errors='replace').decode('utf-8', errors='replace')

        # ✂️ Ограничиваем длину, чтобы Telegram не обрезал сообщение
        if len(safe_response) > 4000:
            safe_response = safe_response[:3997] + "..."

        # Отправляем ответ пользователю
        await update.message.reply_text(safe_response)

    except Exception as e:
        # Безопасно выводим ошибки в консоль
        err_msg = str(e).encode('utf-8', errors='replace').decode('utf-8', errors='replace')
        print(f"[Ошибка OpenAI или Telegram] {err_msg}")
        try:
            await update.message.reply_text(f"⚠️ Ошибка: {err_msg}")
        except:
            pass

# =====================================================
# 🚀 6. Основная функция запуска бота
# =====================================================
def main():
    """
    Запускает Telegram-бота и инициализирует обработчики.
    """
    print("🤖 SeerbornBot запускается...")
    app = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд и сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен. Готов принимать сообщения.")
    app.run_polling()  # Ожидает входящие сообщения

# =====================================================
# ⚙️ 7. Точка входа
# =====================================================
if __name__ == "__main__":
    main()

