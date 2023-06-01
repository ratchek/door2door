from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from . import nycdb
from .forms import AddressForm


def index(request):
    return HttpResponse("Hello, world. This is gonna be a dashboard.")


@login_required
def address_info(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            landlords = nycdb.get_landlords(
                cleaned["street_name"], cleaned["street_number"]
            )
            address = cleaned["street_number"] + " " + cleaned["street_name"]
            blank_form = AddressForm()
            # Create a new, blank form to attach to new page
            return render(
                request,
                "door2door/address_info.html",
                {"landlords": landlords, "form": blank_form, "address": address},
            )

    # if a GET (or any other method) we'll create a blank form
    else:
        blank_form = AddressForm()

    return render(request, "door2door/address_info.html", {"form": blank_form})
