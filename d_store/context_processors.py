from django.contrib.auth.models import User
from .models import CartItem

def cart_info(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0

    return {
        'cart_count': cart_count
    }