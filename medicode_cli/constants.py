import os

# Check if we're running in a dev container
IS_DEV_CONTAINER = os.environ.get('CODESPACES') == 'true'

# Use host.docker.internal to reach the host machine from inside the dev container
DEVCONTAINER_HOST = "host.docker.internal"
LOCAL_HOST = "localhost"
DEVCONTAINER_PORT = 3000

BASE_URL = f"http://{DEVCONTAINER_HOST}:{DEVCONTAINER_PORT}/api/medicode-cli"
PYTHON_VALIDATE_CODE_ENDPOINT = "validate"

# OAuth configuration
OAUTH_CLIENT_ID = "medicode-cli"
OAUTH_AUTHORIZE_URL = f"http://{LOCAL_HOST}:{DEVCONTAINER_PORT}/api/auth/cli/authorize"
OAUTH_CALLBACK_PORT = 3001
OAUTH_CALLBACK_URL = f"http://{LOCAL_HOST}:{OAUTH_CALLBACK_PORT}/callback"