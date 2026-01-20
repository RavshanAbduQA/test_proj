# text-file.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a professional API test automation framework for the JSONPlaceholder REST API. The project demonstrates enterprise-grade testing practices with clean architecture, comprehensive coverage, and modern tooling.

**API Under Test**: https://jsonplaceholder.typicode.com/

**Key Technologies**:
- **Python 3.9+**: Primary programming language
- **pytest**: Testing framework with fixtures and markers
- **requests**: HTTP client for API calls
- **pydantic**: Data validation and schema enforcement
- **allure-pytest**: Rich test reporting
- **GitHub Actions**: CI/CD pipeline

## Architecture & Design Philosophy

### Layered Architecture

The project follows a **3-layer architecture** pattern:

```
┌─────────────────────────────────────────┐
│  TEST LAYER (tests/)                    │
│  - Test classes and functions           │
│  - Allure decorators and steps          │
│  - Assertions and validations           │
└──────────────┬──────────────────────────┘
               │
┌──────────────┴──────────────────────────┐
│  API LAYER (api/)                       │
│  - PostsAPI, UsersAPI, CommentsAPI      │
│  - Page Object Pattern for APIs         │
│  - Business logic wrappers              │
└──────────────┬──────────────────────────┘
               │
┌──────────────┴──────────────────────────┐
│  CLIENT LAYER (api/base_client.py)      │
│  - BaseAPIClient (HTTP methods)         │
│  - Session management                   │
│  - Logging and error handling           │
└──────────────┬──────────────────────────┘
               │
               ▼
           requests library
```

### Design Patterns

#### 1. **Page Object Pattern (for APIs)**

Each API resource has its own class that encapsulates endpoint operations:

```python
# api/posts_api.py
class PostsAPI(BaseAPIClient):
    def get_all_posts(self) -> Response:
        return self.get("/posts")

    def get_post_by_id(self, post_id: int) -> Response:
        return self.get(f"/posts/{post_id}")
```

**Why**: Provides abstraction, reusability, and maintainability. Changes to endpoints are localized.

#### 2. **Facade Pattern**

`BaseAPIClient` acts as a facade, providing a simplified interface to the requests library:

```python
# api/base_client.py
class BaseAPIClient:
    def get(self, endpoint: str, **kwargs) -> Response:
        url = self._build_url(endpoint)
        self._log_request('GET', url, **kwargs)
        response = self.session.get(url, timeout=self.timeout, **kwargs)
        self._log_response(response)
        return response
```

**Why**: Centralizes logging, error handling, and configuration. All API clients inherit common behavior.

#### 3. **Fixture Pattern**

pytest fixtures provide reusable setup/teardown and test data:

```python
# conftest.py
@pytest.fixture(scope="session")
def posts_api():
    client = PostsAPI()
    yield client
    client.close()
```

**Why**: Ensures proper resource management, reduces code duplication, and promotes clean tests.

#### 4. **Data Validation with Pydantic**

Pydantic models enforce strict schema validation:

```python
# models/schemas.py
class Post(BaseModel):
    userId: int = Field(..., gt=0)
    id: int = Field(..., gt=0)
    title: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)
```

**Why**: Catches schema violations early, provides type safety, and documents expected data structures.

## Project Structure

```
api_test/
├── api/                        # API Client Layer
│   ├── base_client.py         # Base HTTP client with logging
│   ├── posts_api.py           # Posts endpoint wrapper
│   ├── users_api.py           # Users endpoint wrapper
│   └── comments_api.py        # Comments endpoint wrapper
│
├── models/                     # Data Models
│   └── schemas.py             # Pydantic models for validation
│
├── tests/                      # Test Layer
│   ├── test_posts.py          # Posts API tests (CRUD, validation)
│   ├── test_users.py          # Users API tests (structure, email)
│   └── test_comments.py       # Comments API tests (relationships)
│
├── utils/                      # Utilities
│   ├── logger.py              # Logging configuration
│   └── helpers.py             # Assertion helpers and validators
│
├── config/                     # Configuration
│   └── settings.py            # Environment-based settings
│
├── .github/workflows/          # CI/CD
│   └── tests.yml              # GitHub Actions pipeline
│
├── conftest.py                 # pytest fixtures and hooks
├── pytest.ini                  # pytest configuration
├── requirements.txt            # Dependencies
└── .env                        # Environment variables
```

## Coding Standards & Conventions

### 1. Test Naming

**Pattern**: `test_<action>_<expected_outcome>`

```python
def test_get_all_posts_success(posts_api):           # ✅ Clear and descriptive
def test_get_non_existing_post(posts_api):           # ✅ Negative scenario
def test_posts():                                     # ❌ Too vague
```

### 2. Test Organization

**Group related tests in classes**:

```python
@allure.feature("Posts API")
@allure.story("Get all posts")
class TestGetAllPosts:
    def test_get_all_posts_success(self, posts_api):
        # Test implementation
```

**Markers for categorization**:
- `@pytest.mark.smoke` - Critical functionality
- `@pytest.mark.regression` - Full test suite
- `@pytest.mark.positive` - Happy path scenarios
- `@pytest.mark.negative` - Error handling

### 3. Allure Decorators (REQUIRED)

**Every test must have**:

```python
@allure.feature("Posts API")              # High-level feature
@allure.story("Create post")              # User story
@allure.severity(allure.severity_level.CRITICAL)  # Priority
```

**Use steps for readability**:

```python
def test_create_post(posts_api, test_post_data):
    with allure.step("Send POST request to /posts"):
        response = posts_api.create_post(test_post_data)

    with allure.step("Verify status code is 201"):
        assert_status_code(response, 201)
```

### 4. Assertions

**Use helper functions for consistent error messages**:

```python
# ✅ Good - descriptive error
assert_status_code(response, 200)
# Error: Expected status code 200, got 404. Response: {"error": "Not found"}

# ❌ Bad - generic error
assert response.status_code == 200
# Error: assert 404 == 200
```

### 5. Schema Validation

**Always validate response schemas**:

```python
with allure.step("Validate against Pydantic schema"):
    assert validate_schema(data, Post), "Post doesn't match schema"
```

### 6. Logging

**The BaseAPIClient logs automatically**:
- Request method, URL, body, params
- Response status, body (first 500 chars)
- All logs go to `logs/test.log` and console

**No need to add manual logging in tests**.

## Common Commands

### Environment Setup

```bash
# Activate virtual environment
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_posts.py

# Run specific test
pytest tests/test_posts.py::TestGetAllPosts::test_get_all_posts_success

# Run by marker
pytest -m smoke          # Only smoke tests
pytest -m posts          # Only posts tests
pytest -m negative       # Only negative scenarios

# Run with Allure
pytest --alluredir=allure-results
allure serve allure-results
```

### Development Workflow

```bash
# 1. Create new test file
touch tests/test_new_feature.py

# 2. Run tests to verify
pytest tests/test_new_feature.py -v

# 3. Generate Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

## Adding New Tests

### 1. Create Test File

Follow naming convention: `test_<feature>.py`

### 2. Import Required Modules

```python
import pytest
import allure
from models.schemas import YourModel
from utils.helpers import assert_status_code, validate_schema
```

### 3. Structure Tests

```python
@allure.feature("Feature Name")
@allure.story("Story Name")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
class TestClassName:
    def test_scenario_name(self, fixture_name):
        with allure.step("Step 1"):
            # Arrange
            data = {"key": "value"}

        with allure.step("Step 2"):
            # Act
            response = api_client.method(data)

        with allure.step("Step 3"):
            # Assert
            assert_status_code(response, 200)
            assert validate_schema(response.json(), Model)
```

### 4. Use Fixtures

```python
# Use existing fixtures from conftest.py
def test_example(posts_api, test_post_data, existing_post_id):
    response = posts_api.get_post_by_id(existing_post_id)
    # ...
```

## Creating New API Clients

### 1. Create Client Class

```python
# api/new_resource_api.py
from api.base_client import BaseAPIClient

class NewResourceAPI(BaseAPIClient):
    ENDPOINT = "/new-resource"

    def get_all(self) -> Response:
        return self.get(self.ENDPOINT)

    def get_by_id(self, resource_id: int) -> Response:
        return self.get(f"{self.ENDPOINT}/{resource_id}")
```

### 2. Add Pydantic Model

```python
# models/schemas.py
class NewResource(BaseModel):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1)
```

### 3. Add Fixture

```python
# conftest.py
@pytest.fixture(scope="session")
def new_resource_api():
    client = NewResourceAPI()
    yield client
    client.close()
```

## CI/CD Pipeline

### GitHub Actions Workflow

**Triggers**:
- Push to `main` or `master`
- Pull requests
- Manual dispatch (`workflow_dispatch`)

**Matrix Testing**:
- Python versions: 3.9, 3.10, 3.11, 3.12
- Runs all tests in parallel across versions

**Artifacts**:
- Test results (`allure-results/`)
- Logs (`logs/`)
- Allure reports (deployed to GitHub Pages)

**Viewing Results**:
1. Go to repository **Actions** tab
2. Click latest workflow run
3. View job logs and download artifacts
4. Access Allure report at: `https://username.github.io/api_test`

## Configuration

### Environment Variables (.env)

```env
BASE_URL=https://jsonplaceholder.typicode.com
API_TIMEOUT=30
LOG_LEVEL=INFO
```

**Never commit `.env` to Git**. Use `.env.example` as template.

### pytest Configuration (pytest.ini)

```ini
[pytest]
testpaths = tests              # Test discovery path
addopts = -v --alluredir=allure-results
markers =
    smoke: critical tests
    regression: full suite
    posts: posts endpoint tests
```

## Troubleshooting

### Tests Fail with "Connection Error"

**Check**:
1. Internet connection
2. API is accessible: `curl https://jsonplaceholder.typicode.com/posts`
3. Timeout settings in `.env`

### Allure Report Not Generated

**Check**:
1. Allure is installed: `allure --version`
2. Results directory exists: `allure-results/`
3. Run: `pytest --alluredir=allure-results --clean-alluredir`

### Import Errors

**Check**:
1. Virtual environment is activated
2. Dependencies installed: `pip install -r requirements.txt`
3. Python version >= 3.9

## Code Review Guidelines

When reviewing code changes:

1. **Test Coverage**: New features must have tests
2. **Allure Decorators**: All tests must have `@allure.feature`, `@allure.story`, `@allure.severity`
3. **Schema Validation**: Use Pydantic models, not manual assertions
4. **Naming**: Follow `test_<action>_<outcome>` convention
5. **Assertions**: Use helper functions from `utils/helpers.py`
6. **Documentation**: Update README.md and CLAUDE.md if adding new patterns
7. **CI/CD**: Tests must pass in GitHub Actions

## Philosophy & Best Practices

### Keep Tests Independent

Each test should:
- Set up its own data
- Clean up after itself
- Not depend on execution order

### Test One Thing

```python
# ✅ Good - tests one aspect
def test_post_title_not_empty(posts_api):
    response = posts_api.get_post_by_id(1)
    assert response.json()["title"]

# ❌ Bad - tests multiple things
def test_post(posts_api):
    response = posts_api.get_post_by_id(1)
    assert response.status_code == 200
    assert response.json()["title"]
    assert response.json()["userId"] > 0
    # ... (split into separate tests)
```

### Use Meaningful Assertions

```python
# ✅ Good - clear intent
assert user["email"], "User email should not be empty"

# ❌ Bad - unclear
assert user["email"]
```

### Parameterize Similar Tests

```python
@pytest.mark.parametrize("post_id", [1, 2, 3, 5, 10])
def test_get_different_posts(posts_api, post_id):
    response = posts_api.get_post_by_id(post_id)
    assert_status_code(response, 200)
```

## When in Doubt

1. **Look at existing tests** for patterns
2. **Check helper functions** in `utils/helpers.py`
3. **Validate schemas** with Pydantic models
4. **Use fixtures** instead of duplicating setup code
5. **Add Allure steps** for clarity in reports

---

**Last Updated**: 2026-01-19
**Project Version**: 1.0.0
