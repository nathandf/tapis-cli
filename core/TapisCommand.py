from tapipy.tapis import Tapis
from core.Command import Command
from core.Authenticator import Authenticator as Auth
from typing import Union
from configs import settings
import re

class TapisCommand(Command):

    client: Union[Tapis, None] = None

    def __init__(self):
        Command.__init__(self)
        try:
            self.client = Auth().authenticate()
            if self.client == None:
                self.exit()
        except SystemExit:
            self.exit()
        except:
            raise ValueError(f"Unable to authenticate user using AUTH_METHOD {settings.AUTH_METHOD}")

    def methods(self):
        all_methods = dir(getattr(self.client, type(self).__name__.lower()))
        methods = []

        pattern = re.compile(r"^[_]{2}[\w]+")
        for method in all_methods:
            if not re.match(pattern, method):
                methods.append(method)

        self.logger.log(methods)
