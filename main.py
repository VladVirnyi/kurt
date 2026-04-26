#!/usr/bin/env python3
import argparse
import sys
import asyncio

from modules.mpris import MprisAdapter, setup_mpris
from kurt_shell import KurtAsyncShell

def main():
    # argparse settings
    parser = argparse.ArgumentParser(prog='kurt', description='Minimalist Async CLI Music Player')
    # parser.add_argument('-sp', '--spotify', action='store_true', help='Use Spotify as search platform')
    # parser.add_argument('-so', '--soundcloud', action='store_true', help='Use Soundcloud as search platform')
    parser.add_argument('-yo', '--youtube', action='store_true', help='Use Youtube as search platform (default)')

    args = parser.parse_args()

    shell = KurtAsyncShell()

    #flags (i guess kurt wil use only youtube search)
    # if args.spotify:
    #     print("Spotify mode activated")
    #     # in future we can use dependency injection
    #     # shell.youtube_search = SpotifySearch()
    # elif args.soundcloud:
    #     print("Soundcloud mode activated")
    #     # shell.youtube_search = SoundcloudSearch()
    # else:
    #     pass

    mpris = None  # Initialize mpris variable
    try:
        if hasattr(shell, 'player'):
            mpris = setup_mpris(shell.player)
            print("MPRIS integration successful")
        else:
            print("Player instance not found in shell.")
    except Exception as e:
        print(f"Integration failed: {e}")

    try:
        # run the shell
        asyncio.run(shell.start())
    except KeyboardInterrupt:
        print("\nGoodbye!")
    finally:
        pass

if __name__ == '__main__':
    main()