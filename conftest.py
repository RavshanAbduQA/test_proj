"""Pytest configuration and fixtures."""
import pytest
import logging
from api.posts_api import PostsAPI
from api.users_api import UsersAPI
from api.comments_api import CommentsAPI
from utils.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)


@pytest.fixture(scope="session")
def posts_api():
    """Fixture for Posts API client.

    Yields:
        PostsAPI: Posts API client instance
    """
    logger.info("Creating PostsAPI client")
    client = PostsAPI()
    yield client
    client.close()
    logger.info("PostsAPI client closed")


@pytest.fixture(scope="session")
def users_api():
    """Fixture for Users API client.

    Yields:
        UsersAPI: Users API client instance
    """
    logger.info("Creating UsersAPI client")
    client = UsersAPI()
    yield client
    client.close()
    logger.info("UsersAPI client closed")


@pytest.fixture(scope="session")
def comments_api():
    """Fixture for Comments API client.

    Yields:
        CommentsAPI: Comments API client instance
    """
    logger.info("Creating CommentsAPI client")
    client = CommentsAPI()
    yield client
    client.close()
    logger.info("CommentsAPI client closed")


@pytest.fixture(scope="function")
def test_post_data():
    """Fixture for test post data.

    Returns:
        dict: Test post data
    """
    return {
        "userId": 1,
        "title": "Test Post Title",
        "body": "Test post body content"
    }


@pytest.fixture(scope="function")
def test_comment_data():
    """Fixture for test comment data.

    Returns:
        dict: Test comment data
    """
    return {
        "postId": 1,
        "name": "Test Comment",
        "email": "test@example.com",
        "body": "Test comment body"
    }


@pytest.fixture(scope="function")
def existing_post_id():
    """Fixture for existing post ID.

    Returns:
        int: Post ID
    """
    return 1


@pytest.fixture(scope="function")
def existing_user_id():
    """Fixture for existing user ID.

    Returns:
        int: User ID
    """
    return 1


@pytest.fixture(scope="function")
def non_existing_post_id():
    """Fixture for non-existing post ID.

    Returns:
        int: Invalid post ID
    """
    return 99999


def pytest_configure(config):
    """Pytest configuration hook."""
    logger.info("=" * 80)
    logger.info("Starting test session")
    logger.info("=" * 80)


def pytest_sessionfinish(session, exitstatus):
    """Pytest session finish hook."""
    logger.info("=" * 80)
    logger.info(f"Test session finished with status: {exitstatus}")
    logger.info("=" * 80)
