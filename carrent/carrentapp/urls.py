from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import ListView, DetailView, TemplateView


from carrentapp.views import base_test_view, CreateOrderView, FutureOrderView,\
                                HistoryOrderView, ActualOrderView, PickOrderDate,\
                                OrderUptadeView, OrderDeleteView, OrderDetailView
from carrentapp.models import Car

urlpatterns = [
    path('base-test/', base_test_view, name='zalogowany'),
    path('carlist/', ListView.as_view(model=Car), name='car_list'),
    path('cardetail/<int:pk>/', DetailView.as_view(model=Car), name="car_detail"),
    path('', TemplateView.as_view(template_name='carrentapp/home_page.html'), name='main'),
    path('contact', TemplateView.as_view(template_name='carrentapp/contact.html'), name='contact'),
    path('aboutus', TemplateView.as_view(template_name='carrentapp/about.html'), name='about'),
    path('order/<int:pk>/', PickOrderDate.as_view(), name='order'),
    path('order/<int:pk>/<str:msg>/', PickOrderDate.as_view(), name='order_msg'),
    path('order-confirm/', CreateOrderView.as_view(), name='order_confirm'),
    path('order-detail/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order-delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
    path('order-actual/', ActualOrderView.as_view(), name='actual_order'),
    path('order-history/', HistoryOrderView.as_view(), name='history_order'),
    path('order-future/', FutureOrderView.as_view(), name='future_order'),
    path('order-update/<int:pk>', OrderUptadeView.as_view(), name='order_update'),
    path('order-update/<int:pk>/<str:msg>/', OrderUptadeView.as_view(), name='order_update_msg'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
