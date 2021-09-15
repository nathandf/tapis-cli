from tapipy.tapis import Tapis
from utils.Logger import Logger
from typing import Union
import sys
from configs import settings
from core.Configuration import Configuration

class Authenticator:
    base_url = ""
    auth_methods = settings.AUTH_METHODS

    def __init__(self, base_url=settings.BASE_URL):
        self.base_url = base_url
        self.logger = Logger()
        self.config = Configuration()

    def authenticate(self,
        auth_method: str = settings.DEFAULT_AUTH_METHOD
    ) -> Union[Tapis, None]:

        # If there are no credentials in the credentials dict, throw error
        if not bool(self.config.credentials):
            # Add the credentials from the config 
            # file to this Configuration object's credentials dict
            self.logger.error("Tapis CLI not configured. Run the following command to add your credentials:")
            self.logger.log("`tapis auth configure`")
            sys.exit(1)

        # Authenticate using the provided auth method. Raise exception
        # if provided credentials do not meet requirements
        if auth_method == settings.PASSWORD:
            self.validate_credentials(auth_method, self.config.credentials)
            try:
                client = Tapis(
                    base_url=self.base_url,
                    username=self.config.credentials["username"],
                    password=self.config.credentials["password"]
                )
                client.get_tokens()

                return client
            except:
                e = sys.exc_info[0]
                self.logger.log(e.message)
        else:
            raise ValueError(f"Invlaid auth_method: {auth_method}. Valid auth_method: {settings.AUTH_METHODS}")

    def validate_credentials(self,
        auth_method: str, credentials: dict
    ) -> None:

        if auth_method == "PASSWORD":
            if not self.keys_in_dict(["username", "password"], credentials):
                raise ValueError("Provided credentials must contain a 'username' and 'password'")

    def keys_in_dict(self, keys: list, dict: dict) -> bool:
        for key in keys:
            if key not in dict:
                return False

        return True