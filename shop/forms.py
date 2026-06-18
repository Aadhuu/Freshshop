from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from shop.models import Category, Product


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1','password2', 'email')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields =['name', 'description', 'image','price','stock' ,'category']

class StockForm(forms.ModelForm):
    class Meta:
        model = Product
        fields =['stock']