#!/usr/bin/env python3
import argparse
import sys
import asyncio
import threading

from modules import player
from modules.mpris import KurtMprisAdapter, Server
from modules.mpris_setup import setup_mpris
from kurt_shell import KurtAsyncShell


def main():
    # argparse settings
    parser = argparse.ArgumentParser(prog='kurt', description='Minimalist Async CLI Music Player')
    parser.add_argument('-yo', '--youtube', action='store_true', help='Use Youtube as search platform (default)')

    args = parser.parse_args()

    shell = KurtAsyncShell()

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