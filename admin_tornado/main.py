import os
import tornado.ioloop
import tornado.web
from dotenv import load_dotenv
from tortoise import Tortoise

# Load environment variables
load_dotenv()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("dashboard.html", title="Administrator Dashboard")

class AuthHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

from handlers.dashboard import DashboardHandler
from handlers.users import UsersHandler
from handlers.shop import ShopHandler
from handlers.coach import CoachHandler
from handlers.orders import OrdersHandler
from handlers.sessions import SessionsHandler

def make_app():
    return tornado.web.Application([
        (r"/", DashboardHandler),
        (r"/users", UsersHandler),
        (r"/shop", ShopHandler),
        (r"/coach", CoachHandler),
        (r"/orders", OrdersHandler),
        (r"/sessions", SessionsHandler),
    ],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True)

async def init_db():
    db_url = os.getenv("DB_URL")
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['models.models']}
    )

if __name__ == "__main__":
    app = make_app()
    port = int(os.getenv("PORT", 8888))
    
    # Run DB initialization in the same loop
    loop = tornado.ioloop.IOLoop.current()
    loop.run_sync(init_db)
    
    print(f"Tornado Admin Dashboard starting on http://localhost:{port}")
    app.listen(port)
    loop.start()
