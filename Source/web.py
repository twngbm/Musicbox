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
        rtmsg=""
        command={"url":"","action":"rtstate"}
        playlist_pipe=os.open("/Youtube_Player/playlist.pipe",os.O_WRONLY)
        msg=message.create_msg(command)
        os.write(playlist_pipe,msg)
        reader=Listener(('localhost',6000))
        conn=reader.accept()
        rtmsg=conn.recv()
        #status_pipe=os.open("/Youtube_Player/status.pipe",os.O_RDONLY | os.O_NONBLOCK )    
        #poll=select.poll()
        #poll.register(status_pipe,select.POLLIN)
        #if (status_pipe,select.POLLIN) in poll.poll(4000):
        #    rtmsg=message.get_message(status_pipe)
        #rtmsg=rtmsg.replace("'",'"')
        #print(json.dumps(rtmsg))
        self.write(rtmsg)

class MainHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("index.html", title="Rteslab Music Player")
    def post(self):
        json_obj=json_decode(self.request.body)
        url=json_obj['URL']
        action=json_obj['ACTION']
        command={"url":url,"action":action}
        playlist_pipe=os.open("/Youtube_Player/playlist.pipe",os.O_WRONLY)
        
        msg=message.create_msg(command)
        os.write(playlist_pipe,msg)
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
