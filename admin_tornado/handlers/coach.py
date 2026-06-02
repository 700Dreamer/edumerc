import tornado.web
from models.models import Coach

class CoachHandler(tornado.web.RequestHandler):
    async def get(self):
        coaches = await Coach.all().prefetch_related("user").order_by("-rating")
        self.render("coach.html", title="EduCoach Management", coaches=coaches)
