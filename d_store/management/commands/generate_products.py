import random
from faker import Faker
from django.core.management.base import BaseCommand
from d_store.models import Product, Category

class Command(BaseCommand):
    help = "Generate fake products for testing"

    def handle(self, *args, **kwargs):
        fake = Faker()
        brands = [
            "Bosch", "Delco", "Exide", "Energizer", "Varta",
            "Panasonic", "Yuasa", "ACDelco", "Duralast",
            "EverStart", "Motorcraft", "NAPA", "Odyssey",
        ]
        # type_oild = [
        #     'Sintentico','Semi-sintentico','Mineral'
        # ]
        # viscosity = [
        #     '0W-20', '0W-30', '0W-40', '5W-20', '5W-30', 
        #     '5W-40', '5W-50', '10W-40', '10W-60', '15W-40'
        # ]

        categoria, created = Category.objects.get_or_create(name="Baterias")
        
        for _ in range(10): 
            brand = random.choice(brands)
            price = round(random.uniform(5500.0, 7500.0), 2)
            amp = f"{random.choice([12, 24, 48])}V"
            volts = f"{random.choice([12, 24, 48])}V"
            stock = round(random.choice([4,20,15]))
            # viscosity = random.choice(viscosity)
            description = fake.paragraph(nb_sentences=3)  # Generate a paragraph with 3 sentences
            
            Product.objects.create(
                brand=brand,
                price=price,
                amp=amp,
                volts=volts,
                category=categoria,
                stock=stock,
                description=description
            )

        self.stdout.write(self.style.SUCCESS("10 products created successfully!"))
