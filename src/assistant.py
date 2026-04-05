# src/assistant.py
"""Основной класс ассистента"""

from piragi import Ragi
from pathlib import Path
from config.settings import RAG_CONFIG, KNOWLEDGE_BASE_PATH, CACHE_DIR
from src.logger import setup_logger, save_conversation
from src.utils import check_model_available

class Assistant:
    """Ассистент для работы с базой знаний"""
    
    def __init__(self):
        self.logger = setup_logger(__name__)
        self.kb = None
        self.last_citations = None
        self.stats = {
            "questions": 0,
            "total_sources": 0
        }
        
    def initialize(self):
        """Инициализация ассистента"""
        print("\n🔧 Инициализация ассистента...")
        print(f"📁 База знаний: {KNOWLEDGE_BASE_PATH}")
        
        # Проверяем наличие базы знаний
        if not KNOWLEDGE_BASE_PATH.exists():
            raise FileNotFoundError(f"База знаний не найдена: {KNOWLEDGE_BASE_PATH}")
        
        # Проверяем наличие модели
        model_name = RAG_CONFIG["llm"]["model"]
        if not check_model_available(model_name):
            print(f"⚠️ Модель {model_name} не найдена. Загружаем...")
            # Здесь можно добавить автоматическую загрузку модели
        
        # Подсчитываем файлы
        files = list(KNOWLEDGE_BASE_PATH.glob("*"))
        print(f"📄 Найдено файлов: {len(files)}")
        for f in files[:5]:  # Показываем первые 5 файлов
            print(f"   - {f.name}")
        if len(files) > 5:
            print(f"   ... и еще {len(files) - 5} файлов")
        
        # Создаем базу знаний
        self.kb = Ragi(
            sources=[str(KNOWLEDGE_BASE_PATH)],
            persist_dir=str(CACHE_DIR),
            config=RAG_CONFIG
        )
        
        print("✅ Ассистент успешно инициализирован!")
        self.logger.info("Ассистент инициализирован")
        
    def ask(self, question: str):
        """Задать вопрос ассистенту"""
        if not self.kb:
            raise RuntimeError("Ассистент не инициализирован")
        
        self.logger.info(f"Вопрос: {question}")
        self.stats["questions"] += 1
        
        try:
            # Получаем ответ
            answer = self.kb.ask(question)
            self.last_citations = answer.citations
            
            # Сохраняем статистику
            self.stats["total_sources"] += len(answer.citations)
            
            # Сохраняем диалог
            save_conversation(question, answer.text, answer.citations)
            
            self.logger.info(f"Ответ получен, источников: {len(answer.citations)}")
            
            return answer
            
        except Exception as e:
            self.logger.error(f"Ошибка при получении ответа: {e}")
            raise
            
    def get_stats(self):
        """Получить статистику"""
        return {
            "total_questions": self.stats["questions"],
            "avg_sources_per_question": self.stats["total_sources"] / self.stats["questions"] if self.stats["questions"] > 0 else 0
        }