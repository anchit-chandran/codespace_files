import json
import time
import random
import string
import webbrowser
import threading
from pathlib import Path
from typing import Optional, Dict, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from rich.console import Console
from . import constants

console = Console()


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.auth_manager = kwargs.pop("auth_manager")
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path.startswith("/callback"):
            query = parse_qs(urlparse(self.path).query)

            # Verify state
            if query.get("state", [""])[0] != self.auth_manager.state:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"Invalid state parameter")
                return

            # Get tokens from query parameters
            access_token = query.get("access_token", [""])[0]
            refresh_token = query.get("refresh_token", [""])[0]
            expires_in = int(query.get("expires_in", ["3600"])[0])

            if access_token:
                # Store tokens
                self.auth_manager._save_config(
                    {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "expires_at": time.time() + expires_in,
                    }
                )

                # Send success response
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(
                    b"Authentication successful! You can close this window."
                )

                # Stop the server
                threading.Thread(target=self.server.shutdown).start()
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"Authentication failed")

    def log_message(self, format, *args):
        # Suppress HTTP server logs
        pass


class AuthManager:
    def __init__(self):
        self.config_dir = Path.home() / ".medicode"
        self.config_file = self.config_dir / "config.json"
        self.state = None
        self._ensure_config_dir()
        self._load_config()

    def _ensure_config_dir(self):
        """Ensure the config directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _load_config(self) -> Dict[str, Any]:
        """Load the configuration from the config file."""
        if not self.config_file.exists():
            return {}
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _save_config(self, config: Dict[str, Any]):
        """Save the configuration to the config file."""
        with open(self.config_file, "w") as f:
            json.dump(config, f)

    def _generate_state(self) -> str:
        """Generate a random state parameter for OAuth."""
        return "".join(random.choices(string.ascii_letters + string.digits, k=32))

    def login(self):
        """Handle the login process using OAuth."""
        # Generate state parameter
        self.state = self._generate_state()

        # Start local server to handle callback
        def run_server():
            server = HTTPServer(
                ("localhost", constants.OAUTH_CALLBACK_PORT),
                lambda *args, **kwargs: OAuthCallbackHandler(
                    *args, auth_manager=self, **kwargs
                ),
            )
            server.serve_forever()

        server_thread = threading.Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()

        # Construct authorization URL
        auth_url = f"{constants.OAUTH_AUTHORIZE_URL}?client_id={constants.OAUTH_CLIENT_ID}&redirect_uri={constants.OAUTH_CALLBACK_URL}&state={self.state}"

        # Open browser for authentication
        console.print("[yellow]Opening browser for authentication...[/yellow]")
        webbrowser.open(auth_url)

        # Wait for server to complete
        server_thread.join()
        console.print("[green]Successfully logged in![/green]")

    def get_token(self) -> Optional[str]:
        """Get the current access token, refreshing if necessary."""
        config = self._load_config()
        if not config:
            return None

        current_time = time.time()
        if current_time >= config.get("expires_at", 0):
            # Token expired, need to re-authenticate
            console.print(
                "[yellow]Session expired. Please run 'medicode login' again.[/yellow]"
            )
            return None

        return config.get("access_token")

    def logout(self):
        """Handle the logout process."""
        self._save_config({})
        console.print("[green]Successfully logged out![/green]")

    def is_authenticated(self) -> bool:
        """Check if the user is currently authenticated."""
        return self.get_token() is not None
