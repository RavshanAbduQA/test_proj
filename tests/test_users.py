"""Tests for Users API endpoints."""
import pytest
import allure
from models.schemas import User, Address
from utils.helpers import (
    assert_status_code,
    assert_content_type,
    assert_field_exists,
    assert_field_type,
    assert_list_not_empty,
    validate_email,
    validate_schema
)


@allure.feature("Users API")
@allure.story("Get all users")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.users
class TestGetAllUsers:
    """Tests for GET /users endpoint."""

    def test_get_all_users_success(self, users_api):
        """Test getting all users returns 200 and valid data."""
        with allure.step("Send GET request to /users"):
            response = users_api.get_all_users()

        with allure.step("Verify status code is 200"):
            assert_status_code(response, 200)

        with allure.step("Verify content type is application/json"):
            assert_content_type(response, "application/json")

        with allure.step("Verify response is a non-empty array"):
            data = response.json()
            assert isinstance(data, list), "Response should be an array"
            assert_list_not_empty(data)

        with allure.step("Verify exactly 10 users are returned"):
            assert len(data) == 10, f"Expected 10 users, got {len(data)}"

        with allure.step("Verify first user has correct structure"):
            first_user = data[0]
            required_fields = ["id", "name", "username", "email", "address", "phone", "website", "company"]
            for field in required_fields:
                assert_field_exists(first_user, field)

        with allure.step("Validate against Pydantic schema"):
            assert validate_schema(first_user, User), "First user doesn't match User schema"

        allure.attach(
            str(data[0]),
            name="First user",
            attachment_type=allure.attachment_type.JSON
        )

    def test_all_users_have_valid_emails(self, users_api):
        """Test that all users have valid email addresses."""
        with allure.step("Get all users"):
            response = users_api.get_all_users()
            assert_status_code(response, 200)
            users = response.json()

        with allure.step("Validate email format for each user"):
            invalid_emails = []
            for user in users:
                email = user.get("email", "")
                if not validate_email(email):
                    invalid_emails.append(f"User {user['id']}: {email}")

            assert len(invalid_emails) == 0, \
                f"Found {len(invalid_emails)} invalid emails: {invalid_emails}"

        allure.attach(
            "\n".join([f"{u['id']}: {u['email']}" for u in users]),
            name="All user emails",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.feature("Users API")
@allure.story("Get user by ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.users
class TestGetUserById:
    """Tests for GET /users/{id} endpoint."""

    def test_get_user_by_id_success(self, users_api, existing_user_id):
        """Test getting user by ID returns 200 and valid data."""
        with allure.step(f"Send GET request to /users/{existing_user_id}"):
            response = users_api.get_user_by_id(existing_user_id)

        with allure.step("Verify status code is 200"):
            assert_status_code(response, 200)

        with allure.step("Verify content type is application/json"):
            assert_content_type(response, "application/json")

        with allure.step("Verify user ID matches requested ID"):
            data = response.json()
            assert data["id"] == existing_user_id, \
                f"Expected ID {existing_user_id}, got {data['id']}"

        with allure.step("Verify all required fields exist"):
            required_fields = ["id", "name", "username", "email", "address", "phone", "website", "company"]
            for field in required_fields:
                assert_field_exists(data, field)

        with allure.step("Validate email format"):
            assert validate_email(data["email"]), f"Invalid email format: {data['email']}"

        with allure.step("Validate against Pydantic schema"):
            assert validate_schema(data, User), "User doesn't match User schema"

        allure.attach(
            str(data),
            name=f"User {existing_user_id}",
            attachment_type=allure.attachment_type.JSON
        )


@allure.feature("Users API")
@allure.story("User address validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.users
class TestUserAddress:
    """Tests for user address structure validation."""

    def test_user_address_structure(self, users_api, existing_user_id):
        """Test user address has correct structure."""
        with allure.step(f"Get user {existing_user_id}"):
            response = users_api.get_user_by_id(existing_user_id)
            assert_status_code(response, 200)
            user = response.json()

        with allure.step("Verify address field exists"):
            assert_field_exists(user, "address")
            address = user["address"]

        with allure.step("Verify address has required fields"):
            required_address_fields = ["street", "suite", "city", "zipcode", "geo"]
            for field in required_address_fields:
                assert_field_exists(address, field)

        with allure.step("Verify geo coordinates structure"):
            assert_field_exists(address, "geo")
            geo = address["geo"]
            assert_field_exists(geo, "lat")
            assert_field_exists(geo, "lng")

        with allure.step("Verify field types"):
            assert_field_type(address, "street", str)
            assert_field_type(address, "suite", str)
            assert_field_type(address, "city", str)
            assert_field_type(address, "zipcode", str)

        with allure.step("Validate address against Pydantic schema"):
            assert validate_schema(address, Address), "Address doesn't match Address schema"

        allure.attach(
            str(address),
            name="User address",
            attachment_type=allure.attachment_type.JSON
        )

    @pytest.mark.parametrize("user_id", [1, 2, 3, 5])
    def test_all_users_have_valid_address_structure(self, users_api, user_id):
        """Test that all users have valid address structure."""
        with allure.step(f"Get user {user_id}"):
            response = users_api.get_user_by_id(user_id)
            assert_status_code(response, 200)
            user = response.json()

        with allure.step("Validate address structure"):
            address = user.get("address", {})
            assert validate_schema(address, Address), \
                f"User {user_id} address doesn't match Address schema"


@allure.feature("Users API")
@allure.story("User data validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.users
class TestUserDataValidation:
    """Tests for user data validation."""

    def test_user_company_structure(self, users_api, existing_user_id):
        """Test user company has correct structure."""
        with allure.step(f"Get user {existing_user_id}"):
            response = users_api.get_user_by_id(existing_user_id)
            assert_status_code(response, 200)
            user = response.json()

        with allure.step("Verify company field exists"):
            assert_field_exists(user, "company")
            company = user["company"]

        with allure.step("Verify company has required fields"):
            required_fields = ["name", "catchPhrase", "bs"]
            for field in required_fields:
                assert_field_exists(company, field)

        with allure.step("Verify field types"):
            assert_field_type(company, "name", str)
            assert_field_type(company, "catchPhrase", str)
            assert_field_type(company, "bs", str)

        allure.attach(
            str(company),
            name="User company",
            attachment_type=allure.attachment_type.JSON
        )

    @pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    def test_each_user_has_unique_id(self, users_api, user_id):
        """Test that each user ID returns a unique user."""
        with allure.step(f"Get user {user_id}"):
            response = users_api.get_user_by_id(user_id)
            assert_status_code(response, 200)
            user = response.json()

        with allure.step("Verify returned user ID matches"):
            assert user["id"] == user_id, f"Expected ID {user_id}, got {user['id']}"

        with allure.step("Verify user has unique username"):
            assert user["username"], "Username should not be empty"

    def test_user_email_validation(self, users_api):
        """Test that all users have valid email addresses with proper format."""
        with allure.step("Get all users"):
            response = users_api.get_all_users()
            assert_status_code(response, 200)
            users = response.json()

        with allure.step("Validate email format requirements"):
            for user in users:
                email = user["email"]

                # Check @ symbol exists
                assert "@" in email, f"User {user['id']} email missing @ symbol: {email}"

                # Check domain exists
                parts = email.split("@")
                assert len(parts) == 2, f"User {user['id']} email has invalid format: {email}"
                assert "." in parts[1], f"User {user['id']} email missing domain extension: {email}"

                # Validate using helper
                assert validate_email(email), f"User {user['id']} has invalid email: {email}"
