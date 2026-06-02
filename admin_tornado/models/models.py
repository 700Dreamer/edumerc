from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=150, unique=True)
    email = fields.CharField(max_length=254, unique=True)
    first_name = fields.CharField(max_length=150, null=True)
    last_name = fields.CharField(max_length=150, null=True)
    role = fields.CharField(max_length=10, default="STUDENT")
    is_coach = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    date_joined = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users_user"

class Profile(models.Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField("models.User", related_name="profile", on_delete=fields.CASCADE)
    bio = fields.TextField(null=True)
    avatar = fields.CharField(max_length=100, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "users_profile"

class Category(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    slug = fields.CharField(max_length=255, unique=True)
    is_active = fields.BooleanField(default=True)

    class Meta:
        table = "edushop_category"

class Product(models.Model):
    id = fields.IntField(pk=True)
    category = fields.ForeignKeyField("models.Category", related_name="products")
    title = fields.CharField(max_length=255)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    stock = fields.IntField(default=0)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "edushop_product"

class Order(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="orders")
    total_price = fields.DecimalField(max_digits=10, decimal_places=2)
    status = fields.CharField(max_length=20, default="Pending")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "edushop_order"

class Coach(models.Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField("models.User", related_name="coach_profile")
    title = fields.CharField(max_length=255)
    price_per_hour = fields.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = fields.BooleanField(default=True)
    rating = fields.DecimalField(max_digits=3, decimal_places=2, default=5.00)

    class Meta:
        table = "educoach_coach"

class CoachingSession(models.Model):
    id = fields.BigIntField(pk=True)
    coach = fields.ForeignKeyField("models.Coach", related_name="sessions")
    student = fields.ForeignKeyField("models.User", related_name="booked_sessions")
    date = fields.DateField()
    start_time = fields.TimeField()
    end_time = fields.TimeField(null=True)
    duration = fields.IntField(default=1)
    status = fields.CharField(max_length=20, default="pending")
    booking_id = fields.CharField(max_length=100, unique=True, null=True)
    total_price = fields.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        table = "educoach_coachingsession"
