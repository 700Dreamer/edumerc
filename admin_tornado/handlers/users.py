import tornado.web
from models.models import User

class UsersHandler(tornado.web.RequestHandler):
    async def get(self):
        users = await User.all().order_by("-date_joined").limit(50)
        self.render("users.html", title="Users & Roles", users=users)
