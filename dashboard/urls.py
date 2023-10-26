from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "about/",
        login_required(TemplateView.as_view(template_name="dashboard/about.html")),
        name="about",
    ),
    path(
        "faq/",
        login_required(TemplateView.as_view(template_name="dashboard/faq.html")),
        name="faq",
    ),
    path("address-info/", views.address_info, name="address-info"),
    re_path(
        r"^address-info/(?P<house_number>[-\w ]+)/(?P<street_name>[-\w ]+)$",
        views.address_info,
        name="address-info",
    ),
    re_path(
        r"^submit_visit_info/(?P<house_number>[-\w ]+)/(?P<street_name>[-\w ]+)$",
        views.submit_visit_info,
        name="submit-visit-info",
    ),
    re_path(
        "search",
        views.search,
        name="search",
    ),
]
