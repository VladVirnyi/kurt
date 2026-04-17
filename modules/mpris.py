# This file provide MPRIS support for Kurt-player, basically for integration with desktop envs,
# I will testing this on GNOME, but it should work on any DE that supports MPRIS, like KDE, XFCE, etc.

from mpris_server.adapters import MprisAdapter
from mpris_server.server import Server

class MprisAdapter(MprisAdapter):
    def __init__(self, player):
        self.player = player
        super().__init__()

    # mpris identity for .desktop file
    def get_desktop_entry(self):
        return "kurt"
    
    # player status
    def get_playback_status(self):
        """returns 'Playing', 'Paused' or 'Stopped'"""
        if self.player.pause:
            return "Paused"
        return "Playing"

    def get_metadata(self):
        """returns a dictionary of metadata according to the MPRIS 2 specification"""
        return {
            'mpris:trackid': '/org/mpris/MediaPlayer2/Track/0',
            'xesam:title': str(self.player.metadata.get('title', 'Unknown')),
            'xesam:artist': [str(self.player.metadata.get('artist', 'Unknown'))],
            'xesam:album': str(self.player.metadata.get('album', '')),
            'xesam:genre': [str(self.player.metadata.get('genre', ''))],

            # If you are fetching album art locally:
            # 'mpris:artUrl': f"file:///path/to/album_art.jpg" 
        }

    # Control (these methods will be called by GNOME)
    def play(self):
        self.player.pause = False

    def pause(self):
        self.player.pause = True

    def next(self):
        self.player.playlist_next()

    def previous(self):
        self.player.playlist_prev()


# Function for setting up MPRIS
def setup_mpris(player):
    adapter = MprisAdapter(player)
    # Register the player with the system (GNOME will see it as "kurt")
    mpris_server = Server('kurt', adapter=adapter)
    mpris_server.publish()

    @player.property_observer('pause')
    def on_pause_change(_name, value):
        mpris_server.emit_changes('org.mpris.MediaPlayer2.Player', ['PlaybackStatus'])

    @player.property_observer('metadata')
    def on_metadata_change(_name, value):
        mpris_server.emit_changes('org.mpris.MediaPlayer2.Player', ['Metadata'])

    return mpris_server