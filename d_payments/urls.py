from django.urls import path
from . import views

urlpatterns = [
    path('stripe-webhook/', views.stripe_webhook, name='stripe-webhook'),
    path('success-payment/',views.success_payment,name='success_payment'),
    path('cencel-payment/',views.cencel_payment,name='cencel_payment'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/',views.view_cart,name='view_cart'),    
    path('update-cart/<int:cart_item_id>',views.update_cart,name='update_cart'),    
    path('remove-from-cart/<int:cart_item_id>',views.remove_from_cart,name='remove_from_cart'),    
]