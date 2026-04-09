import cmd
from modules.search import YoutubeSearch

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
            # Виводимо назву та тривалість (якщо вона є)
            title = entry.get('title', 'Unknown Title')
            duration = entry.get('duration', '??')
            print(f"[{i}] {title} ({duration}s)")


    def do_queue(self, arg):
        """Show the playlist: queue"""
        print("Empty queue. Add something with 'add'.")

    def do_exit(self, arg):
        """Exit the program"""
        print("See you later!")
        return True

    def emptyline(self):
        pass