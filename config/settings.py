# config/settings.py
"""Конфигурация ассистента"""

import os
from pathlib import Path

# Базовые пути
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "knowledge_cache"
LOGS_DIR = BASE_DIR / "logs"
CONVERSATIONS_DIR = LOGS_DIR / "conversations"

# Путь к вашей базе знаний (используйте тот, который создали выше)
KNOWLEDGE_BASE_PATH = DATA_DIR / "База_знаний_ГРМ"

# Проверяем существование пути
if not KNOWLEDGE_BASE_PATH.exists():
    # Если симлинк не работает, используем оригинальный путь
    KNOWLEDGE_BASE_PATH = Path(r"C:\Users\User\Documents\Градум\Проекты\ГРМ\База знаний ГРМ")

# Конфигурация модели Ollama
OLLAMA_CONFIG = {
    "model": "gemma3:4b",  # Ваша выбранная модель
    "base_url": "http://localhost:11434/v1",
    "temperature": 0.3,     # Низкая температура для точных ответов по методикам
    "top_k": 40,
    "top_p": 0.9,
    "max_tokens": 2048,
}

# Конфигурация RAG
RAG_CONFIG = {
    "llm": OLLAMA_CONFIG,
    "embedding": {
        "model": "all-MiniLM-L6-v2",  # Хорошая модель для русского+английского
    },
    "chunk": {
        "strategy": "semantic",       # Умное разбиение текста
        "size": 512,                  # Размер куска текста
        "overlap": 50,                # Перекрытие между кусками
    },
    "retrieval": {
        "use_hybrid_search": True,    # Ключевой + векторный поиск
        "use_cross_encoder": False,   # Отключаем для экономии ресурсов
        "top_k": 5,                   # Количество извлекаемых фрагментов
    },
    "auto_update": {
        "enabled": True,              # Автообновление базы знаний
        "interval": 300,              # Интервал проверки (секунды)
    }
}

# Настройки интерфейса
UI_CONFIG = {
    "show_sources": True,             # Показывать источники
    "show_confidence": True,          # Показывать уверенность
    "max_history": 50,                # Максимум сохраненных диалогов
}

# Создаем необходимые директории
for dir_path in [DATA_DIR, CACHE_DIR, LOGS_DIR, CONVERSATIONS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)