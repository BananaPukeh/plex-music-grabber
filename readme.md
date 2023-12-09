# Plex Music Grabber
Plex Music Grabber is a tool that monitors your Plex TV Show library for missing theme music. Unfortunately not all shows on Plex have theme songs, so I wrote this script that automatically downloads theme songs.

## Key features
- Download missing theme songs
- Works with TV shows, which are also provided by Plex
- Works with Movies, which are not provided by Plex.
- Supports movie/show folders named like: `Movie (year) {tmdb-12345}`


## Installation

1. Mount the `/library` volume on your tv show directory
2. Choose a scan interval (seconds) of your liking

Docker CLI
```
docker run -d \
--name plex-music-grabber \
-v /path/to/tvshows:/library/tvshows \
-v /path/to/movies:/library/movies \
-e interval=3600 \
-e library_path=/library/tvshows,/library/movies \
--restart unless-stopped \
rutgernijhuis/plex-music-grabber
```

Docker Compose
```
version: "3.3"
services:
  plex-music-grabber:
    image: rutgernijhuis/plex-music-grabber
    container_name: plex-music-grabber
    volumes:
      - ./my-library/movies:/library/movies
      - ./my-library/tvshows:/library/tvshows
    environment:
      - interval=3600
      - library_path=/library/movies,/library/tvshows
    restart: unless-stopped
    network_mode: default
```

`library_path` variable needs one or more mounted paths to you library containing sub folders with media folders. Multiple paths needs to be comma seperated.

### Telegram notifications
Add these environment variables:
- `telegram_chat_id`
- `telegram_token`

## Post installation 
3. Verify that the script is working by checking your show folders, the program should create a `theme.mp3` file.
4. Make sure Plex uses your local assets in your media. Go to `Plex > Settings > Agents > Shows > {one/all of your agents}`
5. Ensure `Local Media Assets(TV)` is checked. Optionally, you can change the priorities of where Plex should get your metadata from.
6. Go to a show in Plex and refresh it's metadata, the song should play :)

## Options
### Ignoring items
When you don't want a show folder to be searched for you can choose to ignore it.
Do so by adding a `.themeignore` file in the directory

# Running it locally

## Python native
If you want to run it locally, I suppose you know what you are doing.

Tested on Python 3.9


`pip install -r requirements.txt`

Note Before running:

The script uses environment variables to locate your library and the interval time.
I used VSCode for developing and added them to `./vscode/launch.json`

```
library_path="path/to/your/test/library"
interval=5
```

Or set env variables in your CLI.

# Library structure

Your library should be in the following structure:
- The `shows` path must be specified when starting the script.
- All directories below `shows` will be searched for if they don't contain a `theme.mp3` file. These directories need human readable names!
- Everything below the show directory will be ignored.

```
shows/
├── Vinland Saga/
│   ├── S01E01.mkv
│   ├── S01E02.mkv
│   └── S01E03.mkv
├── Initial D/
│   ├── Season 1/
│   │   ├── S01E01.mkv
│   │   ├── S01E02.mkv
│   │   └── S01E03.mkv
│   └── theme.mp3
└── Game Of Thrones/
    ├── S01E01.mkv
    ├── S01E02.mkv
    ├── S01E03.mkv
    └── theme.mp3
```

# Updating image

- Create a new tag
- run `update-image.sh`