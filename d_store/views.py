from django.shortcuts import render,get_list_or_404,get_object_or_404,redirect,HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

from .models import Car, UserProfile,Category,Product


# Create your views here.

def home(request):
    #cars = car.objects.filter(category__name='Carros')

    context = {}
    
    return render(request,'d_store/index.html',context)



def auto_parts(request):
    categories = get_list_or_404(Category)
    
    context = {
        'categories':categories
    }
    return render(request,'d_store/auto_parts.html',context)


def parts_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products_parts.all()

    context = {
        'category': category,
        'products': products
    }
    return render(request, 'd_store/parts_detail.html', context)




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





