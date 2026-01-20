"""Helper utilities for tests."""
import re
from typing import Any, Dict, List
from pydantic import ValidationError


def validate_email(email: str) -> bool:
    """Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_schema(data: Any, model: type) -> bool:
    """Validate data against Pydantic model.

    Args:
        data: Data to validate
        model: Pydantic model class

    Returns:
        True if valid, False otherwise
    """
    try:
        model.model_validate(data)
        return True
    except ValidationError as e:
        print(f"Validation error: {e}")
        return False


def assert_status_code(response, expected_code: int):
    """Assert response status code.

    Args:
        response: Response object
        expected_code: Expected status code

    Raises:
        AssertionError: If status code doesn't match
    """
    assert response.status_code == expected_code, \
        f"Expected status code {expected_code}, got {response.status_code}. Response: {response.text}"


def assert_content_type(response, expected_type: str = "application/json"):
    """Assert response content type.

    Args:
        response: Response object
        expected_type: Expected content type

    Raises:
        AssertionError: If content type doesn't match
    """
    content_type = response.headers.get('Content-Type', '')
    assert expected_type in content_type, \
        f"Expected content type '{expected_type}', got '{content_type}'"


def assert_response_time(response, max_time: float = 2.0):
    """Assert response time is within limit.

    Args:
        response: Response object
        max_time: Maximum allowed time in seconds

    Raises:
        AssertionError: If response time exceeds limit
    """
    elapsed = response.elapsed.total_seconds()
    assert elapsed <= max_time, \
        f"Response time {elapsed}s exceeded limit {max_time}s"


def get_field_from_response(response, field: str) -> Any:
    """Get field value from JSON response.

    Args:
        response: Response object
        field: Field name

    Returns:
        Field value
    """
    return response.json().get(field)


def assert_field_exists(data: Dict, field: str):
    """Assert field exists in data.

    Args:
        data: Dictionary to check
        field: Field name

    Raises:
        AssertionError: If field doesn't exist
    """
    assert field in data, f"Field '{field}' not found in response"


def assert_field_type(data: Dict, field: str, expected_type: type):
    """Assert field has expected type.

    Args:
        data: Dictionary to check
        field: Field name
        expected_type: Expected field type

    Raises:
        AssertionError: If field type doesn't match
    """
    assert_field_exists(data, field)
    actual_value = data[field]
    assert isinstance(actual_value, expected_type), \
        f"Field '{field}' expected type {expected_type.__name__}, got {type(actual_value).__name__}"


def assert_list_not_empty(data: List):
    """Assert list is not empty.

    Args:
        data: List to check

    Raises:
        AssertionError: If list is empty
    """
    assert isinstance(data, list), f"Expected list, got {type(data).__name__}"
    assert len(data) > 0, "List is empty"
