import pafy
import vlc
def IsValidYoutube(url):
        try:
            pafy.new(url)
            return True
        except:
            return False
class MediaStreamer():
    def __init__(self,APIKEY):
        self.mrl=None
        self.video=None
        self.Player=vlc.MediaPlayer()
        self.IsPause=False
        pafy.set_api_key(APIKEY)
    def SetURL(self,url):
        try:
            self.video=pafy.new(url)
            self.mrl=self.video.getbestaudio().url
            self.Player=vlc.MediaPlayer(self.mrl)
            return 1
        except:
            return 0
    def getVideo(self):
        return self.video
    def Play(self):
        self.Player.play()
        self.IsPause=False
    def Pause(self):
        if self.IsPlaying():
            self.IsPause=True
        self.Player.set_pause(1)
    def Resume(self):
        self.Player.set_pause(0)
        self.IsPause=False
    def Stop(self):
        self.Player.stop()
        self.IsPause=True
    def IsPlaying(self):
        return self.Player.is_playing()
    

