#!/usr/bin/env python3
import argparse
import sys
import asyncio

# Імпортуємо нову асинхронну оболонку
from kurt_shell import KurtAsyncShell

def main():
    # argparse settings
    parser = argparse.ArgumentParser(prog='kurt', description='Minimalist Async CLI Music Player')
    parser.add_argument('-sp', '--spotify', action='store_true', help='Use Spotify as search platform')
    parser.add_argument('-so', '--soundcloud', action='store_true', help='Use Soundcloud as search platform')
    parser.add_argument('-yo', '--youtube', action='store_true', help='Use Youtube as search platform (default)')

    # Парсимо аргументи одразу. Якщо аргументів немає, argparse просто поверне значення за замовчуванням
    args = parser.parse_args()

    # Створюємо екземпляр нашої нової оболонки
    shell = KurtAsyncShell()

    # Обробка прапорців платформ
    if args.spotify:
        print("🟢 Spotify mode activated")
        # У майбутньому тут можна зробити Dependency Injection:
        # shell.youtube_search = SpotifySearch()
    elif args.soundcloud:
        print("🟠 Soundcloud mode activated")
        # shell.youtube_search = SoundcloudSearch()
    else:
        # YouTube використовується за замовчуванням (вже ініціалізовано в KurtAsyncShell)
        pass

    # Запускаємо асинхронний Event Loop
    try:
        asyncio.run(shell.start())
    except KeyboardInterrupt:
        # Глобальний перехват Ctrl+C на випадок, якщо щось піде не так під час ініціалізації
        print("\nGoodbye!")

if __name__ == '__main__':
    main()