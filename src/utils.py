# src/utils.py
"""Вспомогательные функции"""

import os
import sys
import requests
from pathlib import Path
from colorama import init, Fore, Style

# Инициализация colorama для цветного вывода в консоли
init(autoreset=True)

def check_ollama() -> bool:
    """Проверяет, запущен ли Ollama и доступна ли модель"""
    try:
        # Проверяем доступность Ollama API
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                available_models = [m['name'] for m in models]
                print(f"{Fore.GREEN}✅ Ollama запущен. Доступные модели: {', '.join(available_models)}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.YELLOW}⚠️ Ollama запущен, но нет моделей. Установите модель: ollama pull gemma3:4b{Style.RESET_ALL}")
                return False
    except requests.exceptions.ConnectionError:
        print(f"{Fore.RED}❌ Ollama не запущен!{Style.RESET_ALL}")
        print("   Запустите Ollama:")
        print("     Windows: Найдите Ollama в меню Пуск и запустите")
        print("     Или выполните в терминале: ollama serve")
        return False
    return False

def check_model_available(model_name: str) -> bool:
    """Проверяет, скачана ли указанная модель"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return any(model_name in m['name'] for m in models)
    except:
        pass
    return False

def print_header():
    """Печатает красивый заголовок"""
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🤖 Ассистент по нормализации данных ГРМ{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

def print_help():
    """Печатает справку"""
    print(f"\n{Fore.YELLOW}📖 Доступные команды:{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}/help{Style.RESET_ALL}      - показать эту справку")
    print(f"  {Fore.GREEN}/clear{Style.RESET_ALL}     - очистить экран")
    print(f"  {Fore.GREEN}/sources{Style.RESET_ALL}   - показать источники последнего ответа")
    print(f"  {Fore.GREEN}/stats{Style.RESET_ALL}     - показать статистику")
    print(f"  {Fore.GREEN}/exit{Style.RESET_ALL}      - выход")
    print(f"  {Fore.GREEN}/quit{Style.RESET_ALL}      - выход")

def clear_screen():
    """Очищает экран консоли"""
    os.system('cls' if os.name == 'nt' else 'clear')