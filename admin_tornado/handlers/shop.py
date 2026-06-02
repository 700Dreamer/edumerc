import tornado.web
from models.models import Product

class ShopHandler(tornado.web.RequestHandler):
    async def get(self):
        products = await Product.all().prefetch_related("category").order_by("-created_at")
        self.render("shop.html", title="EduShop Management", products=products)
