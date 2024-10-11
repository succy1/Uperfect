from django.urls import path
from .views import ProductListView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/', ProductListView.as_view(), name='product-list')
]
