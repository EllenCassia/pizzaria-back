from unittest import TestCase
from unittest.mock import MagicMock
from pizzaria_api.business.services.user_services import UserService

class TestUserService(TestCase):
    
    def setUp(self):
        self.service = UserService()
        self.service.create_user = MagicMock(return_value={"name_empresa": "Test", "email": "test@example.com"})

    def test_create_user(self):
        user_json = {"id": 1, "name_empresa": "Test", "email": "test@example.com", "password": "password"}
        response = self.service.create_user(user_json)
        self.assertEqual(response["name_empresa"], "Test")
        self.assertEqual(response["email"], "test@example.com")

        
