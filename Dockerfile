FROM ubuntu:latest
MAINTAINER Jack Chen twngbm@gmail.com
RUN apt update && apt install -y python3.8 vlc-bin vlc-plugin-base python3-pip python-setuptools --no-install-recommends\
    &&python3.8 -m pip install setuptools &&python3.8 -m pip install youtube-dl python-vlc pafy tornado --no-cache-dir\
    &&python3.8 -m pip uninstall setuptools -y && apt remove python3-pip python-setuptools -y && apt autoremove -y \
    && mkdir Youtube_Player && mkfifo /Youtube_Player/playlist.pipe && mkfifo /Youtube_Player/status.pipe \
    && chmod 600 /Youtube_Player/playlist.pipe && chmod 600 /Youtube_Player/status.pipe \
    && rm -rf /var/lib/apt/lists/*
COPY Source/ ./Youtube_Player
WORKDIR /Youtube_Player
CMD ./main.sh
