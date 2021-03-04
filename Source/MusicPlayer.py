import time
import os
import vlc
import pafy
import re
import alsaaudio
import requests
import random
import logging


class Player():
    def __init__(self):
        APIKEY = os.environ['APIKEY']
        pafy.set_api_key(APIKEY)
        self.idx = 0
        self.repeat = 0
        self.autoplay = False
        self.status = 0
        self.playList = []
        self.isPsuse = False
        self.playlistText = []
        self.statusChange = False
        self.mp = vlc.MediaPlayer()
        self.volumeControl = alsaaudio.Mixer()
        self.volume = int(self.volumeControl.getvolume()[0])

    def Update(self):
        if self.statusChange:
            if self.status == -1:
                self.mp.set_pause(1)
            elif self.status == 0:
                self.mp.stop()
            elif self.status == 1:
                media = self.playList[self.idx]
                new_media = pafy.new(media.videoid)
                self.mp.set_mrl(new_media.getbestaudio().url)
                self.mp.play()
            elif self.status == 2:
                self.mp.set_pause(0)
                self.isPsuse = False
                self.status = 1
            self.statusChange = False

    def getNextSuggestion(self, videoID):
        retry = 0
        while retry < 10:
            r = requests.get("https://www.youtube.com/watch?v="+videoID)
            content = r.text
            x = content.find("自動播放")
            if x == -1:
                retry += 1
                continue
            c = []
            while x != -1:
                x = content.find("videoIds", x+1)
                candidate = content[x+12:x+23]
                c.append(candidate)
            c = list(set(c))
            try:
                c = c[0:8]
            except:
                pass
            new_c = []
            len_c = len(c)
            for idx, url in enumerate(c):
                for _ in range(len_c-idx):
                    new_c.append(url)
            newpick = random.choice(new_c)
            if len(new_c) == 1 or "html" in newpick:
                continue
            return newpick
        return videoID

    def Check(self):
        if self.mp.is_playing() == 0 and self.status == 1:
            if self.repeat == 1:
                self.statusChange = True
                self.Update()
                return False

            self.idx += 1
            if self.idx == len(self.playList):
                if not self.autoplay:
                    self.idx = 0
                    if self.repeat != 2:
                        self.status = 0
                else:
                    current = self.playList[-1]
                    nextTrack = self.getNextSuggestion(current.videoid)
                    self.playList.append(pafy.new(nextTrack))

            self.statusChange = True
            self.Update()
            return True
        return False

    def Append(self, msg):
        action = msg["Action"]
        url = msg["url"]
        try:
            v = pafy.new(url)
        except ValueError:
            return None
        if action == "Append":
            self.playList.append(v)
        elif action == "Insert":
            self.playList.insert(self.idx+1, v)
        if self.status == 0:
            self.status = 1
            if action == "Append":
                self.idx = len(self.playList)-1
            else:
                self.idx += 1
            self.statusChange = True

    def Play(self, msg):
        if self.status == 0:
            self.status = 1
            self.statusChange = True
        elif self.status == -1:
            self.status = 2
            self.statusChange = True

    def Pause(self, msg):
        if self.status != -1:
            self.status = -1
            self.statusChange = True

    def Resume(self, msg):
        if self.status == -1:
            self.status = 2
            self.statusChange = True
        elif self.status == 0:
            self.status = 1
            self.statusChange = True

    def Stop(self, msg):
        if self.status != 0:
            self.status = 0
            self.statusChange = True

    def Next(self, msg):
        self.idx += 1
        if self.idx == len(self.playList):
            if self.autoplay:
                current = self.playList[-1]
                nextTrack = self.getNextSuggestion(current.videoid)
                self.playList.append(pafy.new(nextTrack))

            else:
                self.idx -= 1

        self.status = 1
        self.statusChange = True

    def Pre(self, msg):
        self.idx -= 1
        if self.idx < 0:
            self.idx = 0
        self.status = 1
        self.statusChange = True

    def Insert(self, msg):
        self.Append(msg)

    def Repeat(self, msg):
        self.repeat += 1
        self.repeat %= 3

    def Autoplay(self, msg):
        self.autoplay = True if self.autoplay == False else False

    def IncreaseVolume(self, msg):
        self.volume += 5
        if self.volume >= 100:
            self.volume = 100
        self.volumeControl.setvolume(self.volume)

    def DecreaseVolume(self, msg):
        self.volume -= 5
        if self.volume <= 0:
            self.volume = 0
        self.volumeControl.setvolume(self.volume)

    def Clean(self, msg):
        self.idx = 0
        self.repeat = 0
        self.autoplay = False
        self.status = 0
        self.playList = []
        self.playlistText = []
        self.statusChange = False
        self.mp.stop()
        self.isPsuse = False
        self.mp = vlc.MediaPlayer()

    def getState(self, msg):
        if len(self.playlistText) == len(self.playList):
            pass
        else:
            self.playlistText = []
            for track in self.playList:
                self.playlistText.append(
                    {"title": track.title.replace("'", "-"),
                     "duration": track.duration,
                     "author": track.author.replace("'", "-"),
                     "length": track.length,
                     "videoid": track.videoid,
                     "thumb": track.bigthumbhd
                     })
        state = {"index": self.idx, "status": self.status,
                 "repeat": self.repeat, "autoplay": self.autoplay, "volume": self.volume, "playlist": self.playlistText}
        return state


def playerInterface(Input, Output):
    music_consol = Player()
    while True:
        try:
            msg = Input.get(timeout=2)
        except:
            if music_consol.Check():
                state = music_consol.getState(None)
                logging.info(f"Status Update:{state}")
                Output.put(state, block=False)
            continue
        try:
            result = getattr(music_consol, msg["Action"])(msg)
        except Exception as e:
            logging.error(f"Wrong Contrlo Type:{e}")
        music_consol.Update()
        state = music_consol.getState(None)
        logging.info(f"Status Update:{state}")
        Output.put(state, block=False)
