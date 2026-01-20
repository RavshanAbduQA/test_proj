"""Tests for Posts API endpoints."""
import pytest
import allure
from models.schemas import Post, PostCreate
from utils.helpers import (
    assert_status_code,
    assert_content_type,
    assert_field_exists,
    assert_field_type,
    assert_list_not_empty,
    validate_schema
)


@allure.feature("Posts API")
@allure.story("Get all posts")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.posts
class TestGetAllPosts:
    """Tests for GET /posts endpoint."""

    def test_get_all_posts_success(self, posts_api):
        """Test getting all posts returns 200 and valid data."""
        with allure.step("Send GET request to /posts"):
            response = posts_api.get_all_posts()

        with allure.step("Verify status code is 200"):
            assert_status_code(response, 200)

        with allure.step("Verify content type is application/json"):
            assert_content_type(response, "application/json")

        with allure.step("Verify response is a non-empty array"):
            data = response.json()
            assert isinstance(data, list), "Response should be an array"
            assert_list_not_empty(data)

        with allure.step("Verify first post has correct structure"):
            first_post = data[0]
            assert_field_exists(first_post, "userId")
            assert_field_exists(first_post, "id")
            assert_field_exists(first_post, "title")
            assert_field_exists(first_post, "body")

        with allure.step("Verify field types"):
            assert_field_type(first_post, "userId", int)
            assert_field_type(first_post, "id", int)
            assert_field_type(first_post, "title", str)
            assert_field_type(first_post, "body", str)

        with allure.step("Validate against Pydantic schema"):
            assert validate_schema(first_post, Post), "First post doesn't match Post schema"

        allure.attach(
            str(data[:2]),
            name="First 2 posts",
            attachment_type=allure.attachment_type.JSON
        )


@allure.feature("Posts API")
@allure.story("Get post by ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.posts
@pytest.mark.positive
class TestGetPostById:
    """Tests for GET /posts/{id} endpoint - positive scenarios."""

    def test_get_post_by_id_success(self, posts_api, existing_post_id):
        """Test getting post by ID returns 200 and valid data."""
        with allure.step(f"Send GET request to /posts/{existing_post_id}"):
            response = posts_api.get_post_by_id(existing_post_id)

        with allure.step("Verify status code is 200"):
            assert_status_code(response, 200)

        with allure.step("Verify content type is application/json"):
            assert_content_type(response, "application/json")

        with allure.step("Verify post ID matches requested ID"):
            data = response.json()
            assert data["id"] == existing_post_id, f"Expected ID {existing_post_id}, got {data['id']}"

        with allure.step("Verify all required fields exist"):
            assert_field_exists(data, "userId")
            assert_field_exists(data, "id")
            assert_field_exists(data, "title")
            assert_field_exists(data, "body")

        with allure.step("Verify field types are correct"):
            assert_field_type(data, "userId", int)
            assert_field_type(data, "id", int)
            assert_field_type(data, "title", str)
            assert_field_type(data, "body", str)

        with allure.step("Validate against Pydantic schema"):
            assert validate_schema(data, Post), "Post doesn't match Post schema"

        allure.attach(
            str(data),
            name=f"Post {existing_post_id}",
            attachment_type=allure.attachment_type.JSON
        )


@allure.feature("Posts API")
@allure.story("Get post by ID")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.posts
@pytest.mark.negative
class TestGetPostByIdNegative:
    """Tests for GET /posts/{id} endpoint - negative scenarios."""

    def test_get_non_existing_post(self, posts_api, non_existing_post_id):
        """Test getting non-existing post returns 404."""
        with allure.step(f"Send GET request to /posts/{non_existing_post_id}"):
            response = posts_api.get_post_by_id(non_existing_post_id)

        with allure.step("Verify status code is 404"):
            assert_status_code(response, 404)

        allure.attach(
            response.text,
            name="Response for non-existing post",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.feature("Posts API")
@allure.story("Create post")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.posts
@pytest.mark.positive
class TestCreatePost:
    """Tests for POST /posts endpoint."""

    def test_create_post_success(self, posts_api, test_post_data):
        """Test creating new post returns 201 and contains sent data."""
        with allure.step("Send POST request to /posts"):
            response = posts_api.create_post(test_post_data)

        with allure.step("Verify status code is 201"):
            assert_status_code(response, 201)

        with allure.step("Verify content type is application/json"):
            assert_content_type(response, "application/json")

        with allure.step("Verify created post contains sent data"):
            data = response.json()
            assert data["userId"] == test_post_data["userId"], "userId mismatch"
            assert data["title"] == test_post_data["title"], "title mismatch"
            assert data["body"] == test_post_data["body"], "body mismatch"

        with allure.step("Verify generated ID exists"):
            assert_field_exists(data, "id")
            assert isinstance(data["id"], int), "ID should be integer"
            assert data["id"] > 0, "ID should be positive"

        allure.attach(
            str(test_post_data),
            name="Request data",
            attachment_type=allure.attachment_type.JSON
        )
        allure.attach(
            str(data),
            name="Created post",
            attachment_type=allure.attachment_type.JSON
        )


@allure.feature("Posts API")
@allure.story("Update post")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.posts
class TestUpdatePost:
    """Tests for PUT /posts/{id} endpoint."""

    def test_update_post_success(self, posts_api, existing_post_id):
        """Test updating post returns 200 and updated data."""
        update_data = {
            "userId": 1,
            "id": existing_post_id,
            "title": "Updated Title",
            "body": "Updated body content"
        }

        with allure.step(f"Send PUT request to /posts/{existing_post_id}"):
            response = posts_api.update_post(existing_post_id, update_data)

        with allure.step("Verify status code is 200"):
            assert_status_code(response, 200)

        with allure.step("Verify content type is application/json"):
            assert_content_type(response, "application/json")

        with allure.step("Verify response contains updated data"):
            data = response.json()
            assert data["title"] == update_data["title"], "Title not updated"
            assert data["body"] == update_data["body"], "Body not updated"
            assert data["id"] == existing_post_id, "ID should remain unchanged"

        allure.attach(
            str(update_data),
            name="Update data",
            attachment_type=allure.attachment_type.JSON
        )
        allure.attach(
            str(data),
            name="Updated post",
            attachment_type=allure.attachment_type.JSON
        )


@allure.feature("Posts API")
@allure.story("Delete post")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.posts
class TestDeletePost:
    """Tests for DELETE /posts/{id} endpoint."""

    def test_delete_post_success(self, posts_api, existing_post_id):
        """Test deleting post returns 200 and empty object."""
        with allure.step(f"Send DELETE request to /posts/{existing_post_id}"):
            response = posts_api.delete_post(existing_post_id)

        with allure.step("Verify status code is 200"):
            assert_status_code(response, 200)

        with allure.step("Verify response is empty object"):
            data = response.json()
            assert data == {}, f"Expected empty object, got {data}"

        allure.attach(
            str(data),
            name="Delete response",
            attachment_type=allure.attachment_type.JSON
        )


@allure.feature("Posts API")
@allure.story("Parameterized tests")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.posts
class TestPostsParameterized:
    """Parameterized tests for posts."""

    @pytest.mark.parametrize("post_id", [1, 2, 3, 5, 10])
    def test_get_different_posts(self, posts_api, post_id):
        """Test getting different posts by ID."""
        with allure.step(f"Get post with ID {post_id}"):
            response = posts_api.get_post_by_id(post_id)

        with allure.step("Verify response is successful"):
            assert_status_code(response, 200)
            data = response.json()
            assert data["id"] == post_id, f"Expected ID {post_id}, got {data['id']}"

        with allure.step("Validate schema"):
            assert validate_schema(data, Post), f"Post {post_id} doesn't match schema"

    @pytest.mark.parametrize("user_id", [1, 2, 3])
    def test_get_posts_by_user(self, posts_api, user_id):
        """Test getting posts filtered by user ID."""
        with allure.step(f"Get posts for user {user_id}"):
            response = posts_api.get_posts_by_user_id(user_id)

        with allure.step("Verify response is successful"):
            assert_status_code(response, 200)
            data = response.json()
            assert_list_not_empty(data)

        with allure.step("Verify all posts belong to the user"):
            for post in data:
                assert post["userId"] == user_id, \
                    f"Post {post['id']} has userId {post['userId']}, expected {user_id}"
