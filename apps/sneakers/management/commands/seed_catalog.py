from django.core.management.base import BaseCommand
from apps.sneakers.models import Category, SneakerModel, SneakerSize, ProductImage
from apps.customizer.models import CustomDesign

class Command(BaseCommand):
    help = 'Seeds initial sneakers catalog, categories, sizes, and community 3D designs'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('[INFO] Seeding Sneakify database catalog...'))

        # 1. Categories
        categories_data = [
            {'name': 'Lifestyle & Casual', 'slug': 'lifestyle', 'description': 'Timeless everyday silhouettes reimagined with handcrafted luxury.'},
            {'name': 'Basketball Icons', 'slug': 'basketball', 'description': 'Court-ready heritage designs with responsive air cushioning.'},
            {'name': 'Skate & Street', 'slug': 'skate', 'description': 'Reinforced durable suede, padded collars, and grippy gum outsoles.'},
            {'name': 'Retro High-Tops', 'slug': 'high-tops', 'description': 'Ankle-wrapping statement classics with iconic checkmarks.'},
            {'name': 'Performance Running', 'slug': 'running', 'description': 'Ultra-lightweight mesh and engineered energy-return midsoles.'},
        ]

        categories = {}
        for cat in categories_data:
            obj, _ = Category.objects.get_or_create(slug=cat['slug'], defaults=cat)
            categories[cat['slug']] = obj

        self.stdout.write(self.style.SUCCESS(f'[OK] Created {len(categories)} categories.'))

        # 2. Sneaker Models
        sneakers_data = [
            {
                'name': 'Nike Air Force 1 Low',
                'slug': 'air-force-1-low',
                'sku': 'CW2288-111',
                'category': categories['lifestyle'],
                'gender': 'unisex',
                'base_price': 11495.00,
                'original_price': 13995.00,
                'description': 'The radiance lives on in the Nike Air Force 1 Low, the b-ball icon that puts a fresh spin on what you know best: crisp leather, bold colors and the perfect amount of flash to make you shine.',
                'details': [
                    'Stitched leather overlays on the upper add heritage style, durability and support',
                    'Originally designed for performance hoops, Nike Air cushioning adds lightweight comfort',
                    'Low-cut silhouette adds a clean, streamlined look',
                    'Padded collar feels soft and comfortable around the ankle',
                    'Perforations on the toe box for breathability',
                    'Solid rubber outsole with classic pivot circle pattern'
                ],
                'is_customizable': True,
                'is_bestseller': True,
                'is_featured': True,
                'is_new_release': False,
                'rating': 4.95,
                'review_count': 342,
            },
            {
                'name': 'Nike Dunk Low Retro',
                'slug': 'dunk-low-retro',
                'sku': 'DD1391-100',
                'category': categories['skate'],
                'gender': 'unisex',
                'base_price': 9995.00,
                'original_price': 11995.00,
                'description': 'Created for the hardwood but taken to the streets, the 80s icon returns with perfectly shined overlays and classic team colors.',
                'details': [
                    'Crisp leather upper with vintage basketball aesthetic',
                    'Foam midsole offers lightweight, responsive cushioning',
                    'Padded, low-cut collar looks sleek and feels comfortable',
                    'Bold color blocking adds standout street attitude',
                    'Rubber outsole with classic hoops pivot circle'
                ],
                'is_customizable': True,
                'is_bestseller': True,
                'is_featured': True,
                'is_new_release': True,
                'rating': 4.92,
                'review_count': 219,
            },
            {
                'name': 'Air Jordan 1 Mid SE',
                'slug': 'air-jordan-1-mid-se',
                'sku': 'FJ3458-160',
                'category': categories['basketball'],
                'gender': 'men',
                'base_price': 13295.00,
                'original_price': 15995.00,
                'description': 'Get that fresh AJ1 feeling every time you lace up. Premium leather and responsive Air cushioning keep your look iconic.',
                'details': [
                    'Encapsulated Air-Sole unit provides lightweight cushioning',
                    'Genuine leather in the upper offers durability and structure',
                    'Solid rubber outsole gives traction on a variety of surfaces',
                    'Wings logo stamped on ankle collar',
                    'Stitched-down Swoosh design'
                ],
                'is_customizable': True,
                'is_bestseller': True,
                'is_featured': True,
                'is_new_release': False,
                'rating': 4.88,
                'review_count': 184,
            },
            {
                'name': 'Nike Air Max 90 Future',
                'slug': 'air-max-90-future',
                'sku': 'DX4233-001',
                'category': categories['running'],
                'gender': 'unisex',
                'base_price': 12795.00,
                'original_price': 14995.00,
                'description': 'Nothing as fly, nothing as proven. The Nike Air Max 90 stays true to its OG roots with the iconic Waffle sole, stitched overlays and classic TPU accents.',
                'details': [
                    'Max Air unit in the heel adds unbelievable cushioning',
                    'Stitched overlays and TPU accents on the heel and eyestays add durability',
                    'Rubber Waffle outsole delivers traction and heritage style',
                    'Padded low-top collar feels soft and comfortable'
                ],
                'is_customizable': True,
                'is_bestseller': False,
                'is_featured': True,
                'is_new_release': True,
                'rating': 4.85,
                'review_count': 96,
            },
        ]

        sizes_list = ['UK 6', 'UK 6.5', 'UK 7', 'UK 7.5', 'UK 8', 'UK 8.5', 'UK 9', 'UK 9.5', 'UK 10', 'UK 10.5', 'UK 11', 'UK 12']

        for s_data in sneakers_data:
            sneaker, created = SneakerModel.objects.get_or_create(slug=s_data['slug'], defaults=s_data)
            
            # Add Sizes
            for size in sizes_list:
                SneakerSize.objects.get_or_create(
                    sneaker=sneaker,
                    size_uk=size,
                    defaults={'stock_quantity': 30}
                )

        self.stdout.write(self.style.SUCCESS(f'[OK] Created {len(sneakers_data)} sneaker models with UK size variants.'))

        # 3. Community 3D Designs
        af1 = SneakerModel.objects.get(slug='air-force-1-low')
        community_designs = [
            {
                'base_model': af1,
                'title': 'AF-1 Cyber Ember Edition',
                'configuration': {
                    'parts': {
                        'upper': {'color': '#111827', 'material': 'leather'},
                        'toebox': {'color': '#FAFAFA', 'material': 'leather'},
                        'swoosh': {'color': '#FF5722', 'material': 'leather'},
                        'midsole': {'color': '#FAFAFA', 'material': 'rubber'},
                        'laces': {'color': '#FF5722', 'material': 'flat'},
                        'tongue': {'color': '#111827', 'material': 'mesh'},
                        'outsole': {'color': '#0F172A', 'material': 'rubber'},
                    },
                    'text': {'content': 'EMBER', 'position': 'heel'},
                },
                'total_price': 12495.00,
                'is_public': True,
                'likes_count': 142,
            },
            {
                'base_model': af1,
                'title': 'AF-1 Royal Cobalt Frost',
                'configuration': {
                    'parts': {
                        'upper': {'color': '#1D4ED8', 'material': 'leather'},
                        'toebox': {'color': '#F3E9D2', 'material': 'suede'},
                        'swoosh': {'color': '#FAFAFA', 'material': 'patent'},
                        'midsole': {'color': '#FAFAFA', 'material': 'rubber'},
                        'laces': {'color': '#1D4ED8', 'material': 'flat'},
                        'tongue': {'color': '#1E293B', 'material': 'mesh'},
                        'outsole': {'color': '#1D4ED8', 'material': 'rubber'},
                    },
                    'text': {'content': 'FROST', 'position': 'heel'},
                },
                'total_price': 13295.00,
                'is_public': True,
                'likes_count': 89,
            },
        ]

        for d in community_designs:
            CustomDesign.objects.get_or_create(title=d['title'], defaults=d)

        self.stdout.write(self.style.SUCCESS('[SUCCESS] Sneakify catalog seeding completed successfully!'))
