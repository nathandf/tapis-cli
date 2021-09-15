""" Handles the configuring of credentials """

from core.Command import Command
from core.Configuration import Configuration

class Auth(Command):
    """ Authorization credentials are parsed here. """
    def __init__(self):
        Command.__init__(self)
        self.config = Configuration()

    def configure(self):
        """ Configures the settings to handle input credentials. """
        self.config.configure()
