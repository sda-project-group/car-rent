import datetime
from datetime import datetime as dt

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView, ListView, FormView, UpdateView, DeleteView, DetailView
from django.forms import modelform_factory

from carrentapp.forms import OrderDateForm, OrderCreationForm, OrderUpdateForm, OrderUpdateFormBlocked
from carrentapp.models import BasePrice, Car, Order
from carrentapp.utilities import calculate_cost
from carrentapp.validators import order_date_validator, if_entries_collide_error


def base_test_view(request):
    return render(request, 'carrentapp/base.html')


class PickOrderDate(FormView):
    form_class = OrderDateForm
    template_name = 'carrentapp/order_form.html'


    def form_valid(self, form):
        start_date = self.request.POST.get('start_date')
        start_date_datetime = dt.strptime(start_date, '%Y-%m-%d').date()
        return_date = self.request.POST.get('return_date')
        return_date_datetime = dt.strptime(return_date, '%Y-%m-%d').date()

        base_price = BasePrice.objects.get(id=1).base_price
        car = Car.objects.get(id=self.kwargs['pk'])
        self.request.session['car_id'] = car.id
        self.request.session['car_image'] = car.car_image.url
        self.request.session['car_brand'] = car.brand.brand_name
        self.request.session['car_model'] = car.car_model.model_name
        self.request.session['car_engine_power'] = car.engine_power
        self.request.session['car_engine_type'] = car.engine_type
        self.request.session['car_gearbox_type'] = car.gearbox_type
        self.request.session['car_color'] = car.color
        self.request.session['car_number_of_seats'] = car.number_of_seats
        self.request.session['car_year_of_production'] = car.year_of_production

        self.request.session['start_date'] = start_date
        self.request.session['return_date'] = return_date
        self.request.session['base_price_value'] = base_price
        self.request.session['total_cost'] = calculate_cost(start_date_datetime,
                                                            return_date_datetime,
                                                            base_price,
                                                            car.rating)

        errors = order_date_validator(start_date_datetime, return_date_datetime)
        if errors:
            return redirect('order_msg', pk=self.request.session.get('car_id'), msg=errors)

        errors = if_entries_collide_error(start_date_datetime, return_date_datetime, car)
        if errors:
            return redirect('order_msg',  pk=self.request.session.get('car_id'), msg=errors)

        return redirect('order_confirm')


class CreateOrderView(CreateView):
    model = Order
    form_class = OrderCreationForm
    template_name = 'carrentapp/order_confirm.html'


    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['start_date'] = self.request.session.get('start_date')
        print(initial['start_date'])
        print(type(initial['start_date']))
        initial['return_date'] = self.request.session.get('return_date')
        return initial


    def form_valid(self, form):
        objct = form.save(commit=False)
        objct.client = self.request.user
        objct.car = Car.objects.get(id=self.request.session.get('car_id'))
        objct.base_price = BasePrice.objects.get(id=1)
        objct.start_date = dt.strptime(self.request.session.get('start_date'), '%Y-%m-%d').date()
        objct.return_date = dt.strptime(self.request.session.get('return_date'), '%Y-%m-%d').date()
        objct.save()
        return redirect('actual_order')


class OrderUptadeView(UpdateView):

    template_name = 'carrentapp/order_update.html'
    model = Order
    form_class = OrderUpdateForm
    form_class_2 = OrderUpdateFormBlocked

    def get_form_class(self):
        order = Order.objects.get(id=self.kwargs['pk'])
        """Return the form class to use in this view."""
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_class' is not permitted."
            )
        if self.form_class and order.is_future:
            return self.form_class
        elif self.form_class and not order.is_past:
            return self.form_class_2
        else:
            if order.is_past:
                return self.form_class_2
            if self.model is not None:
                model = self.model
            elif getattr(self, 'object', None) is not None:
                model = self.object.__class__
            else:
                model = self.get_queryset().model
            if self.fields is None:
                raise ImproperlyConfigured(
                    "Using ModelFormMixin (base class of %s) without "
                    "the 'fields' attribute is prohibited." % self.__class__.__name__
                )
            return modelform_factory(model, fields=self.fields)

    def get_initial(self):
        order = Order.objects.get(id=self.kwargs['pk'])
        initial = super().get_initial()
        initial = initial.copy()
        initial['start_date'] = order.start_date
        initial['start_date'] = initial['start_date'].strftime('%Y-%m-%d')
        initial['return_date'] = order.return_date
        initial['return_date'] = initial['return_date'].strftime('%Y-%m-%d')
        return initial

    def get_success_url(self):
        return reverse('actual_order')

    def form_valid(self, form):
        option = None
        order = Order.objects.get(id=self.kwargs['pk'])
        car = order.car
        start_date = self.request.POST.get('start_date')
        if start_date is None:
            start_date = order.start_date.strftime('%Y-%m-%d')
            option = 'only_longer'
        start_date_datetime = dt.strptime(start_date, '%Y-%m-%d').date()
        return_date = self.request.POST.get('return_date')
        return_date_datetime = dt.strptime(return_date, '%Y-%m-%d').date()

        errors = order_date_validator(start_date_datetime,
                                      return_date_datetime,
                                      option=option,
                                      option_value=order.return_date)
        if errors:
            return redirect('order_update_msg', pk=self.kwargs['pk'], msg=errors)

        errors = if_entries_collide_error(start_date, return_date, car, order.id)
        if errors:
            return redirect('order_update_msg', pk=self.kwargs['pk'], msg=errors)

        form.save()
        if option == 'only_longer':
            return redirect('actual_order')

        return redirect('future_order')


class OrderDeleteView(DeleteView):
    model = Order

    def get_success_url(self):
        return reverse('actual_order')


class OrderDetailView(DetailView):
    model = Order

    def get_success_url(self):
        return reverse('actual_order')


class ActualOrderView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'carrentapp/order_actual.html'

    def get_queryset(self):
        qs = Order.objects.filter(client=self.request.user).filter(start_date__lte=datetime.date.today()).filter(
                         return_date__gte=datetime.date.today()).select_related('car')
        return qs


class HistoryOrderView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'carrentapp/order_history.html'

    def get_queryset(self):
        qs = Order.objects.filter(return_date__lt=datetime.date.today(), client=self.request.user).select_related('car')
        return qs


class FutureOrderView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'carrentapp/order_future.html'

    def get_queryset(self):
        qs = Order.objects.filter(start_date__gt=datetime.date.today(), client=self.request.user).select_related('car')
        return qs
