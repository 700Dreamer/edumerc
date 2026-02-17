import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from edushop.models import Category, Product
from django.core.files import File

# Get categories
textbooks = Category.objects.get(slug='textbooks')
stationery = Category.objects.get(slug='stationery')

# Create placeholder image files (you can replace these with actual images later)
products_with_images = [
    {
        'category': textbooks,
        'title': 'My First Atlas of Uganda',
        'description': 'A colorful and engaging atlas designed for primary school students. Features detailed maps of Uganda showing districts, major cities, rivers, lakes, and national parks. Includes fun facts about Ugandan culture, wildlife, and landmarks. Perfect for Social Studies and Geography lessons.',
        'short_description': 'Colorful Uganda atlas for primary students.',
        'price': 22000,
        'discount_price': 18000,
        'stock': 150,
        'sku': 'TXT-ATLAS-UG-001',
        'is_digital': False,
        'author': 'Uganda Education Publishers',
        'level': 'P4',
        'language': 'English',
        'is_active': True,
        'image_placeholder': 'products/placeholder_atlas.txt',
    },
    {
        'category': stationery,
        'title': 'Casio FX-82MS Scientific Calculator',
        'description': 'Advanced scientific calculator with 240 functions including trigonometry, statistics, and calculus. Two-line display, solar and battery powered. Essential for S3-S6 mathematics and physics. Approved for UCE and UACE exams.',
        'short_description': 'Scientific calculator for secondary students.',
        'price': 45000,
        'discount_price': 40000,
        'stock': 75,
        'sku': 'STA-CALC-FX82-001',
        'is_digital': False,
        'author': 'Casio',
        'level': 'S3',
        'language': 'English',
        'is_active': True,
        'image_placeholder': 'products/placeholder_calculator.txt',
    },
]

created_count = 0
for p_data in products_with_images:
    sku = p_data.pop('sku')
    image_path = p_data.pop('image_placeholder')
    
    if Product.objects.filter(sku=sku).exists():
        print(f"  Skipped: {p_data['title']} (already exists)")
        continue
    
    # Create product
    product = Product.objects.create(sku=sku, **p_data)
    
    # Attach placeholder image
    if os.path.exists(f'media/{image_path}'):
        with open(f'media/{image_path}', 'rb') as f:
            product.image.save(os.path.basename(image_path), File(f), save=True)
    
    created_count += 1
    print(f"  Created: {product.title} (with image)")

print(f"\nDone! Created {created_count} products with images.")
print("\nNote: Placeholder text files were used. Replace them with actual images by:")
print("  1. Upload real images to: e:\\kizito\\cop_e\\API\\e_cop\\src\\media\\products\\")
print("  2. Update the products in Django admin to use the real images")
