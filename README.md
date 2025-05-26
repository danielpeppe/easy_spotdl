## Installation

### Windows

1. ```py -m venv .venv``` - replace py with python or python3 if it does not work

2. ```py -m pip install -r requirements.txt```

3. ```spotdl --download-ffmpeg```

## Usage

Download tracks:
1. Put your spotify link(s) in ```spotify_links.txt```
2. Execute ```download_tracks.bat```

Extract Stems:
0. Download VirtualDJ (tested on v2025 b8553)
1. Open downloaded tracks in VirtualDJ
2. Right click on track and 'Save prepared stems'. This creates a .vdjstems file in the same directory
3. Execute ```extract_stems.bat``` 

## Credits

- DJ VINYLTOUCH on [VirtualDJ forums](https://www.virtualdj.com/forums/259669/VirtualDJ_Technical_Support/Exporting_stems_for_use_in_a_DAW.html)