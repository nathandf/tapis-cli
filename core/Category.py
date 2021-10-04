"""
Handles the command setting, command execution, and command help 
functionality for the TAPIS CLI (adaptable to use non-TAPIS commands
if the user creates new ones and a parser for non-TAPIS categories).
"""

import re
import sys
import types

from typing import List, Dict

from utils.Logger import Logger
from core.OptionSet import OptionSet
from core.options import option_registrar

class Category:
    """ 
    Each category has the same methods available to get/set/execute.
    If the user wants to add non-TAPIS categories and commands, the new parser
    should inherit from this category. See 'TapipyCategory.py' for an example.
    """
    option_set: type[OptionSet] = None
    cmd_options = []
    kw_args: Dict[str, str] = {}
    arg_options: Dict[str, List[str]] = {}
    command = "help"
    override_exec = False
    logger: type[Logger] = None
    exit = sys.exit
    arg_option_tag_pattern = r"([-]{1}[\w]{1}[\w]*)"

    def __init__(self):
        self.logger = Logger()
        self.option_set = option_registrar.get_option_set(type(self).__name__)

    def help(self):
        """
        \nGeneral usage:
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
    
    def set_cmd_options(self, cmd_options: list) -> None:
        self.cmd_options = cmd_options

        return

    def set_kw_args(self, kw_args: Dict[str, str]) -> None:
        self.kw_args = kw_args
        return

    def set_arg_options(self, arg_options: Dict[str, List[str]]) -> None:
        self.arg_options = arg_options
        return

    def execute(self, args: List[str]) -> None:
        if self.override_exec:
            return

        method = getattr(self, self.command)
        method(*args)

        return

    def get_methods(self, instance: object) -> list:
        """Returns all of the methods that are available for the specified category."""
        # Get all props of of the instance.
        class_props = dir(instance)

        # Remove the dunders.
        props = []
        pattern = re.compile(r"^[_]{1:2}[\w]+")
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

    def parse_args(self, args: list[str]):
        pos_args = []
        arg_option_indicies = []
        option_names = self.option_set.get_names()
        for index, arg in enumerate(args):
            # This line will skip the indicies of arg option parameters
            if index in arg_option_indicies:
                continue

            # If the arg doesn't match the arg_option_tag_pattern, then it
            # is a positional argument
            if re.match(rf"{self.arg_option_tag_pattern}", arg) == None:
                pos_args.append(arg)
                continue

            # Validate options against the category's option set
            if arg in option_names:
                option = self.option_set.get_by_name(arg)
                params = option.params
                num_of_params = len(params)
                remaining_args = args[index:]
                # If the number of args passed after the option is insufficient
                # to satisfy the option, raise an exception
                if  len(remaining_args) < num_of_params:
                    raise Exception(f"Option {arg} expects {num_of_params} params: {params}. Only {len(remaining_args)} params providied")
                arg_option_vals = args[index+1:index+1+num_of_params]
                # Set the arg options and their params values
                self.arg_option[arg] = (val for val in arg_option_vals)
            
