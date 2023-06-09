from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("address-info", views.address_info, name="address-info"),
    re_path(
        r"^address-info/(?P<house_number>[-\w ]+)/(?P<street_name>[-\w ]+)$",
        views.address_info,
        name="address-info",
    ),
]
