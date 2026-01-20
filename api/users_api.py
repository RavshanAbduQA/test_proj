"""Users API endpoints."""
from typing import Dict, List
from requests import Response
from api.base_client import BaseAPIClient


class UsersAPI(BaseAPIClient):
    """API client for Users endpoints."""

    ENDPOINT = "/users"

    def get_all_users(self) -> Response:
        """Get all users.

        Returns:
            Response with list of users
        """
        return self.get(self.ENDPOINT)

    def get_user_by_id(self, user_id: int) -> Response:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            Response with user data
        """
        return self.get(f"{self.ENDPOINT}/{user_id}")

    def get_user_posts(self, user_id: int) -> Response:
        """Get all posts by user.

        Args:
            user_id: User ID

        Returns:
            Response with list of posts
        """
        return self.get(f"{self.ENDPOINT}/{user_id}/posts")

    def get_user_albums(self, user_id: int) -> Response:
        """Get all albums by user.

        Args:
            user_id: User ID

        Returns:
            Response with list of albums
        """
        return self.get(f"{self.ENDPOINT}/{user_id}/albums")

    def get_user_todos(self, user_id: int) -> Response:
        """Get all todos by user.

        Args:
            user_id: User ID

        Returns:
            Response with list of todos
        """
        return self.get(f"{self.ENDPOINT}/{user_id}/todos")
