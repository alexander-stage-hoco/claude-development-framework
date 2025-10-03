"""
BDD Step Definitions for User Registration (UC-001)

Implements Given/When/Then steps for pytest-bdd.
"""

import pytest
from pytest_bdd import given, when, then, scenarios, parsers
from fastapi import status

from src.services.user_service import UserService
from src.models.schemas import UserCreate

# Load scenarios from feature file
scenarios("../features/UC-001-create-user.feature")


# ============================================================================
# GIVEN Steps - Set up test context
# ============================================================================


@given("I am an API client")
def api_client(client):
    """Set up API client context."""
    # Client fixture already provides this
    return client


@given("the system is operational")
def system_operational(client):
    """Verify system is operational."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK


@given(parsers.parse('a user exists with email "{email}"'))
def user_exists_with_email(db_session, email):
    """Create a user with specific email."""
    user_service = UserService(db_session)
    user_data = UserCreate(
        email=email,
        username=f"user_{email.split('@')[0]}",
        password="ExistingPass123!",
    )
    user = user_service.create_user(user_data)
    return user


@given(parsers.parse('a user exists with username "{username}"'))
def user_exists_with_username(db_session, username):
    """Create a user with specific username."""
    user_service = UserService(db_session)
    user_data = UserCreate(
        email=f"{username}@example.com",
        username=username,
        password="ExistingPass123!",
    )
    user = user_service.create_user(user_data)
    return user


# ============================================================================
# WHEN Steps - Execute actions
# ============================================================================


@when(parsers.parse('I POST to "{endpoint}" with the following data:'))
def post_to_endpoint_with_data(client, endpoint, datatable):
    """
    POST to endpoint with data from table.

    Stores response in pytest context for later assertions.
    """
    # Convert datatable to dict
    data = {}
    for row in datatable:
        data[row["field"]] = row["value"]

    # Make POST request
    response = client.post(endpoint, json=data)

    # Store response in pytest context
    return response


@pytest.fixture
def context():
    """BDD context for storing state between steps."""
    return {}


@when(
    parsers.parse('I POST to "{endpoint}" with the following data:'), target_fixture="bdd_response"
)
def post_with_data_fixture(client, endpoint, datatable, context):
    """POST to endpoint and store response in fixture."""
    data = {}
    for row in datatable:
        data[row["field"]] = row["value"]

    response = client.post(endpoint, json=data)
    context["response"] = response
    context["response_data"] = response.json() if response.content else None
    return response


# ============================================================================
# THEN Steps - Assertions
# ============================================================================


@then(parsers.parse("I receive a {status_code:d} status code"))
def verify_status_code(bdd_response, status_code):
    """Verify response status code."""
    assert bdd_response.status_code == status_code, (
        f"Expected status {status_code}, got {bdd_response.status_code}. "
        f"Response: {bdd_response.json() if bdd_response.content else 'empty'}"
    )


@then("the response contains a user ID")
def response_contains_user_id(bdd_response):
    """Verify response contains user ID."""
    data = bdd_response.json()
    assert "id" in data, f"Response missing 'id' field: {data}"
    assert data["id"] is not None


@then(parsers.parse('the response contains email "{email}"'))
def response_contains_email(bdd_response, email):
    """Verify response contains specific email."""
    data = bdd_response.json()
    assert "email" in data, f"Response missing 'email' field: {data}"
    assert data["email"] == email, f"Expected email '{email}', got '{data['email']}'"


@then(parsers.parse('the response contains username "{username}"'))
def response_contains_username(bdd_response, username):
    """Verify response contains specific username."""
    data = bdd_response.json()
    assert "username" in data, f"Response missing 'username' field: {data}"
    assert data["username"] == username, f"Expected username '{username}', got '{data['username']}'"


@then("the response does not contain the password")
def response_does_not_contain_password(bdd_response):
    """Verify response does not contain password field."""
    data = bdd_response.json()
    assert "password" not in data, f"Response should not contain 'password' field: {data}"


@then(parsers.parse('the response does not contain "{field}"'))
def response_does_not_contain_field(bdd_response, field):
    """Verify response does not contain specific field."""
    data = bdd_response.json()
    assert field not in data, f"Response should not contain '{field}' field: {data}"


@then(parsers.parse('the error message contains "{text}"'))
def error_message_contains(bdd_response, text):
    """Verify error message contains specific text."""
    data = bdd_response.json()
    assert "detail" in data, f"Response missing 'detail' field: {data}"

    detail = data["detail"]
    # Handle both string and list detail formats
    if isinstance(detail, str):
        assert text.lower() in detail.lower(), f"Expected error to contain '{text}', got: {detail}"
    elif isinstance(detail, list):
        # Validation errors are returned as list
        error_messages = " ".join(str(err) for err in detail)
        assert (
            text.lower() in error_messages.lower()
        ), f"Expected error to contain '{text}', got: {detail}"


# ============================================================================
# Additional Fixtures for BDD
# ============================================================================


@pytest.fixture
def datatable(request):
    """
    Parse datatable from Gherkin step.

    Converts Gherkin table to list of dicts.
    """
    # This is handled by pytest-bdd automatically
    # Just here for documentation
    pass
