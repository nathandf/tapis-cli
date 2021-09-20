""" Handles the configuring of credentials. """

from core.Category import Category
from core.Configuration import Configuration


class Auth(Category):
    """ Configurations are parsed here. """
    def __init__(self):
        Category.__init__(self)
        self.config = Configuration()

    def configure(self):
        """ Configures the settings to handle input credentials. """
        self.config.configure()
