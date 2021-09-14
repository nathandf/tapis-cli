from core.Configuration import Configuration
from core.Command import Command

class Auth(Command):

    def __init__(self):
        Command.__init__(self)
        self.config = Configuration()

    def configure(self):
        self.config.configure()
