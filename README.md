# Kurt

Kurt is a minimalist terminal music player written in Python.
It lets you search songs on YouTube, play audio in the terminal, and manage a simple playback queue.

## Features

- Search tracks on YouTube
- Play audio directly from selected search results
- Pause and resume playback
- Queue management: add, skip, clear, and view
- Volume control and playback status output

## Tech Stack

- Python 3.10+
- yt-dlp (YouTube search and metadata)
- python-mpv (audio playback wrapper)
- mpv (system-level player backend)

## Requirements

Install system dependency first:

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y mpv
```

### Arch Linux

```bash
sudo pacman -S mpv
```

### Fedora

```bash
sudo dnf install -y mpv
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

If your requirements file is empty, install manually:

```bash
pip install yt-dlp python-mpv
```

## Run

```bash
python main.py
```

## Interactive Commands

Inside the shell (`kurt>`):

- `search <your song/band>`: find songs on YouTube
- `<number>`: play song by index from the latest search results
- `pause`: pause playback
- `resume`: resume playback
- `add <number>`: add selected result to queue
- `queue`: show current queue
- `skip`: skip to next item
- `clear`: clear queue
- `volume [0-100]`: show or set volume
- `status`: show current playback status
- `exit`: close the app
