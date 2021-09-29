"""
Handles the command setting, command execution, and command help 
functionality for the TAPIS CLI (adaptable to use non-TAPIS commands
if the user creates new ones and a parser for non-TAPIS categories).
"""

import re
import sys
import types

from typing import Dict

from utils.Logger import Logger
from core.options import option_registrar

class Category:
    """ 
    Each category has the same methods available to get/set/execute.
    If the user wants to add non-TAPIS categories and commands, the new parser
    should inherit from this category. See 'TapipyCategory.py' for an example.
    """
    option_set = []
    options = []
    keyword_args: Dict[str, str] = {}
    arg_options: Dict[str, str] = {}
    command = "help"
    logger = None
    exit = sys.exit

    def __init__(self):
        self.logger = Logger()
        self.option_set = option_registrar.get_option_set(type(self).__name__)

    def help(self, **_):
        """
        \nGeneral usage:
        '*' indicates optional
        $tapis [category] [options] [command] [args/keyword args]
        \nExamples:
        - tapis systems get [systemId]
        - tapis systems getSystem --systemId [systemId]
        - tapis files upload [systems] [path/to/local/file] [destination/folder]
        - tapis systems update [path/to/definition/file]
        - tapis apps create [path/to/definition/file]
        - tapis jobs submit [appName] [appVersion]
        \nCommands:"""
        
        print(self.help.__doc__)
        methods = self.get_methods(self)
        for method in methods:
            print(f"\t- {method}")

    def set_command(self, command: str) -> None:
        """
        Sets the command to be executed in a specific category. 
        EX: apps = category, list = command
        """
        if command not in dir(self):
            self.logger.error(f"Category {type(self).__name__} has no command '{command}'\n")
            self.exit(1)
        self.command = command

        return
    
    def set_cmd_options(self, options: list) -> None:
        """Any options for the command are logged to the class."""
        self.options = options

        return

    def set_keyword_args(self, keyword_args: Dict[str, str]) -> None:
        self.keyword_args = keyword_args
        return

    def set_arg_options(self, arg_options: Dict[str, str]) -> None:
        self.arg_options = arg_options
        return

    def execute(self, args) -> None:
        """The command is executed (along with its options)."""
        method = getattr(self, self.command)
        method(*args)

        return

    def get_methods(self, instance: object) -> list:
        """Returns all of the methods that are available for the specified category."""
        # Get all props of of the instance.
        class_props = dir(instance)

        # Remove the dunders.
        props = []
        pattern = re.compile(r"^[_]{2}[\w]+")
        for prop in class_props:
            if not re.match(pattern, prop):
                props.append(prop)

        # Remove all class properties that are not functions.
        methods = []
        for prop_name in props:
            prop = getattr(instance, prop_name)
            if isinstance(prop, types.MethodType):
                methods.append(prop_name)

        return methods