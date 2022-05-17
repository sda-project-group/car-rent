from django import forms

from .models import Order


class OrderDatePickForm(forms.ModelForm):

    start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    return_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Order
        fields = ['start_date', 'return_date']
