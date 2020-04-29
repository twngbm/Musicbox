import pafy
import vlc
import re

def isYouTubeURL(youtube_url):
    """return the video Id of any valid Youtube Url as string

    >>> isYouTubeURL("https://www.youtube.com/watch?v=T2UW7VawmGI")
    'T2UW7VawmGI'
    >>> isYouTubeURL("https://www.youtube.com/watch?feature=youtu.be&v=T2UW7VawmGI")
    'T2UW7VawmGI'
    >>> isYouTubeURL("http://www.youtube.com/watch?v=T2UW7VawmGI")
    'T2UW7VawmGI'
    >>> isYouTubeURL("www.youtube.com/watch?v=T2UW7VawmGI")
    'T2UW7VawmGI'
    >>> isYouTubeURL("youtube.com/watch?v=T2UW7VawmGI")
    'T2UW7VawmGI'
    >>> isYouTubeURL("https://youtu.be/T2UW7VawmGI")
    'T2UW7VawmGI'
    >>> isYouTubeURL("http://youtu.be/T2UW7VawmGI")
    'T2UW7VawmGI'
    >>> isYouTubeURL("youtu.be/T2UW7VawmGI")
    'T2UW7VawmGI'
    >>> isYouTubeURL("www.youtube.com/embed/T2UW7VawmGI")
    'T2UW7VawmGI'
    >>> isYouTubeURL("")
    >>> isYouTubeURL("http://www.geekblog.tk/?v=T2UW7VawmGI")
    """
    youtube_regex = r"^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))(?P<YouTubeID>(\w|-){11})(?:\S+)?$"
    sreMatch = re.match(youtube_regex, youtube_url)
    return sreMatch.group("YouTubeID") if sreMatch else None
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
            return True
        except:
            return False
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
    

