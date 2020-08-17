from models import Blog
import datetime

blog1 = Blog(title="New Blog 1", text="New Blog 1")
blog2 = Blog(title="New Blog 2", text="New Blog 2")
blog3 = Blog(title="New Blog 3", text="New Blog 3")

blog1.save()
blog2.save()
blog3.save()

