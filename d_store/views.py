from django.shortcuts import render,get_list_or_404,get_object_or_404,redirect,HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

from .models import Car, UserProfile,Category,Product,CartItem


# Create your views here.

def home(request):
    #cars = car.objects.filter(category__name='Carros')

    context = {}
    
    return render(request,'d_store/index.html',context)



def auto_parts(request):
    categories = get_list_or_404(Category)
    
    context = {
        'categories':categories,
    }
    return render(request,'d_store/category_parts.html',context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products_parts.all()

    context = {
        'category': category,
        'products': products,
    }
    
    return render(request, 'd_store/parts_detail.html', context)


def search_products(request):
    search_product = request.GET.get('search_product')
    products = Product.objects.all()

    if search_product:
        products = products.filter(name__icontains=search_product)
        context = {
            'products': products,
        }
        return render(request, 'd_store/search_results.html', context)

    # Si no hay búsqueda, renderiza las categorías originales
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'd_store/category_parts.html', context)


@ensure_csrf_cookie
@login_required
def view_cart(request):
    cart_items = request.user.cart_items.all()


    context = {
        'cart_items': cart_items,
    }
    return render(request, 'cart/view_cart.html', context)

@login_required
def update_cart_items(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
    quantity = int(request.POST.get('quantity', 0))

    if quantity < 1:
        cart_item.delete()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    # Obtener todos los artículos actualizados en el carrito
    cart_items = CartItem.objects.filter(user=request.user)

    # Calcular el precio total del carrito
    total_price = sum(item.get_total_price() for item in cart_items)

    # Retornar solo los artículos actualizados y el total (renderizar solo la parte del carrito y el total)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'cart/cart_items_and_total.html', context)


@login_required
def update_cart_total(request):
    # Obtener todos los artículos del carrito del usuario
    cart_items = CartItem.objects.filter(user=request.user)

    # Calcular el precio total del carrito
    total_price = sum(item.get_total_price() for item in cart_items)
    print('working')

    # Retornar solo el total del carrito (renderizar solo la parte del total)
    context = {
        'total_price': total_price,
    }

    return render(request, 'cart/cart_total.html', context)



@login_required
def add_to_cart_htmx(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart_items = request.user.cart_items.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    cart_html = render_to_string('cart/cart_items.html', {'cart_items': cart_items})
    total_html = render_to_string('cart/cart_total.html', {'total_price': total_price})


    return JsonResponse({
        'cart_html': cart_html,
        'total_html': total_html,
    })

@login_required
def remove_from_cart_htmx(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()

    cart_items = request.user.cart_items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    cart_count = cart_items.count()

    cart_html = render_to_string('cart/cart_items.html', {'cart_items': cart_items})
    total_html = render_to_string('cart/cart_total.html', {'total_price': total_price})
    count_html = render_to_string('cart/cart_count.html', {'cart_count': cart_count})

    return JsonResponse({
        'cart_html': cart_html,
        'total_html': total_html,
        'count_html': count_html,
    })

@login_required
def checkout_htmx(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    cart_items = request.user.cart_items.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    # Create Stripe session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'dop',
                    'product_data': {
                        'name': item.product.brand,
                    },
                    'unit_amount': int(item.product.price * 100),
                },
                'quantity': item.quantity,
            }
            for item in cart_items
        ],
        mode='payment',
        success_url=request.build_absolute_uri('/success/'),
        cancel_url=request.build_absolute_uri('/cart/'),
    )
    
    return redirect(session.url, code=303)



@login_required
def payment_success(request):
    # Clear the cart after payment
    cart_items = request.user.cart_items.all()
    order_details = "\n".join(
        [f"{item.product.brand} x {item.quantity} - ${item.get_total_price()}" for item in cart_items]
    )
    total_price = sum(item.get_total_price() for item in cart_items)
    
    # Send confirmation email
    send_mail(
        subject="Order Confirmation",
        message=f"Thank you for your purchase! \n\nOrder Details:\n{order_details}\n\nTotal: ${total_price}",
        from_email="yourstore@example.com",
        recipient_list=[request.user.email],
        fail_silently=False,
    )
    cart_items.delete()
    
    return render(request, 'd_store/payment_success.html')




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





