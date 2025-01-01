from django.shortcuts import render,get_list_or_404,get_object_or_404,redirect,HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

from .models import Car, UserProfile,Category,Product


# Create your views here.

def home(request):
    #cars = car.objects.filter(category__name='Carros')

    context = {}
    
    return render(request,'d_store/index.html',context)



def car_detail(request,slug):
    car = get_object_or_404(Car, slug = slug)
    slug = car.slug
    
    context = {'car':car, 'slug':slug}
    return render(request,'d_store/car_details.html', context)



def about(request):
    return render(request,'d_store/about.html')




def sell_car(request, car_id):
    car = Car.objects.get(id=car_id)
    main_image = car.car_imange.filter(main=True).first()  
    
    context ={
    'car':car,
    'main_image':main_image
    }
    return render(request,'d_store/sell_car.html', context)



def catetories(request):

    categories = get_list_or_404(Category)
    
    context = {
        'categories':categories
    }

    return render(request,'d_store/catetories.html',context)


def product_detail(request,category_id):

    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    categories = Category.objects.all()
    
    context = {
        'categories': categories,
        'category': category, 
        'products': products,
    }

    return render(request,'d_store/parts_detail.html',context)


def product (request, product_id):
    product = get_object_or_404(Product,id=product_id)
    
    context = {'product':product }
    return render(request,'d_store/product.html',context)


def check_info(request):
    phone = request.POST.get('phone')
    
    if len(phone) < 10:  # Verifica que tenga más de 11 caracteres
        return HttpResponse(
            "<p class='text-danger fw-bold small container text-wrap container'>Asegúrate de que tenga más de 11 caracteres sin guiones.</p>"
        )
    
    if UserProfile.objects.filter(phone=phone).exists():
        user = UserProfile.objects.get(phone=phone)
  
        
        return render(request,'partials/customer_info.html' ,{'user':user})
    else:
        return HttpResponse(
            "<p class='text-danger fw-bold small container'>Identificación no registrada.</p>"
        )





