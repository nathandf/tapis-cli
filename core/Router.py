""" Handles the resolving (parsing) of commands and their options. """

import re

from core.Category import Category
from importlib import import_module
from importlib.util import find_spec
from utils.Logger import Logger
from typing import List, Tuple, Dict
from core.OpenApiCategory import OpenApiCategory

class Router:
    """
    Commands and their options are passed into the router.
    The options are parsed and then the command is resolved.
    """
    command_index: int = 1
    logger: Logger = None

    def __init__(self):
        self.logger = Logger()

    def resolve(self, args: List[str]) -> Tuple[Category, List[str]]:
        """ The command is resolved here. """

        # Parse the arguments and extract the values
        (
            category_name,
            command_name,
            options,
            keyword_args,
            positional_args
        ) = self.parse_args(args)

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
                category.set_keyword_args(keyword_args)

                return (category, positional_args)
            
            # Set the options and command
            category.set_command(command_name)
            category.set_options(options)
            category.set_keyword_args(keyword_args)

            # Return the category with command and options set.
            return (category, positional_args)

        # If a user-defined category doesn't exist, return an instance
        # of core.OpenApiCategory
        category = OpenApiCategory()

        # Set the resource, operation, and options
        category.set_resource(category_name)
        category.set_operation(command_name)
        category.set_options(options)
        category.set_keyword_args(keyword_args)

        return (category, positional_args)
        
        
    def parse_options(self, args: List[str]) -> List[str]:
        """Extract options from the args"""
        # Regex pattern for options.
        pattern = re.compile(r"^[-]{1}[a-z]+[a-z_]*$")
        # First arg in the args list is the category.
        # For every option found in the args list, increment the command_index
        # by 1. If none are found, then the command name is at index 1.
        options = []
        for option in args:
            if pattern.match(option):
                options.append(option)
                self.command_index += 1
                continue
            break

        return options

    def parse_keyword_args(self, args: List[str]) -> Dict[str, str]:
        # Regex pattern for keyword args and their values
        # NOTE This is a weak pattern. Doesn't allow for "=" in 
        # the value of the keword argument AND double quotes
        # must be escaped on the command line.
        # matches: --someKeywordArg="someVlaue"
        # pattern = re.compile(r"[\s]{1}[-]{2}([\w]{1}[\w]*)[\s]*=[\s]*\"([\w\s\r\t\n!@#$%^&*()\-+\{\}\[\]|\\\/:;\"\'<>?\|,.`~]*)\"", re.MULTILINE | re.UNICODE)
        
        # This pattern is like the above but a little more flexible. Doesn't require
        # equal sign or quotes surrounding the value
        pattern = re.compile(r"(?<=[\s]){1}[-]{2}([\w]{1}[\w]*)[\s]+([\w\r\t\n!@#$%^&*()\-+\{\}\[\]|\\\/:;\"\'<>?\|,.`~=]*)(?=[\s])*", re.MULTILINE | re.UNICODE)
        return (dict(pattern.findall(" " + " ".join(args))))

    def parse_args(self, args: List[str]) -> Tuple[str, str, List, Dict, List]:
        # Category name
        category_name: str = args[0]
        # Parse the options from the args. This also keeps determines the
        # index of the command name via self.command_index
        options = self.parse_options(args[1:])
        # Set the command on the category.
        command_name: str = args[self.command_index]
        # Every element in the args list after the command index are arguments
        # for the category.
        command_args = args[self.command_index+1:]
        keyword_args = self.parse_keyword_args(command_args)

        # Remove all options and keyword args from the args list. Only
        # positional arguments will remain
        positional_args = []
        keyword_indicies = []

        for index, item in enumerate(command_args):
            if re.match(r"[-]{2}([\w]{1}[\w]*)", item) is not None and index not in keyword_indicies:
                # Append the index of key
                keyword_indicies.append(index)
                # Append the index of the value
                keyword_indicies.append(index+1)
        
        for index, item in enumerate(command_args):
            if index not in keyword_indicies:
                positional_args.append(item)

        return (
            category_name,
            command_name,
            options,
            keyword_args,
            positional_args
        )