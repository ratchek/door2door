from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase

from dashboard.models import VisitedAddress


class VisitedAddressTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create_user(username="testuser", password="12345")
        cls.address = VisitedAddress.objects.create(
            house_number="123",
            street_name="Main Street",
            visiting_agent=cls.user,
            date_of_visit=date.today(),
            knocked=True,
            door_opened=False,
            owners_available=True,
            notes="Test note",
        )

    def test_visited_address_creation(self):
        """
        Test the creation of a VisitedAddress instance.
        """
        self.assertIsInstance(self.address, VisitedAddress)

    def test_field_content(self):
        """
        Test the content of each field in the VisitedAddress instance.
        """
        self.assertEqual(self.address.house_number, "123")  # Uppercase check
        self.assertEqual(self.address.street_name, "MAIN STREET")  # Uppercase check
        self.assertEqual(self.address.visiting_agent, self.user)
        self.assertTrue(self.address.knocked)
        self.assertFalse(self.address.door_opened)
        self.assertTrue(self.address.owners_available)
        self.assertEqual(self.address.notes, "Test note")

    def test_string_representation(self):
        """
        Test the string representation of the VisitedAddress instance.
        """
        expected_string = f"{self.address.house_number} {self.address.street_name} - {self.address.visiting_agent.username} - {self.address.date_of_visit}"
        self.assertEqual(str(self.address), expected_string)

    def test_save_method(self):
        """
        Test the overridden save method to ensure it correctly converts house number and street name to uppercase.
        """
        new_address = VisitedAddress.objects.create(
            house_number="456b",
            street_name="elm street",
            visiting_agent=self.user,
            date_of_visit=date.today(),
            knocked=False,
            door_opened=True,
            owners_available=False,
            notes="",
        )
        self.assertEqual(new_address.house_number, "456B")
        self.assertEqual(new_address.street_name, "ELM STREET")
