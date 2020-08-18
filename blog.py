import os

from peewee_async import Manager

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define, options
from tornado.web import url

from models import Blog, db

define("port", default=8000, help="run on the given port", type=int)


class BlogList(tornado.web.RequestHandler):
    async def get(self):
        query = Blog.select().order_by(Blog.created_date.desc())
        blogs = await self.application.objects.execute(query)
        self.render("blog_list.html", blogs=blogs)


class BlogDetail(tornado.web.RequestHandler):
    async def get(self, id):
        blog = await self.application.objects.get(Blog, id=id)
        self.render("blog_detail.html", blog=blog)


class BlogCreate(tornado.web.RequestHandler):
    async def get(self, id=None):
        blog = dict()
        if id:
            blog = await self.application.objects.get(Blog, id=id)
        self.render("blog_create.html", blog=blog)

    async def post(self, id=None):
        title = self.get_argument("title")
        text = self.get_argument("text")
        if id:
            blog = await self.application.objects.get(Blog, id=id)
            blog.title = title
            blog.text = text
            blog = await self.application.objects.update(blog)
            return self.redirect(self.reverse_url("blog_detail", id))
        blog = await self.application.objects.create(Blog, title=title, text=text)
        self.redirect(self.reverse_url("blog_detail", blog.id))


if __name__ == "__main__":
    tornado.options.parse_command_line()

    handlers = [
        url(r"/", BlogList, name="blog_list"),
        url(r"/blog-detail/([0-9Xx\-]+)/", BlogDetail, name="blog_detail"),
        url(r"/blog-create/", BlogCreate, name="blog_create"),
        url(r"/blog-edit/([0-9Xx\-]+)/", BlogCreate, name="blog_edit"),
    ]

    settings = dict(
        debug=True, template_path=os.path.join(os.path.dirname(__file__), "templates"),
    )

    app = tornado.web.Application(handlers, **settings)
    app.listen(options.port)

    # allowing Peewee to perform only async operation
    db.set_allow_sync(False)
    app.objects = Manager(db)

    tornado.ioloop.IOLoop.current().start()
