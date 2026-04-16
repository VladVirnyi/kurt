from yt_dlp import YoutubeDL

class SilentLogger:
    """Тихий логер, щоб помилки yt-dlp не 'смітили' в термінал і не ламали UI"""
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        # Замість print просто ігноруємо помилку.
        # Якщо колись захочеш відстежувати баги, можна розкоментувати запис у файл:
        # with open("kurt_errors.log", "a", encoding="utf-8") as f: 
        #     f.write(msg + "\n")
        pass

class YoutubeSearch:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'no_warnings': True,
            'noplaylist': True,
            'extract_flat': True,    # Виправлено: тепер це boolean (True), а не строка ('True')
            'logger': SilentLogger(),
            'ignoreerrors': True,    # КРИТИЧНО: змушує yt-dlp пропускати відео з помилками (наприклад 18+) і шукати далі
            'quiet': True,           # Повністю вимикає стандартний вивід yt-dlp
        }

    def search(self, query, limit=5):
        with YoutubeDL(self.ydl_opts) as ydl:
            try:
                # ytsearch повертає словник, де 'entries' - це список знайдених відео
                results = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
                
                if not results or 'entries' not in results:
                    return []
                    
                # Якщо yt-dlp натрапив на відео 18+ (при ignoreerrors=True), 
                # він вставить замість нього None у список результатів.
                # Тому ми відфільтровуємо всі None, залишаючи тільки робочі відео.
                valid_entries = [entry for entry in results['entries'] if entry is not None]
                
                return valid_entries
                
            except Exception as e:
                # Ми прибрали print(), щоб у разі відсутності інтернету 
                # програма не викидала червоний текст посеред екрану.
                # Замість цього просто повертаємо пустий список результатів.
                return []