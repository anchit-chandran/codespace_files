import requests
import os
import sys
import json
from typing import Optional
from .auth import AuthManager
from rich.console import Console

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .constants import BASE_URL, PYTHON_VALIDATE_CODE_ENDPOINT

console = Console()


class MedicodeAPI:
    def __init__(self):
        self.base_url = BASE_URL
        self.auth_manager = AuthManager()

    def _get_headers(self) -> dict:
        """Get headers with authentication token and session cookies."""
        token = self.auth_manager.get_token()
        headers = {"Content-Type": "application/json"}

        # Get the config which contains the session info
        config = self.auth_manager._load_config()
        if config:
            # Add the session cookies that Supabase expects
            headers["Cookie"] = (
                f"sb-access-token={config.get('access_token')}; sb-refresh-token={config.get('refresh_token')}"
            )
            # Also keep the Bearer token for backward compatibility
            headers["Authorization"] = f"Bearer {token}"

        console.print(f"[yellow]Headers: {headers}[/yellow]")
        return headers

    def validate_code(self, code: str, tutorial_id: str, lesson_id: str) -> dict:
        """Validate code using the medicode API.

        Args:
            code (str): The code to validate
            tutorial_id (str): The tutorial ID
            lesson_id (str): The lesson ID

        Returns:
            dict: The API response
        """
        if not self.auth_manager.is_authenticated():
            raise Exception("Not authenticated. Please run 'medicode login' first.")

        # Gather the data
        data = {
            "student_code": code,
            "tutorialId": tutorial_id,
            "lessonId": lesson_id,
        }
        url = f"{self.base_url}/{PYTHON_VALIDATE_CODE_ENDPOINT}"
        headers = self._get_headers()

        console.print(f"[yellow]Making request to: {url}[/yellow]")
        console.print(f"[yellow]With data: {data}[/yellow]")

        try:
            response = requests.post(url, json=data, headers=headers, timeout=5)
            console.print(f"[yellow]Response status: {response.status_code}[/yellow]")
            console.print(f"[yellow]Response headers: {response.headers}[/yellow]")
            console.print(f"[yellow]Response body: {response.text}[/yellow]")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. The server might not be running or accessible.")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise Exception("Authentication failed. Please run 'medicode login' again.")
            raise e
