import tornado.ioloop
import tornado.web
import message
import os
import select
from tornado.options import define, options
import tornado.escape
import tornado.options
import json
from  tornado.escape import json_decode
from  tornado.escape import json_encode
from tornado.options import define, options
from multiprocessing.connection import Listener


class StatusHandler(tornado.web.RequestHandler):

    def get(self):
        current_path=os.path.dirname(os.path.abspath(__file__))
        msg=message.create_msg(str({"url":"","action":"rtstate"}).encode("utf-8"))
        try:
            command_pipe=os.open(current_path+"/command.pipe",os.O_WRONLY|os.O_NONBLOCK)
            os.write(command_pipe,msg)
            reader=Listener(('localhost',6000))
            conn=reader.accept()
            rtmsg=conn.recv()
            reader.close()
        except:
            print("Player_Interface isn't running.")
            rtmsg={"MusicInfoDict": {}, "Playlist": [], "Status": ["Stop", 0], "NowPlaying": -1}
        self.write(rtmsg)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="Rteslab Music Player")
    def post(self):
        current_path=os.path.dirname(os.path.abspath(__file__))
        if len(self.request.body)<200:
            msg=message.create_msg(self.request.body)
            try:
                command_pipe=os.open(current_path+"/command.pipe",os.O_WRONLY|os.O_NONBLOCK)
                os.write(command_pipe,msg)
            except:
                print("Player_Interface isn't running.")
        else:
            print("Wrong message format:Too Long")

        

define("port", default=80, help="run on the given port", type=int)
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/retstate", StatusHandler),
        ]
        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )
        tornado.web.Application.__init__(self, handlers, **settings)
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
