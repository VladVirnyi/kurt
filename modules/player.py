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
        """Play a song"""
        self.instance.play(url)

    def pause(self):
        """Pause playback"""
        self.instance.pause = True

    def resume(self):
        """Resume playback"""
        self.instance.pause = False

    def toggle_pause(self):
        """Toggle pause"""
        self.instance.pause = not self.instance.pause

    def stop(self):
        """Stop playback"""
        self.instance.stop()

    def set_volume(self, value):
        """Set volume (0-100)"""
        self.instance.volume = value

    def set_volume(self, volume):
        """Set volume (0-100)"""
        volume = max(0, min(100, volume))  # Ensure volume is between 0 and 100
        self.instance.volume = volume

    def get_volume(self):
        """Get current volume"""
        return getattr(self.instance, 'volume', 100)

    def get_status(self):
        """Get current playback status"""
        return {
            "title": self.instance.media_title,
            "pause": self.instance.pause,
            "volume": self.instance.volume,
            "time": self.instance.time_pos,
            "duration": self.instance.duration
        }
    
    def queue_add(self, url):
        """Add a song to the queue"""
        self.instance.loadfile(url, mode='append-play')

    def queue_skip(self):
        """Skip to the next song in the queue"""
        self.instance.command('playlist-next', 'force')
    
    def queue_clear(self):
        """Clear the playlist"""
        self.instance.playlist_clear()