import tornado.web
import json
from models.models import User, Product, Order

class DashboardHandler(tornado.web.RequestHandler):
    async def get(self):
        # Fetch real counts from DB
        user_count = await User.all().count()
        product_count = await Product.all().count()
        order_count = await Order.all().count()
        total_revenue = 45231 # Placeholder for now
        
        # Simulating trend data for Chart.js
        revenue_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        revenue_data = [1200, 1900, 1500, 2100, 1800, 2400, 2100]
        
        signup_labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
        signup_data = [10, 25, 40, 46] # Matches our user_count of 46
        
        self.render("dashboard.html", 
                    title="Administrator Dashboard",
                    user_count=user_count,
                    product_count=product_count,
                    order_count=order_count,
                    class_bookings=89, # Placeholder
                    total_revenue=f"${total_revenue:,}",
                    revenue_labels_json=json.dumps(revenue_labels),
                    revenue_data_json=json.dumps(revenue_data),
                    signup_labels_json=json.dumps(signup_labels),
                    signup_data_json=json.dumps(signup_data)
                   )
