from django import forms
from cart.models import Order




class CheckoutForm(forms.ModelForm):
    payment_choices=(('Cash on delivery','Cash on delivery'),('Online','Online'))
    payment_method=forms.ChoiceField(choices=payment_choices)

    class Meta:
        model = Order
        fields = ['address','phone','payment_method']