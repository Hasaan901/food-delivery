from django.core.management.base import BaseCommand
from tracker.models import Restaurant, FoodItem

class Command(BaseCommand):
    help = 'Seeds mock restaurants and food items for the Foodpanda catalog with Rupees and static images.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding BiteDash catalog data...")

        # Clear existing catalog to prevent duplicate accumulates if re-run
        FoodItem.objects.all().delete()
        Restaurant.objects.all().delete()

        # 1. Burger Loft
        r1 = Restaurant.objects.create(
            name="Burger Loft",
            cuisine="Burgers & American",
            rating=4.8,
            delivery_time="15-25 min",
            delivery_fee=40.00,
            image_url="/static/tracker/images/burger.png"
        )
        FoodItem.objects.create(
            restaurant=r1,
            name="Classic Cheeseburger",
            price=250.00,
            description="Juicy beef patty, melted cheddar cheese, lettuce, tomato, and house burger sauce.",
            image_url="/static/tracker/images/burger.png"
        )
        FoodItem.objects.create(
            restaurant=r1,
            name="Smoky BBQ Bacon Burger",
            price=350.00,
            description="Crispy bacon, smoky BBQ sauce, golden onion rings, and double cheddar cheese.",
            image_url="/static/tracker/images/burger.png"
        )
        FoodItem.objects.create(
            restaurant=r1,
            name="Truffle Parmesan Fries",
            price=150.00,
            description="Crispy golden fries tossed in white truffle oil and freshly grated parmesan cheese.",
            image_url="/static/tracker/images/burger.png"
        )

        # 2. Pizza Napoli
        r2 = Restaurant.objects.create(
            name="Pizza Napoli",
            cuisine="Italian & Pizza",
            rating=4.6,
            delivery_time="20-30 min",
            delivery_fee=60.00,
            image_url="/static/tracker/images/pizza.png"
        )
        FoodItem.objects.create(
            restaurant=r2,
            name="Margherita Pizza",
            price=450.00,
            description="Fresh mozzarella, san marzano tomato sauce, fresh basil, and extra virgin olive oil.",
            image_url="/static/tracker/images/pizza.png"
        )
        FoodItem.objects.create(
            restaurant=r2,
            name="Pepperoni Feast Pizza",
            price=550.00,
            description="Loaded with double pepperoni, mozzarella cheese, and rich herb tomato sauce.",
            image_url="/static/tracker/images/pizza.png"
        )
        FoodItem.objects.create(
            restaurant=r2,
            name="Garlic Mozzarella Bread",
            price=180.00,
            description="Baked artisan bread with garlic butter, parsley, and melted stretch mozzarella.",
            image_url="/static/tracker/images/pizza.png"
        )

        # 3. Wok On Fire
        r3 = Restaurant.objects.create(
            name="Wok On Fire",
            cuisine="Asian & Noodles",
            rating=4.7,
            delivery_time="25-35 min",
            delivery_fee=80.00,
            image_url="/static/tracker/images/noodles.png"
        )
        FoodItem.objects.create(
            restaurant=r3,
            name="Chicken Pad Thai",
            price=320.00,
            description="Stir-fried rice noodles, egg, bean sprouts, crushed peanuts, in sweet signature tamarind glaze.",
            image_url="/static/tracker/images/noodles.png"
        )
        FoodItem.objects.create(
            restaurant=r3,
            name="Spicy Kung Pao Beef",
            price=380.00,
            description="Tender beef slices, bell peppers, scallions, and toasted peanuts in a fiery chili soy glaze.",
            image_url="/static/tracker/images/noodles.png"
        )
        FoodItem.objects.create(
            restaurant=r3,
            name="Crispy Veggie Spring Rolls",
            price=120.00,
            description="Three crispy golden spring rolls loaded with fresh vegetables, served with sweet chili dip.",
            image_url="/static/tracker/images/noodles.png"
        )

        # 4. Sweet Treats
        r4 = Restaurant.objects.create(
            name="Sweet Treats",
            cuisine="Desserts & Bakery",
            rating=4.9,
            delivery_time="10-20 min",
            delivery_fee=30.00,
            image_url="/static/tracker/images/cake.png"
        )
        FoodItem.objects.create(
            restaurant=r4,
            name="Triple Chocolate Fudge Cake",
            price=180.00,
            description="Rich, moist layers of dark chocolate cake covered in decadent chocolate fudge icing.",
            image_url="/static/tracker/images/cake.png"
        )
        FoodItem.objects.create(
            restaurant=r4,
            name="Classic Strawberry Cheesecake",
            price=220.00,
            description="Creamy New York style baked cheesecake topped with fresh strawberry compote.",
            image_url="/static/tracker/images/cake.png"
        )
        FoodItem.objects.create(
            restaurant=r4,
            name="Chocolate Chunk Cookie Box",
            price=150.00,
            description="Four warm, soft-baked cookies loaded with premium Belgian milk chocolate chunks.",
            image_url="/static/tracker/images/cake.png"
        )

        # 5. KFC
        r5 = Restaurant.objects.create(
            name="KFC",
            cuisine="Burgers & American",
            rating=4.5,
            delivery_time="15-25 min",
            delivery_fee=50.00,
            image_url="/static/tracker/images/burger.png"
        )
        FoodItem.objects.create(
            restaurant=r5,
            name="Zinger Burger",
            price=550.00,
            description="Our signature crispy chicken zinger fillet, lettuce, and mayo in a warm sesame bun.",
            image_url="/static/tracker/images/burger.png"
        )
        FoodItem.objects.create(
            restaurant=r5,
            name="Mighty Zinger",
            price=720.00,
            description="Double crispy chicken zinger fillets, double cheese, spicy mayo, and fresh lettuce.",
            image_url="/static/tracker/images/burger.png"
        )
        FoodItem.objects.create(
            restaurant=r5,
            name="Krusher Chocolate",
            price=290.00,
            description="Thick, creamy crushed ice shake blended with rich premium milk chocolate chips.",
            image_url="/static/tracker/images/cake.png"
        )

        # 6. Student Biryani
        r6 = Restaurant.objects.create(
            name="Student Biryani",
            cuisine="Asian & Noodles",
            rating=4.4,
            delivery_time="20-30 min",
            delivery_fee=30.00,
            image_url="/static/tracker/images/noodles.png"
        )
        FoodItem.objects.create(
            restaurant=r6,
            name="Single Chicken Biryani",
            price=300.00,
            description="Fragrant basmati rice layered with juicy spiced chicken, potatoes, and signature herbs.",
            image_url="/static/tracker/images/noodles.png"
        )
        FoodItem.objects.create(
            restaurant=r6,
            name="Double Chicken Biryani",
            price=450.00,
            description="Generous double serving of aromatic chicken biryani with extra leg pieces.",
            image_url="/static/tracker/images/noodles.png"
        )
        FoodItem.objects.create(
            restaurant=r6,
            name="Zeera Raita & Salad",
            price=80.00,
            description="Creamy cumin spiced yogurt dip served with freshly sliced garden salad.",
            image_url="/static/tracker/images/noodles.png"
        )

        # 7. Pizza Hut
        r7 = Restaurant.objects.create(
            name="Pizza Hut",
            cuisine="Italian & Pizza",
            rating=4.3,
            delivery_time="25-35 min",
            delivery_fee=70.00,
            image_url="/static/tracker/images/pizza.png"
        )
        FoodItem.objects.create(
            restaurant=r7,
            name="Chicken Fajita Pizza",
            price=850.00,
            description="Fajita chicken, onions, green peppers, mozzarella, and Pizza Hut's garlic sauce.",
            image_url="/static/tracker/images/pizza.png"
        )
        FoodItem.objects.create(
            restaurant=r7,
            name="Garlic Bread Mozzarella",
            price=240.00,
            description="Four toasted garlic bread slices smothered in warm melted mozzarella cheese.",
            image_url="/static/tracker/images/pizza.png"
        )

        # 8. Savour Foods
        r8 = Restaurant.objects.create(
            name="Savour Foods",
            cuisine="Asian & Noodles",
            rating=4.8,
            delivery_time="15-30 min",
            delivery_fee=40.00,
            image_url="/static/tracker/images/noodles.png"
        )
        FoodItem.objects.create(
            restaurant=r8,
            name="Chicken Pulao Kabab",
            price=380.00,
            description="Traditional aromatic pulao served with two crispy shami kababs and tender roasted chicken.",
            image_url="/static/tracker/images/noodles.png"
        )
        FoodItem.objects.create(
            restaurant=r8,
            name="Extra Shami Kabab",
            price=90.00,
            description="One extra piece of our signature crispy ground beef and lentil shami kabab.",
            image_url="/static/tracker/images/noodles.png"
        )
        FoodItem.objects.create(
            restaurant=r8,
            name="Traditional Kheer Cup",
            price=120.00,
            description="Creamy slow-cooked rice pudding flavored with green cardamom and dry nuts.",
            image_url="/static/tracker/images/cake.png"
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded BiteDash catalog!"))
