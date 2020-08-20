import datetime
import os
from hashlib import md5

from peewee_async import Manager

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define, options
from tornado.web import url

from models import Blog, User, db
from forms import BlogForm, LoginForm

define("port", default=8000, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")


class Login(BaseHandler):
    form = LoginForm

    async def get(self):
        self.render("login.html", form=self.form())

    async def post(self):
        username = self.get_argument("username")
        password = md5(self.get_argument("password").encode()).hexdigest()
        form = self.form(username=username, password=password)
        if form.validate():
            query = User.select().where(
                User.username == username, User.password == password
            )
            user = await self.application.objects.execute(query)
            if user:
                user = await self.application.objects.get(
                    User, username=username, password=password
                )
                self.set_secure_cookie("username", username)
                self.redirect(self.reverse_url("blog_list"))
            return self.render("login.html", form=form)


class Logout(BaseHandler):
    async def get(self):
        self.clear_cookie("username")
        self.redirect(self.reverse_url("login"))


class BlogList(BaseHandler):
    async def get(self):
        query = Blog.select().order_by(Blog.created_at.desc())
        blogs = await self.application.objects.execute(query)
        self.render("blog_list.html", blogs=blogs)


class BlogDetail(BaseHandler):
    async def get(self, id):
        blog = await self.application.objects.get(Blog, id=id)
        self.render("blog_detail.html", blog=blog)


class BlogCreate(BaseHandler):
    @tornado.web.authenticated
    async def get(self, id=None):
        form = BlogForm()
        blog = dict()
        if id:
            blog = await self.application.objects.get(Blog, id=id)
            form = BlogForm(title=blog.title, text=blog.text)
        self.render("blog_create.html", blog=blog, form=form)

    @tornado.web.authenticated
    async def post(self, id=None):
        title = self.get_argument("title")
        text = self.get_argument("text")

        form = BlogForm(title=title, text=text)
        if form.validate():
            if id:
                blog = await self.application.objects.get(Blog, id=id)
                blog.title = title
                blog.text = text
                blog.updated_at = datetime.datetime.now()
                await self.application.objects.update(blog)
                return self.redirect(self.reverse_url("blog_detail", id))
            blog = await self.application.objects.create(Blog, title=title, text=text)
            return self.redirect(self.reverse_url("blog_detail", blog.id))
        return self.render("blog_create.html", form=form)


class BlogDelete(tornado.web.RequestHandler):
    @tornado.web.authenticated
    async def get(self, id):
        self.render("blog_delete.html", id=id)

    @tornado.web.authenticated
    async def post(self, id):
        query = Blog.delete().where(Blog.id == id)
        await self.application.objects.execute(query)
        self.redirect(self.reverse_url("blog_list"))


if __name__ == "__main__":
    tornado.options.parse_command_line()

    handlers = [
        url(r"/login/", Login, name="login"),
        url(r"/logout/", Logout, name="logout"),
        url(r"/", BlogList, name="blog_list"),
        url(r"/blog-detail/([0-9Xx\-]+)/", BlogDetail, name="blog_detail"),
        url(r"/blog-create/", BlogCreate, name="blog_create"),
        url(r"/blog-edit/([0-9Xx\-]+)/", BlogCreate, name="blog_edit"),
        url(r"/blog-delete/([0-9Xx\-]+)/", BlogDelete, name="blog_delete"),
    ]

    settings = dict(
        debug=True,
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        cookie_secret="ZiZ7g6ktROSTVnzyNrRXGOoDctoGrEd+j2mfyAAtgY4=",
        login_url="/login/",
    )

    app = tornado.web.Application(handlers, **settings)
    app.listen(options.port)

    # allowing Peewee to perform only async operation
    db.set_allow_sync(False)
    app.objects = Manager(db)

    tornado.ioloop.IOLoop.current().start()
