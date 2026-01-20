"""Tests for Comments API endpoints."""
import pytest
import allure
from models.schemas import Comment
from utils.helpers import (
    assert_status_code,
    assert_content_type,
    assert_field_exists,
    assert_field_type,
    assert_list_not_empty,
    validate_email,
    validate_schema
)


@allure.feature("Comments API")
@allure.story("Get post comments")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.comments
class TestGetPostComments:
    """Tests for GET /posts/{id}/comments endpoint."""

    def test_get_post_comments_success(self, posts_api, existing_post_id):
        """Test getting comments for a post returns 200 and valid data."""
        with allure.step(f"Send GET request to /posts/{existing_post_id}/comments"):
            response = posts_api.get_post_comments(existing_post_id)

        with allure.step("Verify status code is 200"):
            assert_status_code(response, 200)

        with allure.step("Verify content type is application/json"):
            assert_content_type(response, "application/json")

        with allure.step("Verify response is a non-empty array"):
            data = response.json()
            assert isinstance(data, list), "Response should be an array"
            assert_list_not_empty(data)

        with allure.step(f"Verify all comments belong to postId {existing_post_id}"):
            for comment in data:
                assert comment["postId"] == existing_post_id, \
                    f"Comment {comment['id']} has postId {comment['postId']}, expected {existing_post_id}"

        with allure.step("Verify first comment structure"):
            first_comment = data[0]
            required_fields = ["postId", "id", "name", "email", "body"]
            for field in required_fields:
                assert_field_exists(first_comment, field)

        with allure.step("Verify field types"):
            assert_field_type(first_comment, "postId", int)
            assert_field_type(first_comment, "id", int)
            assert_field_type(first_comment, "name", str)
            assert_field_type(first_comment, "email", str)
            assert_field_type(first_comment, "body", str)

        with allure.step("Validate against Pydantic schema"):
            assert validate_schema(first_comment, Comment), \
                "First comment doesn't match Comment schema"

        allure.attach(
            str(data[0]),
            name="First comment",
            attachment_type=allure.attachment_type.JSON
        )


@allure.feature("Comments API")
@allure.story("Get comments by query")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.comments
class TestGetCommentsByPostId:
    """Tests for GET /comments?postId={id} endpoint."""

    def test_get_comments_by_post_id_success(self, comments_api, existing_post_id):
        """Test getting comments filtered by postId."""
        with allure.step(f"Send GET request to /comments?postId={existing_post_id}"):
            response = comments_api.get_comments_by_post_id(existing_post_id)

        with allure.step("Verify status code is 200"):
            assert_status_code(response, 200)

        with allure.step("Verify response is a non-empty array"):
            data = response.json()
            assert isinstance(data, list), "Response should be an array"
            assert_list_not_empty(data)

        with allure.step(f"Verify all comments belong to postId {existing_post_id}"):
            for comment in data:
                assert comment["postId"] == existing_post_id, \
                    f"Comment {comment['id']} has postId {comment['postId']}, expected {existing_post_id}"

        allure.attach(
            f"Found {len(data)} comments for post {existing_post_id}",
            name="Comments count",
            attachment_type=allure.attachment_type.TEXT
        )


@allure.feature("Comments API")
@allure.story("Email validation in comments")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.comments
class TestCommentsEmailValidation:
    """Tests for email validation in comments."""

    def test_all_comments_have_valid_emails(self, comments_api, existing_post_id):
        """Test that all comments have valid email addresses."""
        with allure.step(f"Get comments for post {existing_post_id}"):
            response = comments_api.get_comments_by_post_id(existing_post_id)
            assert_status_code(response, 200)
            comments = response.json()

        with allure.step("Validate email format for each comment"):
            invalid_emails = []
            for comment in comments:
                email = comment.get("email", "")
                if not validate_email(email):
                    invalid_emails.append(f"Comment {comment['id']}: {email}")

            assert len(invalid_emails) == 0, \
                f"Found {len(invalid_emails)} invalid emails: {invalid_emails}"

        allure.attach(
            "\n".join([f"{c['id']}: {c['email']}" for c in comments]),
            name="All comment emails",
            attachment_type=allure.attachment_type.TEXT
        )

    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_comments_emails_contain_at_symbol(self, posts_api, post_id):
        """Test that all comment emails contain @ symbol."""
        with allure.step(f"Get comments for post {post_id}"):
            response = posts_api.get_post_comments(post_id)
            assert_status_code(response, 200)
            comments = response.json()

        with allure.step("Verify all emails contain @ symbol"):
            for comment in comments:
                email = comment["email"]
                assert "@" in email, \
                    f"Comment {comment['id']} email missing @ symbol: {email}"
                assert "." in email.split("@")[1], \
                    f"Comment {comment['id']} email missing domain extension: {email}"


@allure.feature("Comments API")
@allure.story("Comments and posts relationship")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.comments
class TestCommentsPostsRelationship:
    """Tests for relationship between comments and posts."""

    def test_comments_belong_to_existing_post(self, comments_api, posts_api, existing_post_id):
        """Test that comments are properly linked to their posts."""
        with allure.step(f"Verify post {existing_post_id} exists"):
            post_response = posts_api.get_post_by_id(existing_post_id)
            assert_status_code(post_response, 200)
            post = post_response.json()

        with allure.step("Get comments for the post"):
            comments_response = comments_api.get_comments_by_post_id(existing_post_id)
            assert_status_code(comments_response, 200)
            comments = comments_response.json()

        with allure.step("Verify all comments reference the correct post"):
            for comment in comments:
                assert comment["postId"] == post["id"], \
                    f"Comment {comment['id']} postId mismatch"

        allure.attach(
            f"Post {post['id']} has {len(comments)} comments",
            name="Post-Comments relationship",
            attachment_type=allure.attachment_type.TEXT
        )

    @pytest.mark.parametrize("post_id", [1, 2, 3, 5])
    def test_multiple_posts_have_comments(self, posts_api, post_id):
        """Test that multiple posts have associated comments."""
        with allure.step(f"Get comments for post {post_id}"):
            response = posts_api.get_post_comments(post_id)
            assert_status_code(response, 200)
            comments = response.json()

        with allure.step("Verify post has comments"):
            assert_list_not_empty(comments)

        with allure.step("Verify all comments belong to the post"):
            for comment in comments:
                assert comment["postId"] == post_id


@allure.feature("Comments API")
@allure.story("Comment structure validation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
@pytest.mark.comments
class TestCommentStructure:
    """Tests for comment data structure validation."""

    def test_comment_required_fields(self, comments_api):
        """Test that comments have all required fields."""
        with allure.step("Get a comment"):
            response = comments_api.get_comment_by_id(1)
            assert_status_code(response, 200)
            comment = response.json()

        with allure.step("Verify all required fields exist"):
            required_fields = ["postId", "id", "name", "email", "body"]
            for field in required_fields:
                assert_field_exists(comment, field)
                assert comment[field], f"Field '{field}' should not be empty"

        with allure.step("Validate against Pydantic schema"):
            assert validate_schema(comment, Comment), "Comment doesn't match Comment schema"

        allure.attach(
            str(comment),
            name="Comment structure",
            attachment_type=allure.attachment_type.JSON
        )

    @pytest.mark.parametrize("comment_id", [1, 5, 10, 50, 100])
    def test_different_comments_structure(self, comments_api, comment_id):
        """Test that different comments have consistent structure."""
        with allure.step(f"Get comment {comment_id}"):
            response = comments_api.get_comment_by_id(comment_id)
            assert_status_code(response, 200)
            comment = response.json()

        with allure.step("Verify comment ID matches"):
            assert comment["id"] == comment_id

        with allure.step("Validate schema"):
            assert validate_schema(comment, Comment), \
                f"Comment {comment_id} doesn't match Comment schema"

    def test_comment_body_not_empty(self, comments_api, existing_post_id):
        """Test that comment bodies are not empty."""
        with allure.step("Get comments"):
            response = comments_api.get_comments_by_post_id(existing_post_id)
            assert_status_code(response, 200)
            comments = response.json()

        with allure.step("Verify all comment bodies are not empty"):
            for comment in comments:
                assert comment["body"].strip(), \
                    f"Comment {comment['id']} has empty body"
                assert len(comment["body"]) > 0, \
                    f"Comment {comment['id']} body has zero length"
