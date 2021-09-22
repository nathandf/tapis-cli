""" Handles the resolving (parsing) of commands and their options. """

import re

from core.Category import Category
from importlib import import_module
from importlib.util import find_spec
from utils.Logger import Logger
from typing import List, Tuple
from core.OpenApiCategory import OpenApiCategory

class Router:
    """
    Commands and their options are passed into the router/resolver.
    The options are parsed and then the command is resolved.
    """
    command_index: int = 1
    logger: Logger = None

    def __init__(self):
        self.logger = Logger()

    def resolve(self, args: List[str]) -> Tuple[Category, List[str]]:
        """ The command is resolved here. """
        # Category name
        category_name: str = args[0]
        # Parse the options from the args.
        options = self.parse_options(args[1:])
        # Set the command on the category.
        command_name: str = args[self.command_index]
        # Every element in the args list after the command index are arguments
        # for the category.
        command_arguments = args[self.command_index+1:]

        # The first step of command resolution is to check if a 
        # user-defined category exists by the name provided in args.
        if find_spec(f"categories.{category_name.capitalize()}") is not None:
            # Import and instantiate the category
            module = import_module( f"categories.{category_name.capitalize()}", "./" )
            category: type[Category] = getattr(module, f"{category_name.capitalize()}")()

            if not hasattr(category, command_name):
                # If the command being invoked doesn't exist on the category, 
                # update the category to be an instance of core.OpenApiCategory
                category = OpenApiCategory()
                # Set the resource, operation, and options
                category.set_resource(category_name)
                category.set_operation(command_name)
                category.set_options(options)

                return (category, command_arguments)
            
            # Set the options and command
            category.set_command(command_name)
            category.set_options(options)

            # Return the category with command and options set.
            return (category, command_arguments)

        # If a user-defined category doesn't exist, return an instance
        # of core.OpenApiCategory
        category = OpenApiCategory()

        # Set the resource, operation, and options
        category.set_resource(category_name)
        category.set_operation(command_name)
        category.set_options(options)

        return (category, command_arguments)
        
        
    def parse_options(self, args: List[str]) -> List[str]:
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