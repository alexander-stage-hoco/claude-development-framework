Feature: User Registration (UC-001)
  As an API client
  I want to create a new user account
  So that users can access the system

  Background:
    Given I am an API client
    And the system is operational

  Scenario: Successfully create a new user
    When I POST to "/api/v1/users" with the following data:
      | field    | value                |
      | email    | newuser@example.com  |
      | username | newuser              |
      | password | SecurePass123!       |
    Then I receive a 201 status code
    And the response contains a user ID
    And the response contains email "newuser@example.com"
    And the response contains username "newuser"
    And the response does not contain the password
    And the response does not contain "hashed_password"

  Scenario: Reject duplicate email
    Given a user exists with email "existing@example.com"
    When I POST to "/api/v1/users" with the following data:
      | field    | value                |
      | email    | existing@example.com |
      | username | newuser              |
      | password | SecurePass123!       |
    Then I receive a 400 status code
    And the error message contains "Email already registered"

  Scenario: Reject duplicate username
    Given a user exists with username "existinguser"
    When I POST to "/api/v1/users" with the following data:
      | field    | value                  |
      | email    | newuser@example.com    |
      | username | existinguser           |
      | password | SecurePass123!         |
    Then I receive a 400 status code
    And the error message contains "Username already exists"

  Scenario: Reject invalid email format
    When I POST to "/api/v1/users" with the following data:
      | field    | value           |
      | email    | not-an-email    |
      | username | testuser        |
      | password | SecurePass123!  |
    Then I receive a 422 status code

  Scenario: Reject weak password
    When I POST to "/api/v1/users" with the following data:
      | field    | value              |
      | email    | test@example.com   |
      | username | testuser           |
      | password | weak               |
    Then I receive a 422 status code

  Scenario: Reject invalid username format
    When I POST to "/api/v1/users" with the following data:
      | field    | value              |
      | email    | test@example.com   |
      | username | ab                 |
      | password | SecurePass123!     |
    Then I receive a 422 status code

  Scenario Outline: Create users with various valid formats
    When I POST to "/api/v1/users" with the following data:
      | field    | value       |
      | email    | <email>     |
      | username | <username>  |
      | password | <password>  |
    Then I receive a 201 status code
    And the response contains email "<email>"
    And the response contains username "<username>"

    Examples:
      | email                | username    | password         |
      | user1@example.com    | user123     | Password123!     |
      | test.user@domain.co  | test_user   | SecureP@ss1      |
      | admin@company.org    | admin-user  | C0mpl3xP@ssw0rd  |
