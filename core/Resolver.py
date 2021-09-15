from importlib import import_module
from utils.Logger import Logger
import re, sys

class Resolver:
    command_index = 1
    logger = None

    def __init__(self):
        self.logger = Logger()

    def resolve(self, args: list) -> None:
        # Import the category module and instantiate the class
        module = None
        try:
            module = import_module( f"categories.{args[0].capitalize()}", "./" )

            self.set_category(getattr(module, f"{args[0].capitalize()}")())

            # Set the options on the category.
            options = self.parse_options(args[1:])
            self.category.set_options(options)

            # Set the command on the category.
            self.category.set_command(args[self.command_index])

            # Return the category with command and options set.
            # Every element in the args list after the command index are arguments
            # for the category.
            return (self.category, args[self.command_index+1:])

        except ModuleNotFoundError:
            self.logger.error(f"Invalid category. '{args[0]}' category not implemented")
            sys.exit(1)

    def parse_options(self, args):
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
            
    def set_category(self, category):
        self.category = category