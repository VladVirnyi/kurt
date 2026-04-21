import threading

from .mpris import KurtMprisAdapter
from mpris_server.server import Server
from gi.repository import GLib

def setup_mpris(player):
    adapter = KurtMprisAdapter(player)
    mpris_server = Server('kurt', adapter=adapter)

    def run_server():
        try:

            mpris_server.publish()
            print("Service published on D-Bus")
            
            loop = GLib.MainLoop()
            loop.run()
        except Exception as e:
            print(f"mpris: Error: {e}")

    # Запускаємо в окремому потоці
    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    @player.property_observer('pause')
    def on_pause_change(_name, value):
        mpris_server.emit_changes('org.mpris.MediaPlayer2.Player', ['PlaybackStatus'])

    @player.property_observer('metadata')
    def on_metadata_change(_name, value):
        mpris_server.emit_changes('org.mpris.MediaPlayer2.Player', ['Metadata'])

    return mpris_server