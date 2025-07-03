# ytdl-gui: A Lightweight GUI for yt-dlp

Like the name says: it’s a Python GUI for yt-dlp, developed in one lunch break. Initially this was made to avoid annoying ads in your generic web-based yt-dl wrapper, and cause I was bored as hell.
# Core Functionality

- Graphical User Interface: This project was built with Tkinter, with absolutely zero regards for aesthetics.
- Dynamic Format Selection: ytdl-gui polls yt-dlp to show you a list of resolutions and file sizes.
- Visual Download Progress: A progress bar that lets you know it’s downloading.
- Legacy CLI Mode: I've kept the original `cli.py` for anyone who prefers simplified CLI.

# Getting Started

You'll need a few things to get the program running.
1. Python 3.x
2. The yt-dlp python package.
   
    ```
   pip install yt-dlp
    ```
4. FFmpeg (Recommended): `yt-dlp` may require `ffmpeg` in your system's PATH to merge video and audio.

Once everything is set up, fire up the main interface with a simple command:

```
python gui.py
```

Paste your YouTube URL, click 'Find Video' to see your options, pick one, and press 'Download Format'. The rest is automated, and will be stored in an output folder.
# Disclaimer

This was a rapid prototype. A proof of concept. A... thing built during my lunch break. While it's surprisingly capable, it wasn't exactly made to compete with anything.

- Error Handling: If you feed it a bad URL, it won’t do anything.
- Compatibility: Built and tested on my machine. It should work anywhere Python and Tkinter do.
- Code Quality: I’m a network engineer. I can’t make good code (yet). Please don’t judge harshly on my code :)

# Contributing

Feel free to fork this project, improve it, or rebuild it from the ground up. I'm still getting the hang of Git workflows, so I'm not accepting pull requests just yet. However, feel free to open an issue to share ideas or report bugs!
