from .models import CartItem

def cart_item_count(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0
    return {'cart_count': cart_count}