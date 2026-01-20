"""Base API client for making HTTP requests."""
import logging
from typing import Dict, Optional, Any
import requests
from requests import Response
from config.settings import settings

logger = logging.getLogger(__name__)


class BaseAPIClient:
    """Base API client with common HTTP methods."""

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        """Initialize API client.

        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
        """
        self.base_url = base_url or settings.BASE_URL
        self.timeout = timeout or settings.API_TIMEOUT
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint.

        Args:
            endpoint: API endpoint path

        Returns:
            Full URL
        """
        return f"{self.base_url}{endpoint}"

    def _log_request(self, method: str, url: str, **kwargs):
        """Log request details.

        Args:
            method: HTTP method
            url: Request URL
            **kwargs: Additional request parameters
        """
        logger.info(f"Request: {method} {url}")
        if 'json' in kwargs:
            logger.debug(f"Request body: {kwargs['json']}")
        if 'params' in kwargs:
            logger.debug(f"Request params: {kwargs['params']}")

    def _log_response(self, response: Response):
        """Log response details.

        Args:
            response: Response object
        """
        logger.info(f"Response: {response.status_code} {response.reason}")
        logger.debug(f"Response body: {response.text[:500]}")

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Response:
        """Send GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters
            **kwargs: Additional request parameters

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        self._log_request('GET', url, params=params, **kwargs)

        response = self.session.get(
            url,
            params=params,
            timeout=self.timeout,
            **kwargs
        )

        self._log_response(response)
        return response

    def post(self, endpoint: str, json: Optional[Dict] = None, **kwargs) -> Response:
        """Send POST request.

        Args:
            endpoint: API endpoint
            json: JSON data
            **kwargs: Additional request parameters

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        self._log_request('POST', url, json=json, **kwargs)

        response = self.session.post(
            url,
            json=json,
            timeout=self.timeout,
            **kwargs
        )

        self._log_response(response)
        return response

    def put(self, endpoint: str, json: Optional[Dict] = None, **kwargs) -> Response:
        """Send PUT request.

        Args:
            endpoint: API endpoint
            json: JSON data
            **kwargs: Additional request parameters

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        self._log_request('PUT', url, json=json, **kwargs)

        response = self.session.put(
            url,
            json=json,
            timeout=self.timeout,
            **kwargs
        )

        self._log_response(response)
        return response

    def patch(self, endpoint: str, json: Optional[Dict] = None, **kwargs) -> Response:
        """Send PATCH request.

        Args:
            endpoint: API endpoint
            json: JSON data
            **kwargs: Additional request parameters

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        self._log_request('PATCH', url, json=json, **kwargs)

        response = self.session.patch(
            url,
            json=json,
            timeout=self.timeout,
            **kwargs
        )

        self._log_response(response)
        return response

    def delete(self, endpoint: str, **kwargs) -> Response:
        """Send DELETE request.

        Args:
            endpoint: API endpoint
            **kwargs: Additional request parameters

        Returns:
            Response object
        """
        url = self._build_url(endpoint)
        self._log_request('DELETE', url, **kwargs)

        response = self.session.delete(
            url,
            timeout=self.timeout,
            **kwargs
        )

        self._log_response(response)
        return response

    def close(self):
        """Close session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
