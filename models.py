import asyncio
import datetime
from enum import unique

import peewee_async
from peewee import ForeignKeyField, Model, CharField, TextField, DateTimeField
from wtforms.fields.core import BooleanField

db = peewee_async.PostgresqlDatabase(
    "blog_tornado", user="blog_tornado", password="blog_tornado", host="127.0.0.1",
)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(max_length=20, unique=True)
    email = CharField(max_length=50, unique=True)
    password = CharField()
    first_name = CharField(max_length=20)
    middle_name = CharField(max_length=20, null=True)
    last_name = CharField(max_length=20)
    created_at = DateTimeField(default=datetime.datetime.now)
    is_active = BooleanField(default=True)
    is_superuser = BooleanField(default=False)
    last_login = DateTimeField(null=True)

    def __str__(self):
        return self.username

class Blog(BaseModel):
    author = ForeignKeyField(User, backref='blogs')
    title = CharField(max_length=200)
    text = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(null=True)
    published_date = DateTimeField(null=True)

    def __str__(self):
        return self.title


##########################################################################################
###############                     Sync Peeweee
##########################################################################################
# Sync code
# db.connect()
# # # creating table
# db.create_tables([User, Blog])
# # # deleting table
# # db.drop_tables([User,Blog])
# db.close()

# Blog.create_table(True)
# Blog.create(title="Yo, I can do it sync!",text="Yo, I can do it sync!")
# Blog.drop_table(True)


##########################################################################################
###############                     Async Peeweee
##########################################################################################
# loop = asyncio.new_event_loop()

# # Create async models manager:
# objects = peewee_async.Manager(db, loop=loop)

# # this code is sync, because for creating/dropping table its good to perform sync operation
# Blog.create_table(True)


# objects.database.allow_sync = False  # this will raise AssertionError on ANY sync call


# async def create_or_get_blog():
#     # Add new Blog
#     await objects.create_or_get(
#         Blog, title="title", text="Peewee is AWESOME with async!"
#     )

#     # Get one by title
#     blog = await objects.get(Blog, title="title")
#     print("Was:", blog.text)

#     # Save with new text
#     blog.text = "Peewee is SUPER awesome with async!"
#     await objects.update(blog)
#     print("New:", blog.text)


# loop.run_until_complete(create_or_get_blog())
# loop.close()

# # Clean up, can do it sync again:
# with objects.allow_sync():
#     Blog.drop_table(True)
