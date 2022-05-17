import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView

from .forms import OrderDatePickForm
from .models import BasePrice, Car, Order
from .validators import order_date_validator, if_found_in_db


def base_test_view(request):
    return render(request, 'carrentapp/base.html')


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
                                start_date__range=(objct.start_date, objct.return_date)) | \
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
        return qs.filter(client=self.request.user).filter(start_date__lte=datetime.date.today()).filter(
                         return_date__gte=datetime.date.today())


class HistoryOrderView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'carrentapp/order_history.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(return_date__lt=datetime.date.today(), client=self.request.user)


class FutureOrderView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'carrentapp/order_future.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(start_date__gt=datetime.date.today(), client=self.request.user)
