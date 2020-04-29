FROM ubuntu:latest
MAINTAINER Jack Chen twngbm@gmail.com
RUN apt update && apt install -y python3.8 vlc-bin vlc-plugin-base python3-pip --no-install-recommends\
    &&python3.8 -m pip install setuptools --no-cache-dir&&python3.8 -m pip install youtube-dl python-vlc pafy tornado --no-cache-dir\
    &&python3.8 -m pip uninstall setuptools -y && apt remove python3-pip -y && apt autoremove -y \
    && mkdir Musicbox && mkfifo Musicbox/command.pipe && chmod 600 Musicbox/command.pipe \
    && rm -rf /var/lib/apt/lists/*
COPY Source/ ./Musicbox
WORKDIR /Musicbox
CMD ./main.sh
