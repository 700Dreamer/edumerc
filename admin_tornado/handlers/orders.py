import tornado.web
from models.models import Order

class OrdersHandler(tornado.web.RequestHandler):
    async def get(self):
        orders = await Order.all().prefetch_related("user").order_by("-created_at")
        self.render("orders.html", title="Order Management", orders=orders)
