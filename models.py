import asyncio
import datetime

import peewee_async
from peewee import Model, CharField, TextField, DateTimeField

db = peewee_async.PostgresqlDatabase(
    "blog_tornado", user="blog_tornado", password="blog_tornado", host="127.0.0.1",
)


class Blog(Model):
    title = CharField(max_length=200)
    text = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    published_date = DateTimeField(null=True)

    class Meta:
        database = db

    def __str__(self):
        return self.title


##########################################################################################
###############                     Sync Peeweee
##########################################################################################
# Sync code
# db.connect()
# db.create_tables([Blog])

# Blog.create_table(True)
# Blog.create(title="Yo, I can do it sync!",text="Yo, I can do it sync!")
# db.close()


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
