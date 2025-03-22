#!/bin/bash
set -e

# Выводим информацию о Python и установленных пакетах для отладки
echo "Python version: $(python --version)"
echo "Installed packages:"
pip list

# Запускаем Uvicorn
exec python3 -m uvicorn main:app --host 0.0.0.0 --port 8000