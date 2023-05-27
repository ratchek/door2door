from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("address-info", views.address_info, name="address-info"),
]
