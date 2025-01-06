from . import views

from django.urls import path



urlpatterns = [
    path('',views.home,name='home'),
    path('category_list', views.category_list, name='category_list'),
    path('parts/<slug:slug>/',views.auto_parts,name='auto_parts'),
    path('product/<slug:slug>/',views.view_part,name='view_part'),
    
    
    
    path('cart/', views.view_cart, name='view_cart'),
    
    path('checkout/', views.checkout_htmx, name='checkout_htmx'),
    path('search-products/', views.search_products, name='search_products'),
    
]


# htmx_urlpatterns = [
#     path('check_info',views.check_info,name='check_info')
# ]


cart_urlpatterns = [
    path('cart/add/<int:product_id>/', views.add_to_cart_htmx, name='add_to_cart_htmx'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart_htmx, name='remove_from_cart_htmx'), 
    path('update_cart/<pk>/', views.update_cart_items, name='update_cart_items'),
    path('update-cart-total/', views.update_cart_total, name='update_cart_total'),
]

urlpatterns += cart_urlpatterns

# urlpatterns += htmx_urlpatterns


