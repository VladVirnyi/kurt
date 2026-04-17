from yt_dlp import YoutubeDL

class SilentLogger:
    """logger for yt-dlp that ignores all messages"""
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        #if debug uncomment this:
        # with open("kurt_errors.log", "a", encoding="utf-8") as f: 
        #     f.write(msg + "\n")
        pass

class YoutubeSearch:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'no_warnings': True,
            'noplaylist': True,
            'extract_flat': True,
            'logger': SilentLogger(),
            'ignoreerrors': True,    #continue searching even if some videos are age-restricted or unavailable
            'quiet': True,
        }

    def search(self, query, limit=5):
        with YoutubeDL(self.ydl_opts) as ydl:
            try:
                results = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
                
                if not results or 'entries' not in results:
                    return []
                    
                #if yt-dlp returns some None entries (e.g. age-restricted videos), 
                # we filter them out to avoid issues later on
                valid_entries = [entry for entry in results['entries'] if entry is not None]
                
                return valid_entries
                
            except Exception as e:
                return []