# scripts/rebuild_index.py
"""Перестроение индекса базы знаний"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import shutil
from config.settings import CACHE_DIR, KNOWLEDGE_BASE_PATH
from src.assistant import Assistant

def rebuild():
    """Перестроение индекса"""
    print("🔄 Перестроение индекса базы знаний...")
    
    # Удаляем кэш
    if CACHE_DIR.exists():
        print(f"🗑️ Удаляем старый кэш: {CACHE_DIR}")
        shutil.rmtree(CACHE_DIR)
    
    # Создаем заново
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Инициализируем ассистента (создаст новый индекс)
    assistant = Assistant()
    assistant.initialize()
    
    print("✅ Индекс успешно перестроен!")

if __name__ == "__main__":
    rebuild()