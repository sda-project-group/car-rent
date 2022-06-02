from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import DetailView, TemplateView, ListView

from .views import CreateOrderView, FutureOrderView, HistoryOrderView, ActualOrderView, PickOrderDate, car_list_view
from .models import Car, Department


urlpatterns = [
    path('carlist', car_list_view, name='car_list'),
    path('cardetail/<int:pk>/', DetailView.as_view(model=Car), name="car_detail"),
    path('', TemplateView.as_view(template_name='carrentapp/home_page.html'), name='main'),
    path('contact', TemplateView.as_view(template_name='carrentapp/contact.html'), name='contact'),
    path('aboutus', TemplateView.as_view(template_name='carrentapp/about.html'), name='about'),
    path('order/<int:pk>/', PickOrderDate.as_view(), name='order'),
    path('order/<int:pk>/<str:msg>/', PickOrderDate.as_view(), name='order_msg'),
    path('order-confirm/', CreateOrderView.as_view(), name='order_confirm'),
    path('order-actual/', ActualOrderView.as_view(), name='actual_order'),
    path('order-history/', HistoryOrderView.as_view(), name='history_order'),
    path('order-future/', FutureOrderView.as_view(), name='future_order'),
    path('departments/', ListView.as_view(model=Department), name='department_list'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
