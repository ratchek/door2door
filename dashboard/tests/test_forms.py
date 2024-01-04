from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from dashboard.forms import AddressForm, VisitForm
from dashboard.models import VisitedAddress


class AddressFormTest(TestCase):
    def test_address_form_valid_data(self):
        form = AddressForm(
            data={"address-house_number": "123", "address-street_name": "Main Street"}
        )
        if not form.is_valid():
            print(form.errors)
        print(form.__dict__)
        self.assertTrue(form.is_valid())

    def test_address_form_data_cleaning(self):
        form = AddressForm(
            data={"address-house_number": "123a", "address-street_name": "main street"}
        )
        if form.is_valid():
            cleaned_data = form.cleaned_data
            self.assertEqual(cleaned_data["house_number"], "123A")
            self.assertEqual(cleaned_data["street_name"], "MAIN STREET")

    def test_address_form_no_data(self):
        form = AddressForm(data={})
        self.assertFalse(form.is_valid())
        print(form.errors)
        self.assertEquals(
            form.errors,
            {
                "house_number": ["This field is required."],
                "street_name": ["This field is required."],
            },
        )


class VisitFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="12345")

    def test_visit_form_valid_data(self):
        form = VisitForm(
            data={
                "visit-house_number": "123",
                "visit-street_name": "Main Street",
                "visit-knocked": True,
                "visit-door_opened": False,
                "visit-owners_available": True,
                "visit-notes": "Test note",
            },
            instance=VisitedAddress(
                visiting_agent=self.user, date_of_visit=date.today()
            ),
        )
        self.assertTrue(form.is_valid())

    def test_visit_form_save(self):
        form = VisitForm(
            data={
                "visit-house_number": "123",
                "visit-street_name": "Main Street",
                "visit-knocked": True,
                "visit-door_opened": False,
                "visit-owners_available": True,
                "visit-notes": "Test note",
            },
            instance=VisitedAddress(
                visiting_agent=self.user, date_of_visit=date.today()
            ),
        )
        visit = form.save()
        self.assertEqual(visit.house_number, "123")
        self.assertEqual(visit.street_name, "MAIN STREET")
        self.assertEqual(visit.knocked, True)
        self.assertEqual(visit.door_opened, False)
        self.assertEqual(visit.owners_available, True)
        self.assertEqual(visit.notes, "Test note")
