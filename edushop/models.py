from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    LEVEL_CHOICES = (
        ('P1', 'Primary 1'), ('P2', 'Primary 2'), ('P3', 'Primary 3'), ('P4', 'Primary 4'), ('P5', 'Primary 5'), ('P6', 'Primary 6'), ('P7', 'Primary 7'),
        ('S1', 'Secondary 1'), ('S2', 'Secondary 2'), ('S3', 'Secondary 3'), ('S4', 'Secondary 4'), ('S5', 'Secondary 5'), ('S6', 'Secondary 6'),
        ('Tertiary', 'Tertiary/University'),
        ('General', 'General'),
    )

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    short_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    sku = models.CharField(max_length=100, unique=True, null=True, blank=True)
    is_digital = models.BooleanField(default=False)
    file = models.FileField(upload_to='product_files/', blank=True, null=True)
    author = models.CharField(max_length=255, blank=True)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='Beginner')
    language = models.CharField(max_length=50, default='English')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
