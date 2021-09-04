AUTH_METHOD = "PASSWORD"

AUTH_METHODS = [ "PASSWORD" ]

CREDENTIALS_FILE = "configs/credentials.ini"
DEFAULT_CREDENTIALS_FILE = CREDENTIALS_FILE

MODULES = [
    "jobs",
    "systems",
    "files",
    "apps"
]

PASSWORD = "PASSWORD"
DEFAULT_AUTH_METHOD = PASSWORD

ENV = "develop"
TENANT = "tacc"
BASE_URL = f"https://{TENANT}.{ENV}.tapis.io"