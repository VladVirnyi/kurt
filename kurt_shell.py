import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

from modules.search import YoutubeSearch
from modules.player import Player
from prompt_toolkit.key_binding import KeyBindings

BANNER = """
 ██╗  ██╗██╗   ██╗██████╗ ████████╗
 ██║ ██╔╝██║   ██║██╔══██╗╚══██╔══╝
 █████╔╝ ██║   ██║██████╔╝   ██║   
 ██╔═██╗ ██║   ██║██╔══██╗   ██║   
 ██║  ██╗╚██████╔╝██║  ██║   ██║   
 ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
  Terminal Music Player v0.5
"""

class KurtAsyncShell:
    def __init__(self):
        self.youtube_search = YoutubeSearch()
        self.player = Player()
        self.current_results = []
        self.queue_list = []
        self.current_task = None
        
        self.system_commands = [
            'pause', 'resume', 'queue', 'skip', 'clear', 
            'status', 'exit', 'quit', 'help', 'volume', 'add', 'play'
        ]

    async def perform_search(self, query):
        try:
            loop = asyncio.get_running_loop()
            results = await loop.run_in_executor(None, self.youtube_search.search, query)
            self.current_results = results
            self.display_results(query)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"\n[Error during search: {e}]")

    def display_results(self, query):
        if not self.current_results:
            return
            
        print(f"\n--- Search Results for '{query}' ---")
        for i, entry in enumerate(self.current_results[:10], 1):
            title = entry.get('title', 'Unknown Title')
            duration = entry.get('duration', '??')
            print(f"[{i}] {title} ({duration}s)")
        print("-" * 35)


    def on_text_changed(self, buffer):
        text = buffer.text.strip()

        if self.current_task:
            self.current_task.cancel()

        if not text:
            return

        parts = text.lower().split()
        first_word = parts[0]

        if text.isdigit() or first_word in self.system_commands or len(text) < 3:
            return

        self.current_task = asyncio.create_task(self.run_debounced(text))

    async def run_debounced(self, query):
        await asyncio.sleep(0.5)
        await self.perform_search(query)

    #command handlers
    def handle_play(self, arg):
        if not arg:
            print("Please specify the number of the song to play from the search results.")
            return
        if not self.current_results:
            print("No search results available. Start typing to search first.")
            return
        try:
            index = int(arg) - 1
            if index < 0 or index >= len(self.current_results):
                print("Invalid index. Please choose a number from the search results.")
                return
            
            video_id = self.current_results[index].get('id')
            url = f"https://www.youtube.com/watch?v={video_id}"
            title = self.current_results[index].get('title', 'Unknown Title')

            print(f"▶Playing: {title}")
            self.player.play(url)
        except ValueError:
            print("Please enter a valid number corresponding to the search results.")

    def get_bottom_toolbar(self):
        """Text in progress bar with current song and time"""
        info = self.player.get_status()
        
        if not info:
            return "Ready to play. Start typing to search!"
        if info.get('pause'):
            return " ⏸ Playback Paused."

        curr = info.get('time') or 0
        total = info.get('duration') or 1 
        
        bar_length = 30
        progress = min(curr / total, 1.0)
        filled_chars = int(progress * bar_length)
        bar = '█' * filled_chars + '-' * (bar_length - filled_chars)
        
        curr_str = self._format_time(curr)
        total_str = self._format_time(total)
        
        title = info.get('title') or 'Unknown Title'
        
        title = str(title)
        
        if len(title) > 35:
            title = title[:32] + "..."

        return f" ▶{title} | {curr_str} [{bar}] {total_str} "

    def handle_add(self, arg):
        if not self.current_results:
            print("Please search for a song first by typing its name.")
            return
        try:
            index = int(arg) - 1
            if 0 <= index < len(self.current_results):
                entry = self.current_results[index]
                video_id = entry.get('id')
                url = f"https://www.youtube.com/watch?v={video_id}"
                title = entry.get('title', 'Unknown Title')

                self.player.queue_add(url)
                self.queue_list.append(title)
                print(f"Added to queue: {title}")
            else:
                print("Invalid index. Please choose a number from the search results.")
        except ValueError:
            print("Please enter a valid number.")

    def handle_queue(self):
        if not self.queue_list:
            print("Empty queue. Add something with 'add <number>'.")
        else:
            print("\n--- Current Queue ---")
            for i, song in enumerate(self.queue_list, 1):
                print(f"[{i}] {song}")

    def handle_skip(self):
        #method that exist in player.py
        self.player.queue_skip()
        
        # updating our local queue
        if self.queue_list:
            skipped = self.queue_list.pop(0)
            print(f"⏭ Skipped: {skipped}")

    def handle_clear(self):
        self.player.queue_clear()
        self.queue_list.clear()
        print("Queue cleared.")

    def handle_volume(self, arg):
        if not arg:
            vol = self.player.get_volume()
            print(f"Current volume: {vol}")
            return
        try:
            volume = int(arg)
            if 0 <= volume <= 100:
                self.player.set_volume(volume)
                print(f"Volume set to {volume}.")
            else:
                print("Volume must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid number for volume.")

    def _format_time(self, seconds):
        if seconds is None:
            return "00:00"
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def handle_status(self):
        info = self.player.get_status()
        if not info:
            print("No song is currently playing.")
            return

        curr_time = self._format_time(info.get('time', 0))
        total_time = self._format_time(info.get('duration', 0))
        status_icon = "⏸" if info.get('pause') else "▶"
        title = info.get('title', 'Unknown Title')

        print(f"\n{status_icon} Currently playing: {title}")
        print(f"Time: [{curr_time} / {total_time}]")

    def handle_help(self):
        help_text = """
Commands:
  [type words]    Instant search for songs on YouTube
  [number]        Play the song at that number (e.g. '1')
  play [number]   Play the specified song
  add [number]    Add the specified song to the queue
  pause(-p) / resume(-r)  Pause or resume playback
  queue           Show the current playlist
  skip(-s)        Skip to the next song in the queue
  clear(-c)       Clear the playlist
  volume(-v) [0-100]  Set or view current volume
  status          Show what is currently playing
  exit / quit     Exit the player
"""
        print(help_text)


    async def start(self):
        session = PromptSession()
        session.default_buffer.on_text_changed += self.on_text_changed
        
        #hotkey
        bindings = KeyBindings()

        #creating hotkeys for numbers 1-9 to play songs instantly from search results
        for i in range(1, 10):

            @bindings.add('escape', str(i), eager=True) 
            def _(event, num=i):
                event.app.current_buffer.text = str(num)
                event.app.current_buffer.validate_and_handle()

        #ctrl+l to clear the input
        @bindings.add('c-l')
        def _(event):
            event.app.current_buffer.text = ''

        print(BANNER)
        print("Type to search instantly. Type 'help' for commands.\n")
        print("💡 Pro-Tip: Press Alt+1, Alt+2 to instantly play a result!\n")

        with patch_stdout():
            while True:
                try:
                    user_input = await session.prompt_async(
                        "kurt> ", 
                        bottom_toolbar=self.get_bottom_toolbar,
                        refresh_interval=0.5,
                        key_bindings=bindings
                    )
                    
                    line = user_input.strip()
                    if not line:
                        continue
                        
                    parts = line.split(maxsplit=1)
                    cmd = parts[0].lower()
                    arg = parts[1] if len(parts) > 1 else ""

                    if cmd in ['exit', 'quit']:
                        print("See you later!")
                        break
                    elif cmd == 'help':
                        self.handle_help()
                    elif cmd == 'pause' or cmd == '-p':
                        self.player.pause()
                        print("⏸ Playback paused.")
                    elif cmd == 'resume' or cmd == '-r':
                        self.player.resume()
                        print("▶Playback resumed.")
                    elif cmd == 'queue':
                        self.handle_queue()
                    elif cmd == 'skip' or cmd == '-s':
                        self.handle_skip()
                    elif cmd == 'clear' or cmd == '-c':
                        self.handle_clear()
                    elif cmd == 'status':
                        self.handle_status()
                    elif cmd == 'volume' or cmd == '-v':
                        self.handle_volume(arg)
                    elif cmd == 'add':
                        self.handle_add(arg)
                    elif cmd == 'play':
                        self.handle_play(arg)
                    elif cmd.isdigit():
                        self.handle_play(cmd)
                    else:
                        print(f"Press Enter on a number to play it, or type 'help' for commands.")

                except (KeyboardInterrupt, EOFError):
                    print("\nSee you later!")
                    break

if __name__ == "__main__":
    shell = KurtAsyncShell()
    asyncio.run(shell.start())