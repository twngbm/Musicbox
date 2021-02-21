import flask
from flask import Flask, render_template, request
import multiprocessing
import time
import MusicPlayer
import json
import logging
import os
app = Flask(__name__)
app.config['REDIS_URL'] = "redis://0.0.0.0:5000"


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/action', methods=['POST'])
def submit():
    data = request.get_data()
    clientData = json.loads(data.decode('utf-8'))
    logging.info(f"{request.remote_addr}>->->{clientData}")
    q1.put(clientData, block=False)

    return {}, 200


@app.route('/send')
def send():
    def eventStream():
        while True:
            try:
                statusContent = q2.get(block=True, timeout=5)
            except:
                continue
            data = json.dumps(statusContent)
            yield f'data: {data}\n\n'
    return flask.Response(eventStream(), mimetype='text/event-stream')


if __name__ == "__main__":
    os.environ['VLC_VERBOSE'] = "0"
    formatter = '| %(levelname)s | %(asctime)s |  %(message)s |'
    ch = logging.StreamHandler()
    logging.basicConfig(level=logging.INFO, format=formatter,
                        datefmt="%Y-%m-%d %H:%M:%S", handlers=[ch])
    q1 = multiprocessing.Queue()
    q2 = multiprocessing.Queue()
    p = multiprocessing.Process(
        target=MusicPlayer.playerInterface, args=(q1, q2,), daemon=True)
    p.start()
    app.run(host="0.0.0.0", port="5000")
