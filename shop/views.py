from django.contrib.auth import logout,authenticate,login
from django.shortcuts import render,redirect
from django.views import View
from pyexpat.errors import messages
from shop.models import Category
from shop.models import Product
from shop.forms import SignUpForm
from shop.forms import LoginForm
from shop.forms import StockForm
from shop.forms import ProductForm, CategoryForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from shop.decorator import admin_required

class Categories(View):
    def get(self, request):
        c=Category.objects.all()
        context = {'categories': c}
        return render(request, 'categories.html', context)

class Products(View):
    def get(self, request,i):
        c = Category.objects.get(id=i)
        context = { 'categories' : c }
        return render(request, 'products.html', context)

class ProductDetail(View):
    def get(self, request,i):
        p=Product.objects.get(id=i)
        context = {'product' : p}
        return render(request, 'productdetail.html',context)

class Register(View):
    def post(self,request):
        form_instance=SignUpForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:userlogin')
    def get(self,request):
        form_instance = SignUpForm()
        context = {'form': form_instance}
        return render(request, 'register.html', context)

class UserLogin(View):
    def get(self,request):
        form_instance = LoginForm()
        context = {'form': form_instance}
        return render(request, 'login.html', context)
    def post(self,request):
        form_instance=LoginForm(request.POST)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            print(data)
            u=data['username']
            p=data['password']
            user=authenticate(username=u,password=p)

            if user:
                login(request,user)
                return redirect('categories')
            else:
                messages.error(request, "Login unsuccessfully, Invalid login details provided")
                return redirect('userlogin')

@method_decorator(login_required,name='dispatch')
class UserLogout(View):
    def get(self,request):
        logout(request)
        print(request.user)
        return redirect('shop:userlogin')
@method_decorator(admin_required,name='dispatch')
@method_decorator(login_required,name='dispatch')
class AddCategory(View):
    def post(self,request):
        form_instance=CategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('categories')
    def get(self,request):
        form_instance=CategoryForm()
        context = {'form': form_instance}
        return render(request, 'addcategory.html', context)

@method_decorator(login_required,name='dispatch')
@method_decorator(admin_required,name='dispatch')
class AddProduct(View):
    def post(self,request):
        form_instance=ProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('categories')
    def get(self,request):
        form_instance=ProductForm()
        context = {'form': form_instance}
        return render(request, 'addproduct.html', context)

class AddStock(View):
    def post(self,request,i):
        p=Product.objects.get(id=i)
        form_instance=StockForm(request.POST,instance=p)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('categories')
    def get(self,request,i):
        p=Product.objects.get(id=i)
        form_instance=StockForm(instance=p)
        context = {'form': form_instance}
        return render(request, 'addstock.html', context)




