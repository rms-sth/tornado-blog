import datetime
from peewee import *

db = PostgresqlDatabase(
    "blog_tornado", user="blog_tornado", password="blog_tornado", host="127.0.0.1",
)


class Blog(Model):
    title = CharField(max_length=200)
    text = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    published_date = DateTimeField(null=True)

    class Meta:
        database = db  # This model uses the "people.db" database.


db.connect()

db.create_tables([Blog])
