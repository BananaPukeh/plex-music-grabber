#/bin/bash
IMAGE=rutgernijhuis/plex-music-grabber

docker build -t $IMAGE .
docker push $IMAGE