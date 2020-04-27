# Musicbox
A web base multi user in room music player for workhouse or home using docker.

# Description
   This is a music playing project using python, linux IPC, html and javascript. This project's main feature is to provide a multi user
 single queue music player which can be used at hoome, workhouse or office. It provide a web base interface for streaming youtube's music.
on a central server, like a public-office server or home-hub server with a speaker attach to it. 

This Project is develop and publish via docker for system software dependence isolate and integrity. I provid Dockerfile and every Source that I used inside this project.

This is a working project which main purpose is practicing front-end/back-end integration and coding skill, so it may contain lot of bug and exception. Feel free to modify it at your own used.

# Pre-Requests
1. **Google API keys**, you can request one at google api console.
2. **docker and docker.io** installed on your host machine. 
3. Speaker device on central server.
# Usage
1. Build The Image 

```
$ docker build -t musicbox . --no-cache
```

* You can use whatever valid docker image name you wish.

2. Run This Image at background
```
$ docker run --name=Musicbox -p=8080:80 --env="APIKEY=<Google Api Key>" --device=/dev/snd --detach musicbox
```
3. Setup iptables for limit access(Highly Recommends, sinec this project haven't provide web user authority yet.)
```
$ sudo iptables -I DOCKER-USER -i enp0 -m conntrack --ctorigdstport 8080 --ctdir ORIGINAL -j DROP
$ sudo iptables -I DOCKER-USER -i enp0 -s 192.168.0.1/24 -m conntrack --ctorigdstport 8080 --ctdir ORIGINAL -j ACCEPT
```
* Change enp0 to your outer network interface's name.
* Change 192.168.0.1/24 to your subnet for your need.
* Change 8080 to your outer port.




* You can use whatever **container name** you wish.
* You can use any **port number** which not use on the host you like.
* You must place your **Google Api Key** inside env or this system is not going to work.
# Known Issue

1. There is no authority management yet, using host iptables to achive it now.
2. Sometime it may fail at Append or Insert , please try it again
3. Sometime Append and Insert will take more than 5 seconds, sinec the system is waiting for advertisement on youtube.
