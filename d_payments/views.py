import stripe
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from d_store.models import Product

from .models import Invoice
from d_store.models import CartItem

stripe.api_key = settings.STRIPE_SECRET_KEY




@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = 'tu_endpoint_secret'  # Obtén esto desde tu dashboard de Stripe

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # Manejar el evento de pago exitoso
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_successful_payment(session)

    return JsonResponse({'status': 'success'})

def handle_successful_payment(session):
    print("esta funcion se esta ejecutando")
    user_id = session['metadata'].get('user_id')
    if not user_id:
        print("Error: User ID is missing in session metadata")
        return

    try:
        # Crear una factura
        invoice = Invoice.objects.create(
            user_id=user_id,
            stripe_invoice_id=session.get('payment_intent'),
            total_amount=session['amount_total'] / 100,
            currency=session['currency'],
            status='paid',
        )
        print(f"Invoice {invoice.id} created successfully.")
    except Exception as e:
        print(f"Error creating invoice: {e}")
        return

    # Reducir stock y vaciar carrito
    try:
        cart_items = CartItem.objects.filter(user_id=user_id)
        for item in cart_items:
            product = item.product
            if product.stock >= item.quantity:
                product.stock -= item.quantity
                product.save()
            else:
                print(f"Insufficient stock for {product.brand}")
        cart_items.delete()
    except Exception as e:
        print(f"Error processing cart items: {e}")
    
    
@login_required
def checkout_htmx(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    cart_items = request.user.cart_items.all()
    total_price = sum(item.get_total_price() for item in cart_items)

    # Crear sesión de Stripe
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'dop',
                    'product_data': {'name': item.product.brand},
                    'unit_amount': int(item.product.price * 100),
                },
                'quantity': item.quantity,
            }
            for item in cart_items
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')),
        cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
    )
    return redirect(session.url, code=303)
    
@login_required
def payment_success(request):
    return render(request, 'd_payments/payment_success.html')

@login_required
def payment_cancel(request):
    return render(request, 'd_payments/payment_cancel.html')    
    
    
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
    print(total_price)

    # Retornar solo los artículos actualizados y el total (renderizar solo la parte del carrito y el total)
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'cart/cart_items_and_total.html', context)


@login_required
def update_cart_total(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)


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

    # Retorna una respuesta sin contenido
    return HttpResponse(status=204)


