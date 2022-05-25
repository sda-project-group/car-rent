from django import forms

from carrentapp.models import Order


class OrderDateForm(forms.Form):
    start_date = forms.DateField(required=True,
                                 widget=forms.DateInput(attrs={'class': 'form-control',
                                                               'type': 'date'}))
    return_date = forms.DateField(required=True,
                                  widget=forms.DateInput(attrs={'class': 'form-control',
                                                                'type': 'date'}))


class OrderCreationForm(forms.ModelForm):
    start_date = forms.DateField(required=True,
                                 disabled=True,
                                 widget=forms.DateInput(attrs={'class': 'form-control',
                                                               'type': 'date'}))
    return_date = forms.DateField(required=True,
                                  disabled=True,
                                  widget=forms.DateInput(attrs={'class': 'form-control',
                                                                'type': 'date'}))

    class Meta:
        model = Order
        fields = ['start_date', 'return_date']


class OrderUpdateForm(forms.ModelForm):
    start_date = forms.DateField(required=True,
                                 widget=forms.DateInput(attrs={'class': 'form-control',
                                                               'type': 'date'}))
    return_date = forms.DateField(required=True,
                                  widget=forms.DateInput(attrs={'class': 'form-control',
                                                                'type': 'date'}))

    class Meta:
        model = Order
        fields = ['start_date', 'return_date']


class OrderUpdateFormBlocked(OrderUpdateForm):
    start_date = forms.DateField(required=True,
                                 disabled=True,
                                 widget=forms.DateInput(attrs={'class': 'form-control',
                                                               'type': 'date'}))

    class Meta:
        model = Order
        fields = ['start_date', 'return_date']
