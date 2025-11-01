# -*- coding: utf-8 -*-
"""
Диагностика кодировки Python и окружения
"""

import sys
import locale
import os
import io

print("=== 🔍 PYTHON ENCODING DIAGNOSTICS ===")

# Проверим системные кодировки
print(f"sys.getdefaultencoding(): {sys.getdefaultencoding()}")
print(f"sys.stdout.encoding: {sys.stdout.encoding}")
print(f"sys.stderr.encoding: {sys.stderr.encoding}")
print(f"locale.getpreferredencoding(): {locale.getpreferredencoding(False)}")

# Проверим переменные окружения
for var in ["LANG", "LC_ALL", "PYTHONUTF8", "PYTHONIOENCODING"]:
    print(f"{var} = {os.getenv(var)}")

# Проверим, можем ли вывести русские символы
try:
    print("Тест вывода кириллицы: Привет, мир 🌍")
except Exception as e:
    print(f"Ошибка при выводе: {e}")

# Попробуем вручную переконфигурировать stdout/stderr
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    print("✅ Переконфигурация stdout/stderr в UTF-8 прошла успешно.")
    print("Проверка вывода после переконфигурации: Привет, мир 🌙")
except Exception as e:
    print(f"❌ Ошибка при переконфигурации: {e}")

print("=== ✅ ТЕСТ ЗАВЕРШЁН ===")
