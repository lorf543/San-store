from django.shortcuts import render,get_list_or_404,get_object_or_404,redirect,HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
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


@login_required
def view_cart(request):
    cart_items = request.user.cart_items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'd_store/cart.html', context)


@login_required
def add_to_cart_htmx(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Render partial HTML response
    cart_items = request.user.cart_items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    cart_html = render_to_string('d_store/cart_items_partial.html', {'cart_items': cart_items})
    total_price_html = render_to_string('d_store/cart_total_partial.html', {'total_price': total_price})
    
    return JsonResponse({
        'cart_html': cart_html,
        'total_price_html': total_price_html
    })

@login_required
def remove_from_cart_htmx(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()

    # Render updated cart
    cart_items = request.user.cart_items.all()
    total_price = sum(item.get_total_price() for item in cart_items)
    cart_html = render_to_string('cart/cart_items_partial.html', {'cart_items': cart_items})
    total_price_html = render_to_string('cart/cart_total_partial.html', {'total_price': total_price})
    
    return JsonResponse({
        'cart_html': cart_html,
        'total_price_html': total_price_html
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
                    'currency': 'usd',
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





