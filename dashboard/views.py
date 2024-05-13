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
    """
    The index view, primarily used for logging in.

    If the user is already authenticated, they are redirected to the address-info view.
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("address-info"))
    return render(request, "dashboard/index.html", {})


def save_visit_info_to_database(visit_form, user):
    """
    Saves or updates a visit record in the database based on the provided form data.

    Args:
        visit_form (VisitForm): The form containing visit information.
        user (User): The user (agent) who is making the entry.

    If a visit record for the same address and agent already exists on the same day, it is updated.
    Otherwise, a new record is created.
    """
    cleaned = visit_form.cleaned_data

    # Check if there was already a visit today
    # TODO: write test to check that this function handles a form that returns
    # no visits today without crashing
    todays_visit = VisitedAddress.objects.filter(
        house_number=cleaned["house_number"],
        street_name=cleaned["street_name"],
        visiting_agent=user,
        date_of_visit=date.today(),
    ).first()
    # If agent already visited house today - update, else - create new record
    if todays_visit:
        logger.warning("Updating object (since there's already a visit today)")
        todays_visit.knocked = cleaned["knocked"]
        todays_visit.door_opened = cleaned["door_opened"]
        todays_visit.owners_available = cleaned["owners_available"]
        todays_visit.owners_not_interested = cleaned["owners_not_interested"]
        todays_visit.notes = cleaned["notes"]
        todays_visit.save()
    else:
        logger.warning("Creating object")
        VisitedAddress.objects.create(
            house_number=cleaned["house_number"],
            street_name=cleaned["street_name"],
            visiting_agent=user,
            date_of_visit=date.today(),
            knocked=cleaned["knocked"],
            door_opened=cleaned["door_opened"],
            owners_available=cleaned["owners_available"],
            owners_not_interested=cleaned["owners_not_interested"],
            notes=cleaned["notes"],
        )
    logger.warning("Form data saved")


@login_required
@require_POST
def save_visit_info(request):
    """
    Processes the POST request to save visit information.

    This view is triggered by the VisitForm submission.
    If the form is valid, the data is saved using the save_visit_info_to_database function.
    """
    visit_form = VisitForm(request.POST, prefix="visit")
    # TODO check if data was modified
    # Right now visit_form.has_changed() does nothing
    if visit_form.is_valid() and visit_form.has_changed():
        save_visit_info_to_database(visit_form, request.user)


# Save visit form info and redirect back to address-info page
@login_required
@require_POST
def submit_visit_info(request, house_number, street_name):
    """
    Handles the POST request for submitting visit information.
    Product of refactoring. For now, just a wrapper around save_visit_info, but will be utilized in the future to keep code DRY.

    Args:
        house_number (str): The house number of the visited address.
        street_name (str): The street name of the visited address.

    After processing the visit information, the user is redirected back to the address-info page.
    """
    save_visit_info(request)
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
    """
    Handles the POST request for searching an address.

    This view processes the AddressForm. If the form is valid, it redirects to the address-info view
    with the house number and street name as arguments.
    """
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
    """
    Displays information about a specific address.

    Args:
        house_number (str, optional): The house number of the address.
        street_name (str, optional): The street name of the address.

    This view shows information about the landlords, past visits, and a form for recording a new visit
    if a house number and street name are provided. Otherwise, it shows a blank search form.
    """
    # # Some house numbers have letters in them so they also need to be capitalized
    # house_number = house_number.upper()
    # street_name = street_name.upper()
    # Create blank form for search
    landlords = address = past_visits = current_visit_form = None
    address = None
    if house_number and street_name:
        landlords = nycdb.get_landlords(street_name, house_number)
        address = house_number + " " + street_name
        past_visits = VisitedAddress.objects.filter(
            street_name=street_name,
            house_number=house_number,
            visiting_agent=request.user,
            date_of_visit__lt=date.today(),
        ).order_by("-date_of_visit")
        todays_visit = VisitedAddress.objects.filter(
            street_name=street_name,
            house_number=house_number,
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
                initial={
                    "street_name": street_name,
                    "house_number": house_number,
                }
            )

    else:
        search_form = AddressForm()

    return render(
        request,
        "dashboard/address_info.html",
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
