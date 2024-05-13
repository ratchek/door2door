from django import forms

from .models import VisitedAddress


class CustomCheckboxInput(forms.CheckboxInput):
    template_name = "door2door/checkbox_custom.html"


class AddressForm(forms.Form):
    """
    Form for inputting address details, specifically the house number and street name.

    This form is used to search for buildings based on street name and house number.
    The input data for both fields is converted to uppercase.
    """

    house_number = forms.CharField(label="House Number", max_length=10)
    street_name = forms.CharField(label="Street Name", max_length=30)
    prefix = "address"

    def clean_house_number(self):
        data = self.cleaned_data["house_number"]
        data = data.upper()
        return data

    def clean_street_name(self):
        data = self.cleaned_data["street_name"]
        data = data.upper()
        return data


class VisitForm(forms.ModelForm):
    """
    Model form linked to the VisitedAddress model.

    This form is used to store details of a current visit to an address, including whether the door was knocked,
    if it was opened, whether the owners were available, and any additional notes.
    The 'house_number' and 'street_name' fields are hidden as they are prefilled.
    """

    class Meta:
        model = VisitedAddress
        fields = [
            "house_number",
            "street_name",
            "knocked",
            "door_opened",
            "owners_available",
            "owners_not_interested",
            "notes",
        ]
        widgets = {
            "house_number": forms.HiddenInput(),
            "street_name": forms.HiddenInput(),
        }

    prefix = "visit"
