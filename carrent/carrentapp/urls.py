from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import ListView, DetailView, TemplateView

from .forms import LoginForm
from .views import CustomLoginView, RegisterView, ChangePasswordView, base_test_view, CreateOrderView, \
    OrderConfirmView, UpdateProfileUserView, FutureOrderView, HistoryOrderView, ActualOrderView
from .models import Car
from . import views

urlpatterns = [
    path('base-test/', base_test_view, name='zalogowany'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='carrentapp/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='carrentapp/logout.html'), name='logout'),
    path('registration/', RegisterView.as_view(), name='users-registration'),
    path('carlist/', ListView.as_view(model=Car), name='car_list'),
    path('cardetail/<int:pk>/', DetailView.as_view(model=Car), name="car_detail"),
    path('profile/', UpdateProfileUserView.as_view(), name='user-profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('', TemplateView.as_view(template_name='carrentapp/home_page.html'), name='main'),
    path('contact', TemplateView.as_view(template_name='carrentapp/contact.html'), name='contact'),
    path('aboutus', TemplateView.as_view(template_name='carrentapp/about.html'), name='about'),
    path('order/<int:pk>/', CreateOrderView.as_view(), name='order'),
    path('order-confirm/<int:pk>/', OrderConfirmView.as_view(), name='order_confirm'),
    path('order/<int:pk>/<str:msg>/', CreateOrderView.as_view(), name='order_msg'),
    path('order-actual/', ActualOrderView.as_view(), name='actual_order'),
    path('order-history/', HistoryOrderView.as_view(), name='history_order'),
    path('order-future/', FutureOrderView.as_view(), name='future_order')

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
