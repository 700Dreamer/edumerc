import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from edushop.models import Category, Product

# Ensure categories exist
categories_data = [
    ('textbooks', 'Textbooks'),
    ('stationery', 'Stationery'),
    ('uniforms', 'Uniforms & Apparel'),
    ('digital', 'Digital Resources'),
    ('lab-equipment', 'Lab Equipment'),
]

cats = {}
for slug, name in categories_data:
    cat, created = Category.objects.get_or_create(slug=slug, defaults={'name': name, 'is_active': True})
    cats[slug] = cat
    if created:
        print(f"  Created category: {name}")
    else:
        print(f"  Category exists: {name}")

products = [
    # Textbooks
    {
        'category': cats['textbooks'], 'title': 'MK Primary Mathematics P4',
        'description': 'Comprehensive mathematics textbook for Primary 4 students covering arithmetic, geometry, and basic algebra. Aligned with the Uganda National Curriculum.',
        'short_description': 'P4 Maths textbook aligned to national curriculum.',
        'price': 25000, 'discount_price': 20000, 'stock': 150, 'sku': 'TXT-MATH-P4-001',
        'is_digital': False, 'author': 'MK Publishers', 'level': 'P4', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['textbooks'], 'title': 'Fountain English Grammar S1',
        'description': 'A detailed English grammar textbook for Senior 1 students. Covers parts of speech, sentence structure, comprehension, and essay writing.',
        'short_description': 'S1 English grammar & comprehension.',
        'price': 35000, 'discount_price': 30000, 'stock': 120, 'sku': 'TXT-ENG-S1-001',
        'is_digital': False, 'author': 'Fountain Publishers', 'level': 'S1', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['textbooks'], 'title': 'Understanding Physics S3-S4',
        'description': 'Physics textbook covering mechanics, electricity, magnetism, and waves for S3 and S4 students preparing for UCE exams.',
        'short_description': 'Physics for UCE preparation.',
        'price': 45000, 'discount_price': 38000, 'stock': 80, 'sku': 'TXT-PHY-S34-001',
        'is_digital': False, 'author': 'Dr. James Kiggundu', 'level': 'S3', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['textbooks'], 'title': 'Biology for East Africa S5-S6',
        'description': 'Advanced biology textbook for A-Level students. Covers cell biology, genetics, ecology, and human physiology with practical experiment guides.',
        'short_description': 'A-Level Biology with practicals.',
        'price': 55000, 'discount_price': 48000, 'stock': 60, 'sku': 'TXT-BIO-S56-001',
        'is_digital': False, 'author': 'Prof. Mary Nakabugo', 'level': 'S5', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['textbooks'], 'title': 'Primary Science P6 Revision Guide',
        'description': 'Revision guide for Primary 6 science covering living things, matter, energy, and the environment. Includes PLE past papers.',
        'short_description': 'P6 Science revision with PLE past papers.',
        'price': 18000, 'discount_price': 15000, 'stock': 200, 'sku': 'TXT-SCI-P6-001',
        'is_digital': False, 'author': 'Kampala Education Press', 'level': 'P6', 'language': 'English', 'is_active': True,
    },
    # Stationery
    {
        'category': cats['stationery'], 'title': 'Counter Book 96 Pages (Pack of 5)',
        'description': 'High-quality ruled counter books, 96 pages each. Perfect for note-taking in class. Durable cover and smooth paper.',
        'short_description': 'Pack of 5 ruled counter books.',
        'price': 15000, 'discount_price': 12000, 'stock': 500, 'sku': 'STA-CBOOK-96-005',
        'is_digital': False, 'author': '', 'level': 'General', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['stationery'], 'title': 'Mathematical Instruments Set',
        'description': 'Complete geometry set with compass, protractor, set squares, ruler, and pencil. Essential for S1-S4 mathematics and technical drawing.',
        'short_description': 'Full geometry set for secondary students.',
        'price': 12000, 'discount_price': 10000, 'stock': 300, 'sku': 'STA-MATH-SET-001',
        'is_digital': False, 'author': '', 'level': 'General', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['stationery'], 'title': 'Bic Biro Pens Blue (Box of 50)',
        'description': 'Box of 50 blue Bic ballpoint pens. Smooth ink flow, long-lasting, and comfortable grip. Ideal for everyday school use.',
        'short_description': 'Box of 50 blue ballpoint pens.',
        'price': 25000, 'discount_price': 22000, 'stock': 400, 'sku': 'STA-PEN-BLU-050',
        'is_digital': False, 'author': '', 'level': 'General', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['stationery'], 'title': 'A4 Printing Paper (Ream of 500)',
        'description': 'Premium A4 white printing paper, 80gsm. Suitable for printing assignments, notes, and exam papers.',
        'short_description': '500 sheets of A4 printing paper.',
        'price': 28000, 'discount_price': 25000, 'stock': 250, 'sku': 'STA-A4-PAPER-500',
        'is_digital': False, 'author': '', 'level': 'General', 'language': 'English', 'is_active': True,
    },
    # Uniforms
    {
        'category': cats['uniforms'], 'title': 'White School Shirt (Size M)',
        'description': 'Premium cotton white school shirt, size Medium. Breathable fabric, reinforced buttons, and durable stitching. Fits ages 10-13.',
        'short_description': 'White cotton school shirt, size M.',
        'price': 20000, 'discount_price': 18000, 'stock': 100, 'sku': 'UNI-SHIRT-WHT-M',
        'is_digital': False, 'author': '', 'level': 'General', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['uniforms'], 'title': 'Navy Blue School Shorts (Size L)',
        'description': 'Durable navy blue school shorts, size Large. Made with strong twill fabric and elastic waistband. Ideal for primary school students.',
        'short_description': 'Navy blue shorts, size L.',
        'price': 18000, 'discount_price': 15000, 'stock': 120, 'sku': 'UNI-SHORT-NVY-L',
        'is_digital': False, 'author': '', 'level': 'General', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['uniforms'], 'title': 'Black School Shoes (Size 38)',
        'description': 'Polished black leather school shoes, size 38. Comfortable insole, non-slip sole, and classic design suitable for all schools.',
        'short_description': 'Black leather school shoes, size 38.',
        'price': 65000, 'discount_price': 55000, 'stock': 80, 'sku': 'UNI-SHOE-BLK-38',
        'is_digital': False, 'author': '', 'level': 'General', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['uniforms'], 'title': 'School Backpack (30L)',
        'description': 'Spacious 30-litre school backpack with padded shoulder straps, multiple compartments, and water bottle holder. Available in black.',
        'short_description': '30L black school backpack.',
        'price': 45000, 'discount_price': 40000, 'stock': 90, 'sku': 'UNI-BAG-BLK-30L',
        'is_digital': False, 'author': '', 'level': 'General', 'language': 'English', 'is_active': True,
    },
    # Digital Resources
    {
        'category': cats['digital'], 'title': 'PLE Mathematics Past Papers (2015-2025)',
        'description': 'Complete collection of PLE Mathematics past papers from 2015 to 2025 with detailed marking guides and step-by-step solutions.',
        'short_description': '10 years of PLE Maths past papers with solutions.',
        'price': 10000, 'discount_price': 8000, 'stock': 9999, 'sku': 'DIG-PLE-MATH-PP',
        'is_digital': True, 'author': 'EduMerk Digital', 'level': 'P7', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['digital'], 'title': 'UCE Chemistry Video Lessons (S3-S4)',
        'description': 'Over 60 video lessons covering the entire UCE Chemistry syllabus. Includes organic chemistry, chemical bonding, acids and bases.',
        'short_description': '60+ video lessons for UCE Chemistry.',
        'price': 30000, 'discount_price': 25000, 'stock': 9999, 'sku': 'DIG-UCE-CHEM-VID',
        'is_digital': True, 'author': 'Dr. Patrick Ssemwogerere', 'level': 'S3', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['digital'], 'title': 'UACE Economics Study Notes',
        'description': 'Comprehensive A-Level Economics notes covering microeconomics, macroeconomics, and development economics. PDF format with diagrams.',
        'short_description': 'A-Level Economics PDF study notes.',
        'price': 15000, 'discount_price': 12000, 'stock': 9999, 'sku': 'DIG-UACE-ECON-PDF',
        'is_digital': True, 'author': 'Mr. Ronald Kasule', 'level': 'S5', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['digital'], 'title': 'Interactive Luganda Lessons for P1-P3',
        'description': 'Fun and interactive digital Luganda lessons for lower primary students. Includes audio pronunciation, vocabulary games, and reading exercises.',
        'short_description': 'Interactive Luganda for lower primary.',
        'price': 12000, 'discount_price': 10000, 'stock': 9999, 'sku': 'DIG-LUG-P13-INT',
        'is_digital': True, 'author': 'EduMerk Digital', 'level': 'P1', 'language': 'Luganda', 'is_active': True,
    },
    # Lab Equipment
    {
        'category': cats['lab-equipment'], 'title': 'Chemistry Lab Starter Kit',
        'description': 'Essential chemistry lab kit including beakers, test tubes, Bunsen burner, litmus paper, and safety goggles. Perfect for S1-S2 practicals.',
        'short_description': 'Basic chemistry lab equipment set.',
        'price': 120000, 'discount_price': 100000, 'stock': 30, 'sku': 'LAB-CHEM-KIT-001',
        'is_digital': False, 'author': '', 'level': 'S1', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['lab-equipment'], 'title': 'Student Microscope (40x-1000x)',
        'description': 'High-quality student microscope with 40x, 100x, 400x, and 1000x magnification. LED illumination, metal body, and carrying case included.',
        'short_description': 'Student microscope with LED light.',
        'price': 250000, 'discount_price': 220000, 'stock': 25, 'sku': 'LAB-MICRO-1000X',
        'is_digital': False, 'author': '', 'level': 'S3', 'language': 'English', 'is_active': True,
    },
    {
        'category': cats['lab-equipment'], 'title': 'Physics Spring Balance Set (5 pcs)',
        'description': 'Set of 5 spring balances with different ranges (1N, 2.5N, 5N, 10N, 20N). Essential for mechanics practicals in secondary school physics.',
        'short_description': 'Set of 5 spring balances for physics.',
        'price': 45000, 'discount_price': 40000, 'stock': 50, 'sku': 'LAB-PHY-SPRING-5',
        'is_digital': False, 'author': '', 'level': 'S2', 'language': 'English', 'is_active': True,
    },
]

created_count = 0
skipped_count = 0
for p in products:
    if Product.objects.filter(sku=p['sku']).exists():
        skipped_count += 1
        continue
    Product.objects.create(**p)
    created_count += 1

print(f"\nDone! Created {created_count} products, skipped {skipped_count} (already exist).")
