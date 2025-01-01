from . import views

from django.urls import path



urlpatterns = [
    path('',views.home,name='home'),
    path("catetories/",views.catetories, name="parts"),
    path("product/<int:product_id>/",views.product, name="product"),
    path("product_detail/<int:category_id>/", views.product_detail, name="product_detail"),
    path('Our-Story',views.about,name='about'), 
    path('product/<int:product_id>/sell/',views.sell_car, name='sell_product'),  
    path('<slug:slug>/',views.car_detail,name='articles'),

]


htmx_urlpatterns = [
    path('check_info',views.check_info,name='check_info')
]

urlpatterns += htmx_urlpatterns


