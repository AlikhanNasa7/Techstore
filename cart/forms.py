from django import forms
from store.models import CartItem, Cart, Order


class OrderForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'del__input',
        'placeholder': 'Введите свой адрес',
    }))

    DELIVERY_CHOICES = [
        ('Pickup', 'Pickup'),
        ('Courier', 'Courier'),
    ]
    PAYMENT_CHOICES = [
        ('Card', 'CARD'),
        ('Cash', 'CASH'),
    ]
    delivery_option = forms.ChoiceField(
        choices=DELIVERY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'block__text'})
    )
    payment_option = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'block__text'})
    )

    class Meta:
        model = Order
        exclude = ('user',)
