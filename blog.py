import os

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.web import Application
from tornado.options import define, options

from models import Blog

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", BlogList),
            (r"/blog-detail/([0-9Xx\-]+)/", BlogDetail),
        ]
        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class BlogList(tornado.web.RequestHandler):
    def get(self):
        blogs = Blog.select()
        self.render("blog_list.html", blogs=blogs)


class BlogDetail(tornado.web.RequestHandler):
    def get(self, id):
        blog = Blog.select().where(Blog.id==id).get()
        self.render("blog_detail.html", blog=blog)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
