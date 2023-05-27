from django.http import HttpResponse
from django.shortcuts import render

from . import nycdb
from .forms import AddressForm


def index(request):
    return HttpResponse("Hello, world. This is gonna be a dashboard.")


def landlords(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            landlords = nycdb.get_landlords(
                form.cleaned_data["street_name"], form.cleaned_data["street_number"]
            )
            blank_form = AddressForm()
            # Create a new, blank form to attach to new page
            return render(
                request,
                "door2door/landlord.html",
                {"landlords": landlords, "form": blank_form},
            )

    # if a GET (or any other method) we'll create a blank form
    else:
        blank_form = AddressForm()

    return render(request, "door2door/landlord.html", {"form": blank_form})
