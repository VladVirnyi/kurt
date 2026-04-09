import cmd
from modules.search import YoutubeSearch
from modules.player import Player

BANNER = """
 ██╗  ██╗██╗   ██╗██████╗ ████████╗
 ██║ ██╔╝██║   ██║██╔══██╗╚══██╔══╝
 █████╔╝ ██║   ██║██████╔╝   ██║   
 ██╔═██╗ ██║   ██║██╔══██╗   ██║   
 ██║  ██╗╚██████╔╝██║  ██║   ██║   
 ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
  Terminal Music Player v0.1
"""

class KurtShell(cmd.Cmd):
    intro = BANNER + 'Type "help" for a list of commands or "exit" to quit.\n'
    prompt = 'kurt> '

    def __init__(self):
        super().__init__()
        self.youtube_search = YoutubeSearch()
        self.current_results = []
        self.player = Player()

    def do_search(self, arg):
        """Search for a song: search <title>"""
        if not arg:
            print("Please enter a search query.")
            return
        print(f"Searching for '{arg}' on YouTube (default)...")
        # search module would be called here
        results = self.youtube_search.search(arg)
        self.current_results = results

        for i, entry in enumerate(self.current_results, 1):
            # printing title and duration (if available)
            title = entry.get('title', 'Unknown Title')
            duration = entry.get('duration', '??')
            print(f"[{i}] {title} ({duration}s)")

    def default(self, line):
        """This method is called when the command is not recognized."""
        if line.isdigit():
            # If a number is entered, call do_play with that number
            return self.do_play(line)
        else:
            print(f"*** Unknown command: {line}")

    def do_play(self, arg):
        """Play a song from search results"""
        if not arg:
            print("Please specify the number of the song to play from the search results.")
            return
        if not self.current_results:
            print("No search results available. Use 'search' command first.")
            return
        try:
            index = int(arg) - 1
            if index < 0 or index >= len(self.current_results):
                print("Invalid index. Please choose a number from the search results.")
                return
            
            video_id = self.current_results[index].get('id')
            url = f"https://www.youtube.com/watch?v={video_id}"

            print(f"Playing: {self.current_results[index]['title']}")
            self.player.play(url)

        except ValueError:
            print("Please enter a valid number corresponding to the search results.")

    def do_queue(self, arg):
        """Show the playlist: queue"""
        print("Empty queue. Add something with 'add'.")

    # У файл kurt_shell.py

    def _format_time(self, seconds):
        """Method to format time in seconds to MM:SS format"""
        if seconds is None:
            return "00:00"
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def do_status(self, arg):
        """Show the current playback status: status"""
        info = self.player.get_status()
        
        if not info:
            print("No song is currently playing.")
            return

        curr_time = self._format_time(info['time'])
        total_time = self._format_time(info['duration'])
        status_icon = "⏸" if info['pause'] else "▶"

        print(f"\n{status_icon} Currently playing: {info['title']}")
        print(f"Time: [{curr_time} / {total_time}]")

    def do_exit(self, arg):
        """Exit the program"""
        print("See you later!")
        return True

    def emptyline(self):
        pass