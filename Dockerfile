FROM ubuntu:latest
MAINTAINER Jack Chen twngbm@gmail.com
RUN apt update && apt install -y python3.8 vlc-bin vlc-plugin-base python3-pip python3-alsaaudio --no-install-recommends\
    &&python3.8 -m pip install setuptools --no-cache-dir&&python3.8 -m pip install youtube-dl python-vlc pafy Flask requests --no-cache-dir\
    &&python3.8 -m pip uninstall setuptools -y && apt remove python3-pip -y && apt autoremove -y \
    && mkdir Musicbox \
    && rm -rf /var/lib/apt/lists/*
COPY Source/ ./Musicbox
WORKDIR /Musicbox
CMD /bin/python3 app.py
