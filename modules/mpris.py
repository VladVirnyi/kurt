# This file provide MPRIS support for Kurt-player, basically for integration with desktop envs,
# I will testing this on GNOME, but it should work on any DE that supports MPRIS, like KDE, XFCE, etc.

from mpris_server.adapters import MprisAdapter
from mpris_server.server import Server
import threading

class KurtMprisAdapter(MprisAdapter):
    def __init__(self, player):
        self.player = player
        super().__init__()

    # mpris identity for .desktop file
    @property
    def Identity(self):
        return "Kurt Player"
    @property
    def DesktopEntry(self):
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
    def playback_status(self):
        """returns 'Playing', 'Paused' or 'Stopped'"""
        if self.player.pause:
            return "Paused"
        else:
            return "Playing"

    def metadata(self):
        """returns a dictionary of metadata according to the MPRIS 2 specification"""
        if not self.player or not hasattr(self.player, 'metadata'):
            return {'mpris:trackid': '/org/mpris/MediaPlayer2/Track/0'}
        
        try:
            return {
                'mpris:trackid': '/org/mpris/MediaPlayer2/Track/0',
                'xesam:title': str(self.player.metadata.get('title', 'Unknown')),
                'xesam:artist': [str(self.player.metadata.get('artist', 'Unknown'))],
                'xesam:album': str(self.player.metadata.get('album', '')),
                'xesam:genre': [str(self.player.metadata.get('genre', ''))],

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

