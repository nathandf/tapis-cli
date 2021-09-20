""" Handles the resolving (parsing) of commands and their options. """

import re
import sys

from core.Category import Category
from importlib import import_module
from importlib.util import find_spec
from utils.Logger import Logger


class Router:
    """
    Commands and their options are passed into the router/resolver.
    The options are parsed and then the command is resolved.
    """
    command_index = 1
    logger = None

    def __init__(self):
        self.logger = Logger()

    def resolve(self, args: list[str]) -> tuple:
        """ The command is resolved here. """
        # The first step of command resolution is to check if a user-defined
        # category exists by the name provided in args. If it does, import it.
        if find_spec(f"categories.{args[0].capitalize()}") is not None:
            # Import and instantiate the category
            module = import_module( f"categories.{args[0].capitalize()}", "./" )
            category = getattr(module, f"{args[0].capitalize()}")()

            # Set the options on the category.
            options = self.parse_options(args[1:])
            category.set_options(options)

            # Set the command on the category.
            category.set_command(args[self.command_index])

            # If the command being invoked doesn't exist on the category, 
            # return a generic instance of TapipyCategory
            # TODO implement tapipy category

            # Return the category with command and options set.
            # Every element in the args list after the command index are arguments
            # for the category.
            return (category, args[self.command_index+1:])

        # If a user-defined category doesn't exist, return a generic instance 
        # of TapipyCategory
        # TODO implement tapipy category
        
        # No category was found by the provided name
        # TODO Remove logging and exit line below once tapipy category is
        # implemented
        self.logger.error(f"Invalid category. '{args[0]}' category not implemented.\n")
        sys.exit(1)

    def parse_options(self, args: list[str]):
        """ Checks to make sure the options are valid. """
        # Regex pattern for options.
        option_pattern = re.compile(r"^[-]{1,2}[a-z]+[a-z_]*$")

        # First arg in the args list is the category.
        # For every option found in the args list, increment the command_index
        # by 1. If none are found, then the command name is at index 1.
        options = []
        for option in args:
            if re.match(option_pattern, option):
                options.append(option)
                self.command_index += 1
                continue
            break

        return options