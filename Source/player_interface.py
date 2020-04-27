from multiprocessing.connection import Listener ,Client
from player import MediaStreamer, IsValidYoutube
import signal
import time
import os
import message
import json
import select
import pafy
from multiprocessing.connection import Client
import json

playlist_pipe=os.open("/Youtube_Player/playlist.pipe",os.O_RDONLY | os.O_NONBLOCK)

poll=select.poll()
poll.register(playlist_pipe,select.POLLIN)
idx=-1
add=0
repeat=0
status="Stop"
now_playing=None
playList=[]
md=MediaStreamer()
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
            print("Trying")
            time.sleep(1)
    writer.send(player_status)
    writer.close()
    #retmsg=message.create_msg(player_status)
    #status_pipe=os.open("/Youtube_Player/status.pipe",os.O_WRONLY)
    #os.write(status_pipe,retmsg)
while True:
    msg=None
    url=""
    action=""
    if (playlist_pipe,select.POLLIN) in poll.poll(1000):
        msg=message.get_message(playlist_pipe)
        msg=msg.replace("'",'"')
        msg=json.loads(msg)
    if not md.IsPlaying() and not md.IsPause:#Next song
        if (idx<len(playList)-1 and len(playList)>0) or add or repeat:
            idx+=1
            if repeat==1:
                idx-=1
            now_playing=playList[idx]
            while True:
                success=md.SetURL(now_playing)
                if success:
                    md.Play()
                time.sleep(2)
                if md.IsPlaying():
                    break
            status="Playing"
            add=0
        else:
            now_playing=None
            status="Stop"
    elif md.IsPause:
        status="Pause"

    if msg!=None:
        url=msg["url"]
        action=msg["action"]

    if IsValidYoutube(url):
        if action=="Append":
            playList.append(url)
            add=1
        if action=="Insert":
            playList.insert(idx+1,url)
            add=1
        new_add=pafy.new(url)
        MusicInfoDict[url]={
            "Title": new_add.title,
            "Author":new_add.author,
            "Length":new_add.length,
            "Image":new_add.bigthumbhd
            #"description":new_add.description
        }
    if md!=None:
        if action=="Play":
            md.Play()
            #print("Play")
            status="Playing"
        elif action=="Pause":
            md.Pause()
            #print("Pause")
            status="Pause"
        elif action=="Resume":
            md.Resume()
            #print("Resume")
            status="Playing"
        elif action=="Stop":
            md.Stop()
            #print("Stop")
            status="Stop"
        elif action=="Next":
            #print("Next")
            md.Stop()
            if idx==len(playList)-1:
                idx-=1
            md.IsPause=False
        elif action=="Pre":
            #print("Pre")
            idx-=2
            if idx<=-1:
                idx=-1
            md.Stop()
            md.IsPause=False
        elif action=="Repeat":
            #print("Repeat")
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
            md=MediaStreamer()
        elif action=="rtstate":
            returnState(MusicInfoDict,playList,idx,status,repeat)
    #print(playList,idx,status)