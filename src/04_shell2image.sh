source build.cfg

docker run --rm -it --entrypoint=/bin/bash $DOCKER_REGISTRY/$DOCKER_IMAGE:$DOCKER_IMAGE_TAG
