# This file provide MPRIS support for Kurt-player, basically for integration with desktop envs,
# I will testing this on GNOME, but it should work on any DE that supports MPRIS, like KDE, XFCE, etc.

from mpris_server.adapters import MprisAdapter
from mpris_server.base import PlayState

class KurtMprisAdapter(MprisAdapter):
    def __init__(self, player):
        self.player = player
        super().__init__()

    # mpris identity for .desktop file
    def get_desktop_entry(self):
        return "kurt"

    def can_quit(self):
        return False

    def can_raise(self):
        return False

    def can_fullscreen(self):
        return False

    def has_tracklist(self):
        return True

    def _get_pause_state(self):
        """Return True when paused, False when playing."""
        if not self.player:
            return True

        # Wrapper class: read pause from underlying MPV instance.
        instance = getattr(self.player, "instance", None)
        if instance is not None and hasattr(instance, "pause"):
            return bool(getattr(instance, "pause", True))

        pause_attr = getattr(self.player, "pause", True)
        if callable(pause_attr):
            return True

        return bool(pause_attr)

    def _set_pause_state(self, paused):
        if not self.player:
            return

        instance = getattr(self.player, "instance", None)
        if instance is not None and hasattr(instance, "pause"):
            instance.pause = paused
            return

        pause_attr = getattr(self.player, "pause", None)
        if callable(pause_attr):
            if paused:
                self.player.pause()
            elif hasattr(self.player, "resume") and callable(self.player.resume):
                self.player.resume()
            return

        setattr(self.player, "pause", paused)
    
    # player status
    def get_playstate(self):
        if not self.player:
            return PlayState.STOPPED
        if self._get_pause_state():
            return PlayState.PAUSED
        return PlayState.PLAYING

    # Keep this for compatibility with older snippets/usages.
    def playback_status(self):
        return self.get_playstate().value.title()

    def can_control(self):
        return True

    def can_go_next(self):
        return hasattr(self.player, 'playlist_next') or hasattr(self.player, 'queue_skip')

    def can_go_previous(self):
        return hasattr(self.player, 'playlist_prev')

    def can_pause(self):
        return True

    def can_play(self):
        return True

    def can_seek(self):
        return False

    def get_shuffle(self):
        return False

    def get_current_position(self):
        if not self.player:
            return 0

        instance = getattr(self.player, "instance", None)
        if instance is not None:
            seconds = getattr(instance, "time_pos", 0) or 0
        elif hasattr(self.player, "get_status") and callable(self.player.get_status):
            seconds = (self.player.get_status() or {}).get("time", 0) or 0
        else:
            seconds = 0

        return int(float(seconds) * 1_000_000)

    def get_volume(self):
        if not self.player:
            return 1.0

        instance = getattr(self.player, "instance", None)
        if instance is not None:
            raw_volume = getattr(instance, "volume", 100) or 0
        elif hasattr(self.player, "get_volume") and callable(self.player.get_volume):
            raw_volume = self.player.get_volume()
        else:
            raw_volume = 100

        normalized = float(raw_volume) / 100.0
        return max(0.0, min(1.0, normalized))

    def metadata(self):
        """returns a dictionary of metadata according to the MPRIS 2 specification"""
        md = getattr(self.player, "metadata", {}) if self.player else {}
        if not isinstance(md, dict):
            md = {}
        artist = md.get('artist', 'Unknown')
        if not isinstance(artist, list):
            artist = [str(artist)]
            
        try:
            return {
                'mpris:trackid': '/org/mpris/MediaPlayer2/Track/0',
                'xesam:title': str(md.get('title', 'Unknown')),
                'xesam:artist': artist,
                'xesam:album': str(md.get('album', '')),
                'xesam:genre': [str(md.get('genre', ''))],

                # If you are fetching album art locally:
                # 'mpris:artUrl': f"file:///path/to/album_art.jpg" 
            }
        except Exception as e:
            return {'mpris:trackid': '/org/mpris/MediaPlayer2/Track/0'}

    # Control (these methods will be called by GNOME)
    def play(self):
        self._set_pause_state(False)

    def pause(self):
        self._set_pause_state(True)

    def next(self):
        if self.player and hasattr(self.player, 'playlist_next'):
            self.player.playlist_next()
        elif self.player and hasattr(self.player, 'queue_skip'):
            self.player.queue_skip()

    def previous(self):
        if self.player and hasattr(self.player, 'playlist_prev'):
            self.player.playlist_prev()

