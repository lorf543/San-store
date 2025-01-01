import stripe
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from d_store.models import Product
from .models import Cart,Invoice

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    # Verificar que el usuario tiene productos en el carrito
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('cart')  # Redirigir si el carrito está vacío

    # Crear una lista de ítems para Stripe
    line_items = [
        {
            'price_data': {
                'currency': 'dop',
                'product_data': {
                    'name': item.product.name,
                    'images': [item.product.image.url],  # Usar directamente la URL de la imagen
                },
                'unit_amount': int(item.product.price * 100),  # Stripe usa centavos
            },
            'quantity': item.quantity,
        }
        for item in cart_items
    ]

    # Crear la sesión de Stripe
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success_payment')),
            cancel_url=request.build_absolute_uri(reverse('cancel_payment')),
            metadata={'user_id': request.user.id},  # Agregar el ID del usuario
        )
        return redirect(session.url, code=303)  # Redirigir al usuario al checkout de Stripe
    except stripe.error.StripeError as e:
        return JsonResponse({'error': f'Error al crear la sesión de pago: {str(e)}'}, status=400)

@login_required
def success_payment(request):
    Cart.objects.filter(user=request.user).delete()  # Vaciar el carrito
    return HttpResponse('Pago realizado con éxito')

@login_required
def cencel_payment(request):
    return HttpResponse('pago cancelado')



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
    # Obtener el ID del usuario desde metadata (puedes personalizar esto)
    user_id = session['metadata']['user_id']

    # Crear una factura
    Invoice.objects.create(
        user_id=user_id,
        stripe_invoice_id=session.get('payment_intent'),
        total_amount=session['amount_total'] / 100,
        currency=session['currency'],
        status='paid',
    )

    # Reducir el stock de los productos comprados
    cart_items = Cart.objects.filter(user_id=user_id)
    for item in cart_items:
        product = item.product
        if product.stock >= item.quantity:
            product.stock -= item.quantity
            product.save()
        else:
            # Manejar caso de stock insuficiente si es necesario
            print(f"Stock insuficiente para {product.name}")

    # Vaciar el carrito después de la compra
    cart_items.delete()

def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()

        # Renderizar el fragmento actualizado
        return render(request, 'cart/cart_item_partial.html', {'cart_item': cart_item})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def view_cart(request):
    # Obtener los productos en el carrito del usuario
    cart_items = Cart.objects.filter(user=request.user)

    # Calcular el total del carrito
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'cart/view_cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount
    })
    


def update_cart(request, cart_item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
    return redirect('view_cart')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')

