import logging
from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import nycdb
from .forms import AddressForm, VisitForm
from .models import VisitedAddress

logger = logging.getLogger(__name__)


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("address-info"))
    return render(request, "door2door/index.html", {})


@login_required
def address_info(request, house_number=None, street_name=None):
    if request.method == "POST":
        # Make sure to save any data that has been inputed
        # (this should be done both, when clicking the save button AND when clicking the search button)

        logger.warning("POST request detected")
        visit_form = VisitForm(request.POST, prefix="visit")
        if visit_form.is_valid() and visit_form.has_changed():
            cleaned = visit_form.cleaned_data
            logger.warning("Form data cleaned")
            # TODO check if data was modified
            # TODO A hidden field witht the building ID so I don't have to
            # requery the database every time

            building_id = cleaned["building_id"]
            # Check if there was already a visit today
            todays_visit = VisitedAddress.objects.filter(
                building_id=building_id,
                visiting_agent=request.user,
                date_of_visit=date.today(),
            )
            if todays_visit:
                logger.warning("Updating object (since there's already a visit today)")
                todays_visit[0].knocked = cleaned["knocked"]
                todays_visit[0].door_opened = cleaned["door_opened"]
                todays_visit[0].owners_available = cleaned["owners_available"]
                todays_visit[0].notes = cleaned["notes"]
                todays_visit[0].save()
            else:
                logger.warning("Creating object")
                VisitedAddress.objects.create(
                    house_number=nycdb.get_building_house_number(building_id),
                    street_name=nycdb.get_building_street_name(building_id),
                    visiting_agent=request.user,
                    building_id=building_id,
                    date_of_visit=date.today(),
                    knocked=cleaned["knocked"],
                    door_opened=cleaned["door_opened"],
                    owners_available=cleaned["owners_available"],
                    notes=cleaned["notes"],
                )
            logger.warning("Form data saved")

        # If a new address is being searched
        if "search" in request.POST:
            # Make sure that any information added to the VisitForm is saved
            # visit_form = VisitForm(request.POST, prefix="visit")
            # if visit_form.has_changed():
            address_form = AddressForm(request.POST, prefix="address")
            if address_form.is_valid():
                cleaned = address_form.cleaned_data
                return HttpResponseRedirect(
                    reverse(
                        "address-info",
                        kwargs={
                            "house_number": cleaned["house_number"],
                            "street_name": cleaned["street_name"],
                        },
                    )
                )

        return HttpResponseRedirect(
            reverse(
                "address-info",
                kwargs={
                    "house_number": house_number,
                    "street_name": street_name,
                },
            )
        )

    # GET
    else:
        # Create blank form for search
        landlords = address = past_visits = current_visit_form = None
        address = None
        if house_number and street_name:
            landlords = nycdb.get_landlords(street_name, house_number)
            address = house_number + " " + street_name
            building_id = nycdb.get_building_id(street_name, house_number)
            past_visits = VisitedAddress.objects.filter(
                building_id=building_id,
                visiting_agent=request.user,
                date_of_visit__lt=date.today(),
            ).order_by("-date_of_visit")
            todays_visit = VisitedAddress.objects.filter(
                building_id=building_id,
                visiting_agent=request.user,
                date_of_visit=date.today(),
            )
            search_form = AddressForm(
                initial={"house_number": house_number, "street_name": street_name}
            )
            if todays_visit:
                current_visit_form = VisitForm(instance=todays_visit[0])
            else:
                current_visit_form = VisitForm(initial={"building_id": building_id})

        else:
            search_form = AddressForm()

    return render(
        request,
        "door2door/address_info.html",
        {
            "landlords": landlords,
            "search_form": search_form,
            "address": address,
            "house_number": house_number,
            "street_name": street_name,
            "past_visits": past_visits,
            "current_visit_form": current_visit_form,
        },
    )


# @login_required
# def address_info(request):
#     if request.method == "POST":
#         # If a new address is being searched
#         if "search" in request.POST:
#             # Make sure that any information added to the VisitForm is saved
#             # visit_form = VisitForm(request.POST, prefix="visit")
#             # if visit_form.has_changed():
#             address_form = AddressForm(request.POST, prefix="address")
#             if address_form.is_valid():
#                 cleaned = address_form.cleaned_data
#                 landlords = nycdb.get_landlords(
#                     cleaned["street_name"], cleaned["house_number"]
#                 )
#                 address = cleaned["house_number"] + " " + cleaned["street_name"]
#                 blank_form = AddressForm()

#                 # Create a new, blank form to attach to new page
#                 return render(
#                     request,
#                     "door2door/address_info.html",
#                     {"landlords": landlords, "form": blank_form, "address": address},
#                 )
#         # If the save button was hit
#         if "save" in request.POST:
#             logger.warning("Form being saved")

#     # GET
#     else:
#         # Create blank form for search
#         blank_form = AddressForm()

#     return render(request, "door2door/address_info.html", {"form": blank_form})
