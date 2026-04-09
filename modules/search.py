from yt_dlp import YoutubeDL

class Logger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class YoutubeSearch:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'no_warnings': True,
            'noplaylist': True,
            'extract_flat': 'True',
            'logger': Logger(),
        }

    def search(self, query, limit=5):
        with YoutubeDL(self.ydl_opts) as ydl:
            try:
                results = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
                return results['entries']
            except Exception as e:
                print(f"Error during YouTube search: {e}")
                return []