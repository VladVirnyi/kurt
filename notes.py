import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from modules.search import YoutubeSearch  # Твій існуючий модуль

class KurtShell:
    def __init__(self):
        self.search_engine = YoutubeSearch()
        self.current_task = None
        self.results = []

    async def perform_search(self, query):
        """Виконує реальний пошук через yt-dlp у фоновому потоці"""
        try:
            # Використовуємо run_in_executor, щоб yt-dlp не фрізив термінал
            loop = asyncio.get_running_loop()
            print(f"\n[Searching YouTube for: {query}...]")
            
            # Викликаємо твій синхронний метод search
            results = await loop.run_in_executor(None, self.search_engine.search, query)
            
            self.results = results
            self.display_results()
        except asyncio.CancelledError:
            # Це стається, коли користувач ввів новий символ і ми скасували старий таск
            pass
        except Exception as e:
            print(f"Error: {e}")

    def display_results(self):
        """Гарне виведення результатів"""
        if not self.results:
            return
        
        print("\n--- Top Results ---")
        for i, entry in enumerate(self.results[:5], 1):
            title = entry.get('title', 'Unknown Title')
            print(f"{i}. {title}")
        print("-" * 20)

    async def on_text_changed(self, buffer):
        """Callback на кожен натиск клавіші"""
        query = buffer.text.strip()
        
        if self.current_task:
            self.current_task.cancel()

        if len(query) < 3:
            return

        # Запускаємо дебаунс (0.5 сек)
        self.current_task = asyncio.create_task(self.run_debounced_search(query))

    async def run_debounced_search(self, query):
        await asyncio.sleep(0.5)
        await self.perform_search(query)

    async def start(self):
        session = PromptSession()
        with patch_stdout():
            print("Welcome to Kurt Instant Search!")
            print("Start typing to search. Press Enter to select or Ctrl+C to exit.")
            try:
                while True:
                    # Чекаємо на фінальний ввід (натискання Enter)
                    user_input = await session.prompt_async(
                        "kurt > ", 
                        on_changed=self.on_text_changed
                    )
                    if user_input:
                        print(f"You selected: {user_input}. Starting playback...")
                        # Тут можна додати виклик твого player.py
            except (KeyboardInterrupt, EOFError):
                print("\nExiting...")

if __name__ == "__main__":
    shell = KurtShell()
    asyncio.run(shell.start())