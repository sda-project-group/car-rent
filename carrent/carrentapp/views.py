from django.shortcuts import render

# Create your views here.


def base_test_view(request):
    return render(request, 'carrent/base.html')