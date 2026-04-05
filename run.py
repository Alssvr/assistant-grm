# run.py
"""Главный скрипт запуска ассистента"""

import sys
from pathlib import Path

# Добавляем текущую директорию в путь Python
sys.path.insert(0, str(Path(__file__).parent))

from src.cli import run_interactive

if __name__ == "__main__":
    run_interactive()