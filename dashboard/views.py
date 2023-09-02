import logging
from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from . import nycdb
from .forms import AddressForm, VisitForm
from .models import VisitedAddress

logger = logging.getLogger(__name__)


def index(request):
    # Index is used strictly for logging in.
    # If user is already logged in, redirect to address-info
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("address-info"))
    return render(request, "door2door/index.html", {})


def save_visit_info_to_database(visit_form, user):
    cleaned = visit_form.cleaned_data

    nycdb_building_id = cleaned["nycdb_building_id"]
    # Check if there was already a visit today
    # TODO: write test to check that this function handles a form that returns
    # no visits today without crashing
    todays_visit = VisitedAddress.objects.filter(
        nycdb_building_id=nycdb_building_id,
        visiting_agent=user,
        date_of_visit=date.today(),
    ).first()
    # If agent already visited house today - update, else - create new record
    if todays_visit:
        logger.warning("Updating object (since there's already a visit today)")
        todays_visit.knocked = cleaned["knocked"]
        todays_visit.door_opened = cleaned["door_opened"]
        todays_visit.owners_available = cleaned["owners_available"]
        todays_visit.notes = cleaned["notes"]
        todays_visit.save()
    else:
        logger.warning("Creating object")
        VisitedAddress.objects.create(
            house_number=nycdb.get_building_house_number(nycdb_building_id),
            street_name=nycdb.get_building_street_name(nycdb_building_id),
            visiting_agent=user,
            nycdb_building_id=nycdb_building_id,
            date_of_visit=date.today(),
            knocked=cleaned["knocked"],
            door_opened=cleaned["door_opened"],
            owners_available=cleaned["owners_available"],
            notes=cleaned["notes"],
        )
    logger.warning("Form data saved")


# Save visit form info and redirect back to address-info page
@login_required
@require_POST
def submit_visit_info(request, house_number=None, street_name=None):
    visit_form = VisitForm(request.POST, prefix="visit")
    # TODO check if data was modified
    # Right now visit_form.has_changed() does nothing
    if visit_form.is_valid() and visit_form.has_changed():
        save_visit_info_to_database(visit_form, request.user)

        return HttpResponseRedirect(
            reverse(
                "address-info",
                kwargs={"house_number": house_number, "street_name": street_name},
            )
        )


#  Parse search parameters and redirect to address_info with appropriate arguments
@login_required
@require_POST
def search(request):
    # TODO check if VisitForm was modified. If yes, call save_visit_info_to_database first
    # visit_form = VisitForm(request.POST, prefix="visit")

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

    return HttpResponseRedirect(reverse("address-info"))


@login_required
def address_info(request, house_number=None, street_name=None):
    # Create blank form for search
    landlords = address = past_visits = current_visit_form = None
    address = None
    if house_number and street_name:
        landlords = nycdb.get_landlords(street_name, house_number)
        address = house_number + " " + street_name
        nycdb_building_id = nycdb.get_building_id(street_name, house_number)
        past_visits = VisitedAddress.objects.filter(
            nycdb_building_id=nycdb_building_id,
            visiting_agent=request.user,
            date_of_visit__lt=date.today(),
        ).order_by("-date_of_visit")
        todays_visit = VisitedAddress.objects.filter(
            nycdb_building_id=nycdb_building_id,
            visiting_agent=request.user,
            date_of_visit=date.today(),
        )
        search_form = AddressForm(
            initial={"house_number": house_number, "street_name": street_name}
        )
        if todays_visit:
            current_visit_form = VisitForm(instance=todays_visit[0])
        else:
            current_visit_form = VisitForm(
                initial={"nycdb_building_id": nycdb_building_id}
            )

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
