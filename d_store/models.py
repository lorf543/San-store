from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import uuid

FUEL_CHOICES = [
    ('Gasolina', 'Gasolina'),
    ('Diésel', 'Diésel'),
    ('Eléctrico', 'Eléctrico'),
    ('Híbrido', 'Híbrido'),
]

TRANSMISSION_CHOICES = [
    ('Manual', 'Manual'),
    ('Automático', 'Automático'),
    ('CVT', 'CVT'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20,null=True, blank=True)
    address = models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=50,null=True, blank=True)
    provincia = models.CharField(max_length=50,null=True, blank=True)
    country = models.CharField(max_length=50,null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.user.email}"


class Category(models.Model):
    name = models.CharField(max_length=50,null=True, blank=True)
    code = models.CharField(max_length=10, unique=True,null=True, blank=True)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('id',)
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.code = str(uuid.uuid4().int)[-6:]
        super().save(*args, **kwargs)

class Car(models.Model):
    brand = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    km = models.CharField(max_length=50, null=True, blank=True)
    fuel = models.CharField(max_length=50, choices=FUEL_CHOICES, null=True, blank=True)
    engine = models.CharField(max_length=50, null=True, blank=True)
    transmission = models.CharField(max_length=50, choices=TRANSMISSION_CHOICES, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    
    
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='added_cars',on_delete=models.CASCADE,null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='updated_cars',on_delete=models.CASCADE,null=True, blank=True )
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class Product(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='part_images', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="added_parts", null=True, blank=True)  # Relación con la categoría
    
    def __str__(self):
        return self.name
    
    
    
class CarImages(models.Model):
    product = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="product_imange")
    image = models.ImageField(upload_to="car_images", null=True, blank=True)
    main = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.car.brand} {self.car.model}"


    def get_main_image(self):
        main_image = self.car_images.filter(main=True).first()
        return main_image.image.url if main_image else 'https://placehold.co/600x400'
    
#     def active_items(self):
#         if self.sold == True:
#             return True

#     def __str__(self):
#         return f"{self.brand} ({self.year})  ({self.category})"
    
    def get_main_image(self):
        main_image = self.product_imange.filter(main=True).first()
        return main_image.image.url if main_image else 'https://placehold.co/600x400'
    
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(f"{self.brand}-{self.year}")
        
#         self.name = f"{self.brand} - {self.year}"        
#         super().save(*args, **kwargs)
        
        

    


# class PaymentPlan(models.Model):
#     product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='payment_plan', null=True, blank=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='user_payment', blank=True, null=True)
#     annual_interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00, null=True, blank=True)
#     months = models.PositiveIntegerField(default=12)
#     monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

#     def clean(self):
#         if self.months <= 0:
#             raise ValidationError("El número de meses debe ser mayor que cero.")
#         if self.annual_interest_rate < 0 or self.annual_interest_rate > 100:
#             raise ValidationError("La tasa de interés debe estar entre 0% y 100%.")

#     def update_total_paid(self):
#         self.total_paid = sum([payment.amount for payment in self.payments.all()])
#         self.save()

#     def get_remaining_balance(self):
#         return round(self.monthly_payment * self.months - self.total_paid, 2)

#     def calculate_monthly_payment(self):
#         P = self.product.price
#         r = self.annual_interest_rate / 12 / 100
#         n = self.months
#         if r > 0:
#             M = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
#         else:
#             M = P / n
#         self.monthly_payment = round(M, 2)
#         self.save()

#     def is_fully_paid(self):
#         return self.get_remaining_balance() <= 0

#     def total_interest_paid(self):
#         return round(self.total_paid - self.product.price, 2)

#     def __str__(self):
#         return f"Payment Plan for {self.product}"


# class Payment(models.Model):
#     payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.CASCADE, related_name='payments')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     payment_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     balance_remaining = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     status = models.CharField(
#         max_length=20, 
#         choices=[('completed', 'Completed'), ('pending', 'Pending')], 
#         default='pending'
#     )

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         self.payment_plan.update_total_paid()
#         self.balance_remaining = self.payment_plan.get_remaining_balance()
#         if self.payment_plan.is_fully_paid():
#             self.status = 'completed'
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Payment of {self.amount} for Payment Plan {self.payment_plan}"
