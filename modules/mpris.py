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
        self.player.pause = False

    def pause(self):
        self.player.pause = True

    def next(self):
        self.player.playlist_next()

    def previous(self):
        self.player.playlist_prev()

