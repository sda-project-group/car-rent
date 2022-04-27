from django.urls import path
from . import views

urlpatterns = [
    path('base-test/', views.base_test_view)
]