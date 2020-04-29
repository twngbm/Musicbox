from multiprocessing.connection import Listener ,Client
from player import MediaStreamer, isYouTubeURL, IsValidYoutube
import signal
import time
import os
import message
import json
import select
import pafy
from multiprocessing.connection import Client
import json
current_path=os.path.dirname(os.path.abspath(__file__))
command_pipe=os.open(current_path+"/command.pipe",os.O_RDONLY | os.O_NONBLOCK)
poll=select.poll()
poll.register(command_pipe,select.POLLIN)
APIKEY=os.environ['APIKEY']
idx=-1
add=0
repeat=0
status="Stop"
now_playing=None
playList=[]
md=MediaStreamer(APIKEY)
MusicInfoDict={}

def returnState(MusicInfoDict,playList,idx,status,repeat):
    player_status={
        "MusicInfoDict":MusicInfoDict,
        "Playlist":playList,
        "Status":[status,repeat],
        "NowPlaying":idx        
    }
    while True:
        try:
            writer=Client(('localhost',6000))
            break
        except:
            #print("Trying",i)
            time.sleep(1)
    writer.send(player_status)
    writer.close()

def returnCommand(msg):
    url=""
    action=""
    try:
        msg=msg.decode("utf-8")
        msg=msg.replace("'",'"')
        msg=json.loads(msg)
    except:
        msg=None
    if msg!=None:
        if "url" in msg:
            url=msg["url"]
        if "action" in msg:
            action=msg["action"]
    return url,action

while True:
    if not md.IsPlaying() and not md.IsPause:
        if (idx<len(playList)-1 and len(playList)>0) or add or repeat:
            if not repeat:
                idx+=1
            now_playing=playList[idx]
            try_count=0
            while True:
                if md.SetURL(now_playing):
                    md.Play()
                    time.sleep(2)
                    if md.IsPlaying():
                        add=0
                        break
                if try_count==10:
                    add=0
                    break
                try_count+=1
        else:
            now_playing=None
            status="Stop"


    if (command_pipe,select.POLLIN) in poll.poll(100):
        url,action=returnCommand(message.get_message(command_pipe))
    else:
        continue
    
    if action=="rtstate":
        if md.IsPlaying():
            status="Playing"
        returnState(MusicInfoDict,playList,idx,status,repeat)
        continue
    
    youtubeCode=isYouTubeURL(url)
    if youtubeCode!=None and IsValidYoutube(youtubeCode):
        if action=="Append":
            playList.append(youtubeCode)
            add=1
        if action=="Insert":
            playList.insert(idx+1,youtubeCode)
            add=1
        new_add=pafy.new(youtubeCode)
        MusicInfoDict[youtubeCode]={
            "Title": new_add.title,
            "Author":new_add.author,
            "Length":new_add.length,
            "Image":new_add.bigthumbhd
        }
        continue

    if md!=None:
        if action=="Play":
            md.Play()
        elif action=="Pause":
            md.Pause()
            status="Pause"
        elif action=="Resume":
            md.Resume()
        elif action=="Stop":
            md.Stop()
            status="Stop"
        elif action=="Next":
            md.Stop()
            if idx==len(playList)-1:
                idx-=1
            md.IsPause=False
        elif action=="Pre":
            idx-=2
            if idx<=-1:
                idx=-1
            md.Stop()
            md.IsPause=False
        elif action=="Repeat":
            repeat=1 if repeat==0 else 0
        elif action=="Clean":
            md.Stop()
            MusicInfoDict={}
            idx=-1
            add=0
            repeat=0
            status="Stop"
            now_playing=None
            playList=[]
            md=MediaStreamer(APIKEY)
        
