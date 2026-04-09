import cmd
import argparse
import sys

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

    def do_search(self, arg):
        """Search for a song: search <title>"""
        if not arg:
            print("Please enter a search query.")
            return
        print(f"Searching for '{arg}' on YouTube (default)...")
        # search module would be called here

    def do_queue(self, arg):
        """Show the playlist: queue"""
        print("Empty queue. Add something with 'add'.")

    def do_exit(self, arg):
        """Exit the program"""
        print("See you later!")
        return True

    def emptyline(self):
        pass

def main():
    # argparse settings
    parser = argparse.ArgumentParser(prog='kurt', description='Minimalist CLI Music Player')
    parser.add_argument('-sp', '--spotify', action='store_true', help='Use Spotify as search platform')
    parser.add_argument('-so', '--soundcloud', action='store_true', help='Use Soundcloud as search platform')
    parser.add_argument('-yo', '--youtube', action='store_true', help='Use Youtube as search platform (default)')

    if len(sys.argv) == 1:
        KurtShell().cmdloop()
    else:
        args = parser.parse_args()
        if args.spotify:
            print("Spotify mode activated (Shell will still open)")
            # search modules here
            KurtShell().cmdloop()

if __name__ == '__main__':
    main()