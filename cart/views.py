import uuid


from django.shortcuts import render, redirect
from django.views import View
import razorpay

from shop.models import Product

from cart.models import Cart

from cart.forms import CheckoutForm

from cart.models import Order

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required,name='dispatch')
class AddtoCart(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        try:
            c=Cart.objects.get(user=u,product=p)#check whether the product is already added
                                                #to cart by the logged in user.if yes increment quantity by 1
            c.quantity+=1
            c.save()
        except: #else,create a new cart record with quantity 1
            c = Cart.objects.create(user=u, product=p,quantity=1)
            c.save()

        return redirect('cart:cartview')
@method_decorator(login_required,name='dispatch')
class CartView(View):
    def get(self,request):
        c=Cart.objects.filter(user=request.user)

        total=0
        for i in c:
            total+=i.subtotal()
        context = {'cart': c, 'total': total}
        return render(request,'cart.html',context)

class CartDecrement(View):
    def get(self,request,i):
        c=Cart.objects.get(id=i)
        if c.quantity>1:
            c.quantity-=1
            c.save()
        else:
            c.delete()
        return redirect('cart:cartview')
class CartRemove(View):
    def get(self,request,i):
        c=Cart.objects.get(id=i)
        c.delete()
        return redirect('cart:cartview')
import uuid
@method_decorator(login_required,name='dispatch')
class Checkout(View):
    def post(self,request):
        form_instance=CheckoutForm(request.POST)
        if form_instance.is_valid():
            o=form_instance.save(commit=False)
            # user
            u=request.user
            o.user=u
            # amount
            c=Cart.objects.filter(user=u)
            total=0
            for i in c:
                total+=i.subtotal()
            o.amount=total
            o.save()
            if o.payment_method=="Online":
                # razorpay client connection
                client=razorpay.Client(auth=('rzp_test_T2NqB3BLcuCSAZ','eS1ooiQ86CmDt8R6NjmNKef2'))
                print(client)
            #creates an order using client
                response_payment=client.order.create(dict(amount=total*100,currency="INR"))
                print(response_payment)

                o.order_id=response_payment['id']
                o.save()
                context = {'payment': response_payment}
                return render(request, 'payment.html', context)

            else:
                # order id manually create id for cod order
                id='ord_cod'+uuid.uuid4().hex[:14]
                o.order_id=id
                o.is_ordered = True
                o.save()
                # order items
                c = Cart.objects.filter(user=request.user)
                for i in c:
                    item = OrderItem.objects.create(order=o, product=i.product, quantity=i.quantity)
                    item.save()
                    item.product.stock -= item.quantity
                    item.product.save()
                # cart
                c.delete()
                return render(request, 'payment.html')


    def get(self,request):
        form_instance=CheckoutForm()
        context = {'form': form_instance}
        return render(request,'checkout.html',context)

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from cart.models import OrderItem

@method_decorator(csrf_exempt,name='dispatch')
@method_decorator(login_required,name='dispatch')#to avoid csrf verification
class PaymentSuccess(View):
    def post(self,request):
        print(request.POST)
        id=request.POST.get('razorpay_order_id')
        # order
        o=Order.objects.get(order_id=id)
        o.is_ordered = True
        o.save()
        # ordered items
        c=Cart.objects.filter(user=request.user)
        for i in c:
            item=OrderItem.objects.create(order=o, product=i.product, quantity=i.quantity)
            item.save()
            item.product.stock-=item.quantity
            item.product.save()
        #cart
        c.delete()

        return render(request,'paymentsuccess.html')
class OrderSummary(View):
    def get(self,request):
        o=Order.objects.filter(user=request.user,is_ordered=True)
        context = {'orders': o}

        return render(request,'ordersummary.html',context)
