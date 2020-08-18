import os

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.web import Application
from tornado.options import define, options
from tornado.web import url

from models import Blog

define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            url(r"/", BlogList, name="blog_list"),
            url(r"/blog-detail/([0-9Xx\-]+)/", BlogDetail, name="blog_detail"),
            url(r"/blog-create/", BlogCreate, name="blog_create"),
            url(r"/blog-edit/([0-9Xx\-]+)/", BlogCreate, name="blog_edit"),
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
        blog = Blog.select().where(Blog.id == id).get()
        self.render("blog_detail.html", blog=blog)


class BlogCreate(tornado.web.RequestHandler):
    def get(self, id=None):
        blog = dict()
        if id:
            blog = Blog.select().where(Blog.id == id).get()
        self.render("blog_create.html", blog=blog)

    def post(self, id=None):
        title = self.get_argument("title")
        text = self.get_argument("text")
        if id:
            blog = Blog.select().where(Blog.id == id).get()
            blog.title = title
            blog.text = text
            blog.save()
            return self.redirect(self.reverse_url("blog_detail", blog.id))
        blog = Blog.create(title=title, text=text)
        self.redirect(self.reverse_url("blog_detail", blog.id))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
