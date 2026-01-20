"""Posts API endpoints."""
from typing import Dict, List, Optional
from requests import Response
from api.base_client import BaseAPIClient
from models.schemas import Post, PostCreate, PostUpdate, Comment


class PostsAPI(BaseAPIClient):
    """API client for Posts endpoints."""

    ENDPOINT = "/posts"

    def get_all_posts(self) -> Response:
        """Get all posts.

        Returns:
            Response with list of posts
        """
        return self.get(self.ENDPOINT)

    def get_post_by_id(self, post_id: int) -> Response:
        """Get post by ID.

        Args:
            post_id: Post ID

        Returns:
            Response with post data
        """
        return self.get(f"{self.ENDPOINT}/{post_id}")

    def create_post(self, post_data: Dict) -> Response:
        """Create new post.

        Args:
            post_data: Post data (userId, title, body)

        Returns:
            Response with created post
        """
        return self.post(self.ENDPOINT, json=post_data)

    def update_post(self, post_id: int, post_data: Dict) -> Response:
        """Update post by ID (full update).

        Args:
            post_id: Post ID
            post_data: Updated post data

        Returns:
            Response with updated post
        """
        return self.put(f"{self.ENDPOINT}/{post_id}", json=post_data)

    def partial_update_post(self, post_id: int, post_data: Dict) -> Response:
        """Partially update post by ID.

        Args:
            post_id: Post ID
            post_data: Partial post data

        Returns:
            Response with updated post
        """
        return self.patch(f"{self.ENDPOINT}/{post_id}", json=post_data)

    def delete_post(self, post_id: int) -> Response:
        """Delete post by ID.

        Args:
            post_id: Post ID

        Returns:
            Response (empty object)
        """
        return self.delete(f"{self.ENDPOINT}/{post_id}")

    def get_post_comments(self, post_id: int) -> Response:
        """Get all comments for a post.

        Args:
            post_id: Post ID

        Returns:
            Response with list of comments
        """
        return self.get(f"{self.ENDPOINT}/{post_id}/comments")

    def get_posts_by_user_id(self, user_id: int) -> Response:
        """Get all posts by user ID.

        Args:
            user_id: User ID

        Returns:
            Response with list of posts
        """
        return self.get(self.ENDPOINT, params={"userId": user_id})
