from django.conf import settings
from django.db import models
from django.utils.text import slugify
import uuid
from django.contrib.auth.models import User
from django.conf import settings


def get_default_image():
    return settings.STATIC_ROOT + '/images/default.jpg'

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

TYPE_OIL = [
    ('Sintentico','Sintentico'),
    ('Semi-sintentico','Semi-sintentico'),
    ('Mineral','Mineral')
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
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True)
    code = models.CharField(max_length=10, unique=True,null=True, blank=True)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('id',)
        verbose_name = "Category"
        verbose_name_plural = "Categories"
               
        
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4().int)[-6:]

        if not self.slug and self.name:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

class Car(models.Model):
    brand = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    km = models.CharField(max_length=50, null=True, blank=True)
    fuel = models.CharField(max_length=50, choices=FUEL_CHOICES, null=True, blank=True)
    engine = models.CharField(max_length=50, null=True, blank=True)
    transmission = models.CharField(max_length=50, choices=TRANSMISSION_CHOICES, null=True, blank=True)
    color_ext = models.CharField(max_length=50, null=True, blank=True)
    color_int = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    
    
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    added_by = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='added_cars',on_delete=models.CASCADE,null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='updated_cars',on_delete=models.CASCADE,null=True, blank=True )
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    
    
    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugify(f"{self.brand}-{self.model}-{self.price}")
            
        self.name = f"{self.brand} - {self.price}"        
        super().save(*args, **kwargs)

class Product(models.Model):
    brand = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=10, unique=True,null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='part_images', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="products_parts", null=True, blank=True) 
    
    amp = models.CharField(max_length=50,null=True, blank=True)
    volts = models.CharField(max_length=50,null=True, blank=True)
    
    psi = models.CharField(max_length=50,null=True, blank=True)
    
    type_oild = models.CharField(max_length=50,null=True, blank=True, choices=TYPE_OIL)
    viscosity = models.CharField(max_length=50,null=True, blank=True)
        
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.brand
    
    def get_product_info(self):
        info = f"{self.brand } - {self.category.name}"
        return info 
    
    def get_product_image(self):
        if not self.image:
            return settings.MEDIA_URL + 'images/default.jpg'
        return self.image.url
        
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4().int)[-6:]
            
        if not self.slug:
            self.slug = slugify(f"{self.brand}-{self.price}")
            
        if not self.image:
            self.image = 'images/default.jpg'
        
        self.name = f"{self.brand} - {self.price}"        
        super().save(*args, **kwargs)
                   
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.brand} - {self.product.category.name} - {self.quantity}" 
    
    def get_total_price(self):
        return self.product.price * self.quantity  
    
    def get_quantity_minus_one(self):
        return self.quantity - 1

    def get_quantity_plus_one(self):
        return self.quantity + 1
            
class CarImages(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="product_imange")
    image = models.ImageField(upload_to="car_images", null=True, blank=True)
    main = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.car.brand} {self.car.model}"


    def get_main_image(self):
        main_image = self.product_imange.filter(main=True).first()
        return main_image.image.url if main_image else 'https://placehold.co/600x400'
        
        
        
        
class PossibleBuyer(models.Model):
    name = models.CharField(max_length=50,null=True, blank=True)
    phone = models.CharField(max_length=50,null=True, blank=True)
    email = models.EmailField(max_length=254,null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE,related_name="possiblebuyercar")
    
    checked = models.BooleanField(null=True, blank=True)
    checked_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    when_checked = models.DateTimeField(null=True, blank=True)
    
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
     
    