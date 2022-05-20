from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.core.validators import RegexValidator
from .validators import validation_age
import re


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'username', 'first_name', 'last_name', 'birthdate', 'addr_city', 'addr_street', 'addr_post_code',
            'mobile_nr')

    def clean_password2(self):
        """Check if the two password entries match"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """Save the provided password in hashed format"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = (
            'email', 'username', 'first_name', 'last_name', 'birthdate', 'addr_city', 'addr_street', 'addr_post_code',
            'mobile_nr', 'is_active', 'is_admin', 'is_staff')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'e-mail',
                                                              'class': 'form-control',
                                                              }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Hasło',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Nazwa użytkownika',
                                                             'class': 'form-control',
                                                             }))
    first_name = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'Imię',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Nazwisko',
                                                              'class': 'form-control',
                                                              }))
    birthdate = forms.DateField(validators=[validation_age], required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD',
                                                              'class': 'form-control',
                                                              }))
    addr_city = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Miasto',
                                                              'class': 'form-control',
                                                              }))
    addr_street = forms.CharField(required=True,
                                  widget=forms.TextInput(attrs={'placeholder': 'Ulica',
                                                                'class': 'form-control',
                                                                }))
    addr_post_code = forms.CharField(required=True,
                                     validators=[
                                         RegexValidator(
                                             regex=r'^[0-9]{2}-[0-9]{3}$',
                                             message='Proszę wpisać kod pocztowy w formacie xx-xxx',
                                         ),
                                     ],
                                     widget=forms.TextInput(attrs={'placeholder': 'Kod pocztowy',
                                                                   'class': 'form-control',
                                                                   }))
    mobile_nr = forms.CharField(required=True,
                                validators=[
                                    RegexValidator(
                                        regex=r'^(?:\(?\?)?(?:[-\.\(\)\s]*(\d)){9}\)?$',
                                        message='Proszę wpisać nr telefonu w formacie: xxx-xxx-xxx',
                                    ),
                                ],
                                widget=forms.TextInput(attrs={'placeholder': 'Numer telefonu',
                                                              'class': 'form-control',
                                                              }))

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'username', 'first_name', 'last_name', 'birthdate', 'addr_city',
                  'addr_street', 'addr_post_code', 'mobile_nr')

    @atomic
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.birthdate = self.cleaned_data['birthdate']
        user.addr_city = self.cleaned_data['addr_city']
        user.addr_street = self.cleaned_data['addr_street']
        user.addr_post_code = self.cleaned_data['addr_post_code']
        user.mobile_nr = self.cleaned_data['mobile_nr']

        if commit:
            user.save()

        return user


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    birthdate = forms.DateField(required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    addr_city = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    addr_street = forms.CharField(required=True,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
    addr_post_code = forms.CharField(required=True,
                                     validators=[
                                         RegexValidator(
                                             regex=r'^[0-9]{2}-[0-9]{3}$',
                                             message='Proszę wpisać kod pocztowy w formacie xx-xxx',
                                         ),
                                     ],
                                     widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile_nr = forms.CharField(required=True,
                                validators=[
                                    RegexValidator(
                                        regex=r'^(?:\(?\?)?(?:[-\.\(\)\s]*(\d)){9}\)?$',
                                        message='Proszę wpisać nr telefonu w formacie: xxx-xxx-xxx',
                                    ),
                                ],
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'first_name', 'last_name', 'birthdate', 'addr_city', 'addr_street',
                  'addr_post_code', 'mobile_nr']
