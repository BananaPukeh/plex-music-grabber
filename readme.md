# Plex Music Grabber
Plex Music Grabber is a tool that monitors your Plex TV Show library for missic theme music. Unfortunately not all shows on Plex have theme songs, so I wrote this script that automatically downloads theme songs

## Installation

1. Mount the `/library` volume on your tv show directory
2. Choose a scan interval (seconds) of your liking

```
docker run -d \
--name plex-music-grabber \
-v /path/to/tvshow:/library \
-e interval=3600 \
--restart unless-stopped \
rutgernijhuis/plex-music-grabber
```

## Post installation 
3. Verify that the script is working by checking your show folders, the program should create a `theme.mp3` file.
4. Make sure Plex uses your local assets in your media. Go to `Plex > Settings > Agents > Shows > {one/all of your agents}`
5. Ensure `Local Media Assets(TV)` is checked. Optionally, you can change the priorities of where Plex should get your metadata from.


## Running it locally
If you want to run it locally, I suppose you know what you are doing.

Tested on Python 3.8.5

`pip install -r requirements.txt`

Note Before running:

The script uses environment variables to locate your library and the interval time.
I used VSCode for developing and added them to `./vscode/launch.json`

```
library_path="path/to/your/test/library"
interval=5
```