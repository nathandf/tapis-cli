APP_REGISTRY = [
    "core",
    "tapis"
]

AUTH_METHOD = "PASSWORD"

AUTH_METHODS = [ "PASSWORD" ]

CONFIG_FILE = "configs/configs.ini"
DEFAULT_CONFIG_FILE = CONFIG_FILE

PASSWORD = "PASSWORD"
DEFAULT_AUTH_METHOD = PASSWORD

ENVS = [ "develop", "staging", "prod" ]

ENV = "prod"
TENANT = "tacc"

ENV = ENV + "." if (ENV != "prod") else ""

BASE_URL = f"https://{TENANT}.{ENV}tapis.io"