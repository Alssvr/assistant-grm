# scripts/batch_process.py
"""Пакетная обработка вопросов из файла"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from src.assistant import Assistant

def batch_process(questions_file: str, output_file: str = "batch_results.json"):
    """Обрабатывает вопросы из файла"""
    
    # Читаем вопросы
    with open(questions_file, 'r', encoding='utf-8') as f:
        questions = [q.strip() for q in f.readlines() if q.strip()]
    
    print(f"📋 Загружено {len(questions)} вопросов")
    
    # Инициализируем ассистента
    assistant = Assistant()
    assistant.initialize()
    
    results = []
    for i, question in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] Обработка: {question[:50]}...")
        
        try:
            answer = assistant.ask(question)
            results.append({
                "question": question,
                "answer": answer.text,
                "sources": [str(cite.source) for cite in answer.citations],
                "confidence": sum(c.score for c in answer.citations) / len(answer.citations) if answer.citations else 0
            })
        except Exception as e:
            results.append({
                "question": question,
                "error": str(e)
            })
    
    # Сохраняем результаты
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Результаты сохранены в {output_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        batch_process(sys.argv[1])
    else:
        print("Использование: python batch_process.py вопросы.txt")