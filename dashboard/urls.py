from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # Root URL. Redirects to the index view, primarily used for logging in.
    path("", views.index, name="index"),
    # URL for the 'About' page. Requires user authentication.
    path(
        "about/",
        login_required(TemplateView.as_view(template_name="dashboard/about.html")),
        name="about",
    ),
    # URL for the 'FAQ' page. Also requires user authentication.
    path(
        "faq/",
        login_required(TemplateView.as_view(template_name="dashboard/faq.html")),
        name="faq",
    ),
    # URL for viewing address information without parameters.
    path("address-info/", views.address_info, name="address-info"),
    # URL pattern for accessing detailed information about a specific address.
    # URL pattern using regex to match 'address-info' followed by house number and street name.
    # The regex pattern `(?P<house_number>[-\w ]+)` matches any combination of alphanumeric characters,
    # hyphens, and spaces for the house number. Similarly, `(?P<street_name>[-\w ]+)` matches the street name.
    # These are captured as named groups for use in the view.
    # The alphanumeric nature of the pattern for house number is to accomodate building numbers like 32-35 or 12E
    re_path(
        r"^address-info/(?P<house_number>[-\w ]+)/(?P<street_name>[-\w ]+)$",
        views.address_info,
        name="address-info",
    ),
    # URL for submitting visit information for a specific address.
    re_path(
        r"^submit_visit_info/(?P<house_number>[-\w ]+)/(?P<street_name>[-\w ]+)$",
        views.submit_visit_info,
        name="submit-visit-info",
    ),
    # URL for the search functionality, handling POST requests to search addresses.
    re_path(
        "search",
        views.search,
        name="search",
    ),
]
