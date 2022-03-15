#/bin/bash
IMAGE=rutgernijhuis/plex-music-grabber

TAG=$(git describe --tags `git rev-list --tags --max-count=1`)

docker build -t $IMAGE:$TAG .
docker push $IMAGE:$TAG