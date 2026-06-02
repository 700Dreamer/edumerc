import tornado.web
from models.models import CoachingSession

class SessionsHandler(tornado.web.RequestHandler):
    async def get(self):
        sessions = await CoachingSession.all().prefetch_related("coach", "student").order_by("-start_time")
        self.render("sessions.html", title="Coaching Sessions", sessions=sessions)
