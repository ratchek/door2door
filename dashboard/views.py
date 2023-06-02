from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import nycdb
from .forms import AddressForm


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dashboard:address-info"))
    return render(request, "door2door/index.html", {})


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
