from django.contrib import admin

from .models import UserProfile, Category, Car, CarImages,Product, CartItem, PossibleBuyer

 
class ImageInline(admin.TabularInline):
    model = CarImages
    extra = 4
    

class CarAdmin(admin.ModelAdmin):
    inlines = [ImageInline]  # Relacionamos las imágenes con los coches



admin.site.register(Car,CarAdmin)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(PossibleBuyer)


    




