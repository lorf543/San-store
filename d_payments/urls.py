from django.urls import path
from . import views


urlpatterns = [
    path('stripe/webhook/', views.stripe_webhook, name="stripe_webhook"),
]


checkout_urlpatterns = [
    path('checkout/', views.checkout_htmx, name='checkout_htmx'),
    path('checkout/success/', views.payment_success, name='payment_success'),
    path('checkout/cancel/', views.payment_cancel, name='payment_cancel'),
    
]

cart_urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart_htmx, name='add_to_cart_htmx'),
    path('update_cart/<pk>/', views.update_cart_items, name='update_cart_items'),
    path('update-cart-total/', views.update_cart_total, name='update_cart_total'),
]

urlpatterns = checkout_urlpatterns + cart_urlpatterns