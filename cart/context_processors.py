from cart.models import Cart


def cart_items(request):
    total = 0
    if request.user.is_authenticated:
        u=request.user
        c = Cart.objects.filter(user=u)

        for i in c:
           total+=i.quantity


    return {'total':total}
