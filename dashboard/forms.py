from django import forms

from .models import VisitedAddress


class CustomCheckboxInput(forms.CheckboxInput):
    template_name = "door2door/checkbox_custom.html"


class AddressForm(forms.Form):
    house_number = forms.CharField(label="House Number", max_length=10)
    street_name = forms.CharField(label="Street Name", max_length=30)
    prefix = "address"


class VisitForm(forms.ModelForm):
    class Meta:
        model = VisitedAddress
        fields = [
            "nycdb_building_id",
            "knocked",
            "door_opened",
            "owners_available",
            "notes",
        ]
        widgets = {
            "nycdb_building_id": forms.HiddenInput(),
        }

    prefix = "visit"
