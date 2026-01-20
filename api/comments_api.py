"""Comments API endpoints."""
from typing import Dict, List, Optional
from requests import Response
from api.base_client import BaseAPIClient


class CommentsAPI(BaseAPIClient):
    """API client for Comments endpoints."""

    ENDPOINT = "/comments"

    def get_all_comments(self) -> Response:
        """Get all comments.

        Returns:
            Response with list of comments
        """
        return self.get(self.ENDPOINT)

    def get_comment_by_id(self, comment_id: int) -> Response:
        """Get comment by ID.

        Args:
            comment_id: Comment ID

        Returns:
            Response with comment data
        """
        return self.get(f"{self.ENDPOINT}/{comment_id}")

    def get_comments_by_post_id(self, post_id: int) -> Response:
        """Get all comments for a post.

        Args:
            post_id: Post ID

        Returns:
            Response with list of comments
        """
        return self.get(self.ENDPOINT, params={"postId": post_id})

    def create_comment(self, comment_data: Dict) -> Response:
        """Create new comment.

        Args:
            comment_data: Comment data (postId, name, email, body)

        Returns:
            Response with created comment
        """
        return self.post(self.ENDPOINT, json=comment_data)

    def update_comment(self, comment_id: int, comment_data: Dict) -> Response:
        """Update comment by ID.

        Args:
            comment_id: Comment ID
            comment_data: Updated comment data

        Returns:
            Response with updated comment
        """
        return self.put(f"{self.ENDPOINT}/{comment_id}", json=comment_data)

    def delete_comment(self, comment_id: int) -> Response:
        """Delete comment by ID.

        Args:
            comment_id: Comment ID

        Returns:
            Response (empty object)
        """
        return self.delete(f"{self.ENDPOINT}/{comment_id}")
