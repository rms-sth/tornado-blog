import datetime
from models import Blog, User
import hashlib

password = hashlib.md5("ramesh123".encode()).hexdigest()
author = User.create(
    username="ramesrest",
    email="ramesrest@gmail.com",
    password=password,
    first_name="Ramesh",
    last_name="Pradhan",
    is_superuser=True,
)

blog1 = Blog(author=author, title="New Blog 1", text="New Blog 1")
blog2 = Blog(author=author, title="New Blog 2", text="New Blog 2")
blog3 = Blog(author=author, title="New Blog 3", text="New Blog 3")

blog1.save()
blog2.save()
blog3.save()

