from django.http import HttpResponse
from django.shortcuts import render

from . import nycdb


def index(request):
    return HttpResponse("Hello, world. This is gonna be a dashboard.")


def landlords(request):
    landlords = nycdb.get_landlords("74th street", "2150")
    return render(request, "door2door/landlord.html", {"landlords": landlords})
