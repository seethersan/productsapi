from django.test import TestCase
from django.test import Client

from users.models import User

class UserTest(TestCase):


    def test_document_id_min_length(self):
        u = User(document_id="1234567",name="Luis",profession="Ing de Sistemas")
        try:
            u.validate_user()
        except Exception as e:
            self.assertTrue('document_id' in e.args[0][0].args[0])

    def test_document_id_max_length(self):
        u = User(document_id="123456789123",name="Luis",profession="Ing de Sistemas")
        try:
            u.validate_user()
        except Exception as e:
            self.assertTrue('document_id' in e.args[0][0].args[0])

    def test_name_min_length(self):
        u = User(document_id="12345678",name="Lu",profession="Ing de Sistemas")
        try:
            u.validate_user()
        except Exception as e:
            self.assertTrue('name' in e.args[0][0].args[0])

    def test_name_max_length(self):
        u = User(document_id="12345678",name="12345678901234567890123456789012345678901234567890123456",
                profession="Ing de Sistemas")
        try:
            u.validate_user()
        except Exception as e:
            self.assertTrue('name' in e.args[0][0].args[0])

    def test_profession_min_length(self):
        u = User(document_id="12345678",name="Luis",profession="Ing de Sistemas")
        try:
            u.validate_user()
        except Exception as e:
            self.assertTrue('profession' in e.args[0][0].args[0])

    def test_profession_max_length(self):
        u = User(document_id="12345678",name="Luis",profession="Ing de Sistemas")
        try:
            u.validate_user()
        except Exception as e:
            self.assertTrue('profession' in e.args[0][0].args[0])