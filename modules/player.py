import mpv

class Player:
    def __init__(self):
        """
        mpv init
        ytdl=True allows mpv to handle YouTube URLs directly,
        video=False only audio playback, terminal=False disables mpv's own terminal interface,
        """
        try:
            self.instance = mpv.MPV(ytdl=True, video=False, terminal=False, input_default_bindings=False)
        except OSError as e:
            print("Error: mpv library not found. Please ensure mpv is installed and accessible.")
            raise e

    def play(self, url):
        """Запустити відтворення"""
        self.instance.play(url)

    def toggle_pause(self):
        """Toggle pause"""
        self.instance.pause = not self.instance.pause

    def stop(self):
        """Stop playback"""
        self.instance.stop()

    def set_volume(self, value):
        """Set volume (0-100)"""
        self.instance.volume = value

    def get_status(self):
        """Get current playback status"""
        return {
            "title": self.instance.media_title,
            "pause": self.instance.pause,
            "volume": self.instance.volume,
            "time": self.instance.time_pos,
            "duration": self.instance.duration
        }