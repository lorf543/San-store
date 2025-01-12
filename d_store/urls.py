from . import views

from django.urls import path



urlpatterns = [
    path('',views.home,name='home'),
    path('category_list', views.category_list, name='category_list'),
    path('parts/<slug:slug>/',views.auto_parts,name='auto_parts'),
    path('product/<slug:slug>/',views.view_part,name='view_part'),
    

    path('add-to-cart-btn/<int:product_id>/', views.add_to_cart_btn, name='add_to_cart_btn'),
        

    path('search-products/', views.search_products, name='search_products'),
    
    
    path('car/<slug:slug>/',views.view_car,name="car_view")
    
]


# htmx_urlpatterns = [
#     path('check_info',views.check_info,name='check_info')
# ] 




# urlpatterns += htmx_urlpatterns


