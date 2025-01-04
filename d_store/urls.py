from . import views

from django.urls import path



urlpatterns = [
    path('',views.home,name='home'),
    path('parts',views.auto_parts,name='auto_parts'),
    path('cart/', views.view_cart, name='view_cart'),
    path('auto-parts/<slug:slug>/', views.parts_detail, name='parts_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart_htmx, name='add_to_cart_htmx'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart_htmx, name='remove_from_cart_htmx'),
    path('update_cart/<pk>/', views.update_cart_htmx, name='update_cart_htmx'),
    path('checkout/', views.checkout_htmx, name='checkout_htmx'),
    # path('success/', views.payment_success, name='payment_success'),

]


htmx_urlpatterns = [
    path('check_info',views.check_info,name='check_info')
]

urlpatterns += htmx_urlpatterns


