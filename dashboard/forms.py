from django import forms

from .models import VisitedAddress


class CustomCheckboxInput(forms.CheckboxInput):
    template_name = "door2door/checkbox_custom.html"


class AddressForm(forms.Form):
    house_number = forms.CharField(label="House Number", max_length=10)
    street_name = forms.CharField(label="Street Name", max_length=30)
    prefix = "address"

    def clean_house_number(self):
        data = self.cleaned_data["house_number"]
        data.upper()
        return data

    def clean_street_name(self):
        data = self.cleaned_data["street_name"]
        data.upper()
        return data


class VisitForm(forms.ModelForm):
    class Meta:
        model = VisitedAddress
        fields = [
            "house_number",
            "street_name",
            "knocked",
            "door_opened",
            "owners_available",
            "notes",
        ]
        widgets = {
            "house_number": forms.HiddenInput(),
            "street_name": forms.HiddenInput(),
        }

    prefix = "visit"
