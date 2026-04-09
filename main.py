#!/usr/bin/env python3
import cmd
import argparse
import sys
from kurt_shell import KurtShell, BANNER

def main():
    (print("DEBUG: Starting KurtShell..."))
    # argparse settings
    parser = argparse.ArgumentParser(prog='kurt', description='Minimalist CLI Music Player')
    parser.add_argument('-sp', '--spotify', action='store_true', help='Use Spotify as search platform')
    parser.add_argument('-so', '--soundcloud', action='store_true', help='Use Soundcloud as search platform')
    parser.add_argument('-yo', '--youtube', action='store_true', help='Use Youtube as search platform (default)')

    if len(sys.argv) == 1:
        KurtShell().cmdloop()
        print("DEBUG: Exiting KurtShell...")
    else:
        args = parser.parse_args()
        if args.spotify:
            print("Spotify mode activated (Shell will still open)")
            # search modules here
            KurtShell().cmdloop()

if __name__ == '__main__':
    main()