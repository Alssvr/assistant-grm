# src/cli.py
"""Интерфейс командной строки"""

from src.assistant import Assistant
from src.utils import print_header, print_help, clear_screen, check_ollama
from colorama import Fore, Style
from pathlib import Path

def run_interactive():
    """Запуск интерактивного режима"""
    
    # Проверяем Ollama
    if not check_ollama():
        print(f"\n{Fore.RED}⚠️ Невозможно продолжить без Ollama{Style.RESET_ALL}")
        return
    
    # Инициализируем ассистента
    assistant = Assistant()
    try:
        assistant.initialize()
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка инициализации: {e}{Style.RESET_ALL}")
        return
    
    # Основной цикл
    print_header()
    print_help()
    print(f"\n{Fore.GREEN}💡 Готов к вопросам по методикам нормализации данных!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}\n")
    
    while True:
        try:
            # Получаем вопрос
            user_input = input(f"{Fore.YELLOW}❓ Вы:{Style.RESET_ALL} ").strip()
            
            # Обработка команд
            if user_input.lower() in ['/exit', '/quit', 'exit', 'quit']:
                print(f"\n{Fore.GREEN}👋 До свидания!{Style.RESET_ALL}")
                break
                
            if user_input.lower() == '/clear':
                clear_screen()
                print_header()
                print_help()
                print()
                continue
                
            if user_input.lower() == '/help':
                print_help()
                continue
                
            if user_input.lower() == '/sources':
                if assistant.last_citations:
                    print(f"\n{Fore.CYAN}📚 Источники последнего ответа:{Style.RESET_ALL}")
                    for i, cite in enumerate(assistant.last_citations, 1):
                        print(f"  {i}. {Fore.GREEN}{Path(cite.source).name}{Style.RESET_ALL}")
                        print(f"     Уверенность: {Fore.YELLOW}{cite.score:.0%}{Style.RESET_ALL}")
                        print(f"     Фрагмент: {cite.chunk[:150]}...")
                else:
                    print(f"\n{Fore.YELLOW}⚠️ Нет сохраненных источников. Задайте вопрос сначала.{Style.RESET_ALL}")
                continue
                
            if user_input.lower() == '/stats':
                stats = assistant.get_stats()
                print(f"\n{Fore.CYAN}📊 Статистика:{Style.RESET_ALL}")
                print(f"  Всего вопросов: {Fore.GREEN}{stats['total_questions']}{Style.RESET_ALL}")
                print(f"  В среднем источников: {Fore.GREEN}{stats['avg_sources_per_question']:.1f}{Style.RESET_ALL}")
                continue
            
            if not user_input:
                continue
            
            # Обрабатываем вопрос
            print(f"\n{Fore.MAGENTA}🤔 Анализирую методики...{Style.RESET_ALL}")
            
            try:
                answer = assistant.ask(user_input)
                
                # Выводим ответ
                print(f"\n{Fore.CYAN}🤖 Ассистент:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}{'-'*50}{Style.RESET_ALL}")
                print(answer.text)
                print(f"{Fore.WHITE}{'-'*50}{Style.RESET_ALL}")
                
                # Показываем источники
                if answer.citations:
                    print(f"\n{Fore.GREEN}📚 Найдено в {len(set(str(cite.source) for cite in answer.citations))} файлах:{Style.RESET_ALL}")
                    unique_sources = {}
                    for cite in answer.citations:
                        filename = Path(cite.source).name
                        if filename not in unique_sources:
                            unique_sources[filename] = cite.score
                            print(f"  • {Fore.YELLOW}{filename}{Style.RESET_ALL} (уверенность: {cite.score:.0%})")
                    
                    # Средняя уверенность
                    avg_score = sum(c.score for c in answer.citations) / len(answer.citations)
                    print(f"\n🎯 Общая уверенность ответа: {Fore.GREEN if avg_score > 0.7 else Fore.YELLOW}{avg_score:.0%}{Style.RESET_ALL}")
                else:
                    print(f"\n{Fore.YELLOW}⚠️ Ответ основан на общих знаниях (источники не найдены){Style.RESET_ALL}")
                
                print()
                
            except Exception as e:
                print(f"{Fore.RED}❌ Ошибка: {e}{Style.RESET_ALL}")
                print("   Попробуйте переформулировать вопрос или проверьте подключение к Ollama.")
                
        except KeyboardInterrupt:
            print(f"\n\n{Fore.GREEN}👋 Прервано пользователем. До свидания!{Style.RESET_ALL}")
            break
        except EOFError:
            break