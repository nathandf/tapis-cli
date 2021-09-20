from importlib import import_module
from importlib.util import find_spec
from utils.Logger import Logger
import re, sys
from core.Category import Category

class Router:
    command_index = 1
    logger = None

    def __init__(self):
        self.logger = Logger()

    def resolve(self, args: list[str]) -> tuple[Category, list[str]]:
        # The first step of command resolution is to check if a
        # user-defined category exists by the name provided in args. If it does,
        # import it
        category_name = args[0]
        if find_spec(f"categories.{category_name.capitalize()}") is not None:
            # Import and instantiate the category
            module = import_module( f"categories.{category_name.capitalize()}", "./" )
            category = getattr(module, f"{category_name.capitalize()}")()

            # Set the options on the category.
            options = self.parse_options(args[1:])
            category.set_options(options)

            # Set the command on the category.
            command_name = args[self.command_index]
            if not hasattr(category, args[self.command_index]):
                # If the command being invoked doesn't exist on the category, 
                # return a generic instance of TapipyCategory
                # TODO implement tapipy category
                pass
                

            category.set_command(command_name)

            # Return the category with command and options set.
            # Every element in the args list after the command index are arguments
            # for the category.
            command_arguments = args[self.command_index+1:]
            return (category, command_arguments)

        # If a user-defined category doesn't exist, return a generic instance 
        # of TapipyCategory
        # TODO implement tapipy category
        
        # No category was found by the provided name
        # TODO Remove logging and exit line below once tapipy category is
        # implemented
        self.logger.error(f"Invalid category. '{category_name}' category not implemented")
        sys.exit(1)

    def parse_options(self, args: list[str]):
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