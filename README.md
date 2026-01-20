# JSONPlaceholder API Test Automation

![Tests](https://github.com/your-username/api_test/workflows/API%20Tests/badge.svg)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Automated API testing framework for [JSONPlaceholder](https://jsonplaceholder.typicode.com/) REST API using Python, pytest, and Allure reporting.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Test Structure](#test-structure)
- [CI/CD](#cicd)
- [Allure Reports](#allure-reports)
- [Project Structure](#project-structure)

## 🎯 Project Overview

This project provides comprehensive test coverage for the JSONPlaceholder API, including:
- **Posts API**: CRUD operations, filtering, and validation
- **Users API**: User data retrieval and validation
- **Comments API**: Comments retrieval, email validation, and relationship testing

## ✨ Features

- **Complete API Coverage**: Tests for all major endpoints (Posts, Users, Comments)
- **Schema Validation**: Pydantic models for robust data validation
- **Page Object Pattern**: Clean, maintainable API client architecture
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Allure Reports**: Rich, interactive test reports
- **CI/CD Integration**: GitHub Actions workflow with matrix testing
- **Parameterized Tests**: Data-driven testing approach
- **Positive & Negative Testing**: Both happy path and error scenarios

## 🏗️ Architecture

The project follows a layered architecture:

```
┌─────────────────────────────────────┐
│         Test Layer                  │
│  (test_posts, test_users, etc.)    │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│         API Layer                   │
│  (PostsAPI, UsersAPI, CommentsAPI)  │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│      Base Client Layer              │
│     (BaseAPIClient)                 │
└──────────────┬──────────────────────┘
               │
┌──────────────┴──────────────────────┐
│      HTTP Layer (requests)          │
└─────────────────────────────────────┘
```

**Design Patterns Used:**
- **Page Object Pattern**: Each API endpoint has its own class
- **Facade Pattern**: BaseAPIClient provides unified interface
- **Fixture Pattern**: pytest fixtures for test setup/teardown
- **Data Validation**: Pydantic models for schema validation

## 📦 Requirements

- Python 3.9 or higher
- pip (Python package manager)
- Git (for CI/CD)

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/api_test.git
cd api_test
```

### 2. Create and activate virtual environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify installation

```bash
pytest --version
```

## 🧪 Running Tests

### Run all tests

```bash
pytest
```

### Run tests with verbose output

```bash
pytest -v
```

### Run specific test file

```bash
pytest tests/test_posts.py
```

### Run specific test

```bash
pytest tests/test_posts.py::TestGetAllPosts::test_get_all_posts_success
```

### Run tests by marker

```bash
# Run only smoke tests
pytest -m smoke

# Run only positive tests
pytest -m positive

# Run posts tests
pytest -m posts
```

### Run tests with Allure report generation

```bash
pytest --alluredir=allure-results
```

### Run tests in parallel (requires pytest-xdist)

```bash
pip install pytest-xdist
pytest -n auto
```

## 📊 Allure Reports

### Generate and view Allure report

1. Run tests with Allure results:
```bash
pytest --alluredir=allure-results
```

2. Generate and open report:
```bash
allure serve allure-results
```

### Allure Report Features

- Test execution timeline
- Test categorization by features and stories
- Severity levels
- Detailed test steps
- Request/Response attachments
- Failure screenshots and logs
- Historical trends

### Example Allure Report

![Allure Report Example](docs/allure-example.png)

## 📁 Project Structure

```
api_test/
├── .github/
│   └── workflows/
│       └── tests.yml          # GitHub Actions CI/CD workflow
├── api/
│   ├── __init__.py
│   ├── base_client.py         # Base API client with HTTP methods
│   ├── posts_api.py           # Posts endpoint API client
│   ├── users_api.py           # Users endpoint API client
│   └── comments_api.py        # Comments endpoint API client
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuration management
├── models/
│   ├── __init__.py
│   └── schemas.py             # Pydantic models for validation
├── tests/
│   ├── __init__.py
│   ├── test_posts.py          # Posts API tests
│   ├── test_users.py          # Users API tests
│   └── test_comments.py       # Comments API tests
├── utils/
│   ├── __init__.py
│   ├── logger.py              # Logging configuration
│   └── helpers.py             # Helper functions and assertions
├── data/                      # Test data directory
├── logs/                      # Test execution logs
├── allure-results/            # Allure test results
├── .env                       # Environment variables
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── conftest.py                # Pytest fixtures and configuration
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
├── CLAUDE.md                  # Claude Code guidance
└── README.md                  # This file
```

## 🧪 Test Structure

### Test Organization

Tests are organized by feature:
- **test_posts.py**: 15+ tests for Posts API
- **test_users.py**: 10+ tests for Users API
- **test_comments.py**: 10+ tests for Comments API

### Test Categories

- **Smoke Tests** (`@pytest.mark.smoke`): Critical functionality
- **Regression Tests** (`@pytest.mark.regression`): Full test suite
- **Positive Tests** (`@pytest.mark.positive`): Happy path scenarios
- **Negative Tests** (`@pytest.mark.negative`): Error handling

### Example Test

```python
@allure.feature("Posts API")
@allure.story("Get all posts")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_get_all_posts_success(posts_api):
    with allure.step("Send GET request to /posts"):
        response = posts_api.get_all_posts()

    with allure.step("Verify status code is 200"):
        assert_status_code(response, 200)

    with allure.step("Verify response is non-empty array"):
        data = response.json()
        assert len(data) > 0
```

## 🔄 CI/CD

### GitHub Actions Workflow

The project includes a comprehensive CI/CD pipeline that:

1. **Triggers**:
   - Push to main/master branch
   - Pull requests
   - Manual workflow dispatch

2. **Matrix Testing**:
   - Python versions: 3.9, 3.10, 3.11, 3.12
   - Parallel execution

3. **Pipeline Steps**:
   - Checkout code
   - Set up Python environment
   - Cache dependencies
   - Install dependencies
   - Run tests
   - Generate Allure report
   - Deploy report to GitHub Pages
   - Upload artifacts

4. **Artifacts**:
   - Test results
   - Allure reports
   - Logs

### Viewing CI/CD Results

1. Go to the **Actions** tab in your repository
2. Click on the latest workflow run
3. View test results and download artifacts
4. Access Allure report at: `https://your-username.github.io/api_test`

## 📝 Configuration

### Environment Variables

Edit `.env` file to configure:

```env
BASE_URL=https://jsonplaceholder.typicode.com
API_TIMEOUT=30
LOG_LEVEL=INFO
```

### Pytest Configuration

Edit `pytest.ini` to customize:
- Test discovery patterns
- Logging settings
- Markers
- Allure settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure they pass
5. Submit a pull request

## 📄 License

This project is created as a test assignment for educational purposes.

## 📧 Contact

For questions or issues, please contact: [your-email@example.com]

---

**Test Status**: ![Tests](https://github.com/your-username/api_test/workflows/API%20Tests/badge.svg)

**Last Updated**: 2026-01-19
