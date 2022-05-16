from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm, UpdateUserForm, OrderDatePickForm
from .models import BasePrice, Car, Order
from .validators import order_date_validator, if_found_in_db

def base_test_view(request):
    return render(request, 'carrentapp/base.html')


class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        return reverse('main')


class RegisterView(View):
    form_class = RegistrationForm
    initial = {'key': 'value'}
    template_name = 'carrentapp/registration.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            return redirect(to='main')

        return render(request, self.template_name, {'form': form})


class UpdateProfileUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_form = UpdateUserForm(instance=request.user)
        return render(request, 'carrentapp/profile.html', {'user_form': user_form} )

    def post(self, request, *args, **kwargs):
        user_form = UpdateUserForm(request.POST, instance=request.user)
        print(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Twój profil został pomyślnie zaktualizowany')
            return redirect(to='user-profile')

        return HttpResponse(request.POST)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'carrentapp/password_change.html'
    success_message = "Hasło zostało zmienione"
    success_url = reverse_lazy('main')


class CreateOrderView(CreateView):
    model = Order
    form_class = OrderDatePickForm

    def form_valid(self, form):
        objct = form.save(commit=False)
        objct.client = self.request.user
        objct.car = Car.objects.get(id=self.kwargs['pk'])
        objct.base_price = BasePrice.objects.get(id=1)

        errors = order_date_validator(objct.start_date, objct.return_date)
        if errors:
            return redirect('order_msg', pk=objct.car.pk, msg=errors)

        colliding_entries = Order.objects.filter(
                                                status='Aktywny',
                                                car=objct.car,
                                                start_date__range=(objct.start_date, objct.return_date)) |\
                            Order.objects.filter(
                                                status='Aktywny',
                                                car=objct.car,
                                                return_date__range=(objct.start_date, objct.return_date))

        errors = if_found_in_db(colliding_entries)
        if errors:
            return redirect('order_msg', pk=objct.car.pk, msg=errors)

        objct.save()
        return redirect('order_confirm', pk=objct.id)


class OrderConfirmView(DeleteView):
    model = Order

    def get_success_url(self):
        return reverse('car_detail', args=[self.object.car.id])


class ActualOrderView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'carrentapp/order_actual.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(start_date__gt=datetime.date.today(), client=self.request.user)


class HistoryOrderView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'carrentapp/order_history.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(return_date__lt=datetime.date.today(), client=self.request.user)


class FutureOrderView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'carrentapp/order_history.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(start_date__gt=datetime.date.today(), client=self.request.user)