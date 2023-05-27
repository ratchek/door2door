from django import forms


class AddressForm(forms.Form):
    street_number = forms.CharField(label="House Number", max_length=10)
    street_name = forms.CharField(label="Street Name", max_length=30)
