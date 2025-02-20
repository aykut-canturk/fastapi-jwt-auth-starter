import unittest
from sqlmodel import Session, SQLModel, create_engine
from app.models.user import Users
from app.services.user import UserService
from app.utils.exception import ValidationError


class TestUserService(unittest.TestCase):
    def setUp(self):
        # Create in-memory database for testing
        self.engine = create_engine("sqlite:///:memory:")
        SQLModel.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        self.user_service = UserService(self.session)

        # self.clean_password = "testpass123"
        # Create sample user
        self.sample_user = Users(
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
        )

    def test_create_user(self):
        created_user = self.user_service.create(self.sample_user.model_copy())
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.email, self.sample_user.email)
        self.assertEqual(created_user.first_name, self.sample_user.first_name)
        self.assertEqual(created_user.last_name, self.sample_user.last_name)
        self.assertEqual(created_user.phone_number, self.sample_user.phone_number)
        # Hashed password should not be the same as clean password
        self.assertNotEqual(created_user.password, self.sample_user.password)
        # password should be hashed
        self.assertTrue(created_user.password.startswith("scrypt:"))

    def test_create_duplicate_user(self):
        self.user_service.create(self.sample_user)
        with self.assertRaises(ValidationError):
            self.user_service.create(self.sample_user)

    def test_get_by_email(self):
        self.user_service.create(self.sample_user)
        found_user = self.user_service.get_by_email(self.sample_user.email)
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.email, self.sample_user.email)

    def test_login_success(self):
        pwd = self.sample_user.password
        created_user = self.user_service.create(self.sample_user)
        logged_in_user = self.user_service.login(created_user.email, pwd)
        self.assertIsNotNone(logged_in_user)
        self.assertEqual(logged_in_user.email, self.sample_user.email)

    def test_login_failure_wrong_password(self):
        self.user_service.create(self.sample_user.model_copy())
        logged_in_user = self.user_service.login(
            self.sample_user.email, "wrongpassword"
        )
        self.assertIsNone(logged_in_user)

    def test_login_failure_wrong_email(self):
        logged_in_user = self.user_service.login(
            "nonexistent@example.com", "anypassword"
        )
        self.assertIsNone(logged_in_user)

    def test_delete_user(self):
        created_user = self.user_service.create(self.sample_user.model_copy())
        self.user_service.delete(created_user)
        self.assertNotEqual(created_user.email, self.sample_user.email)
        self.assertIn("-deleted-", created_user.email)


if __name__ == "__main__":
    unittest.main()
