# src/logger.py
"""Модуль логирования"""

import logging
import json
from datetime import datetime
from pathlib import Path
from config.settings import LOGS_DIR, CONVERSATIONS_DIR

def setup_logger(name: str) -> logging.Logger:
    """Настройка логгера"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Лог в файл
    log_file = LOGS_DIR / f"{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    return logger

def save_conversation(question: str, answer: str, sources: list):
    """Сохраняет диалог в JSON файл"""
    conversation = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "sources": [
            {
                "file": str(source.source),
                "score": source.score,
                "chunk": source.chunk[:200]  # Сохраняем только начало для экономии места
            }
            for source in sources
        ]
    }
    
    # Имя файла по дате
    date_str = datetime.now().strftime("%Y%m%d")
    conv_file = CONVERSATIONS_DIR / f"conversation_{date_str}.json"
    
    # Загружаем существующие диалоги
    conversations = []
    if conv_file.exists():
        with open(conv_file, 'r', encoding='utf-8') as f:
            conversations = json.load(f)
    
    # Добавляем новый
    conversations.append(conversation)
    
    # Сохраняем обратно
    with open(conv_file, 'w', encoding='utf-8') as f:
        json.dump(conversations, f, ensure_ascii=False, indent=2)