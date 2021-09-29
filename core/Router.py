"""Handles the resolving (parsing) of commands and their options."""
import re

from importlib.util import find_spec
from importlib import import_module
from typing import List, Tuple, Dict

from core.Category import Category
from core.OpenApiCategory import OpenApiCategory
from configs.options import option_registrar
from utils.Logger import Logger

class Router:
    """
    Commands and their options are passed into the router.
    The options are parsed and then the command is resolved.
    """
    command_index: int = 1
    logger: Logger = None
    tag_value_pattern = r"([\w\r\t\n!@#$%^&*()\-+\{\}\[\]|\\\/:;\"\'<>?\|,.`~=]*)"
    arg_option_tag_pattern = r"[-]{1}([\w]{1}[\w]*)"
    kw_arg_tag_pattern = r"[-]{2}([\w]{1}[\w]*)"
    cmd_option_pattern = r"^[-]{1}([a-z]+[a-z_]*)$"

    def __init__(self):
        self.logger = Logger()

    def resolve(self, args: List[str]) -> Tuple[Category, List[str]]:
        """The command is resolved here."""

        # Parse the arguments and extract the values
        (
            category_name,
            cmd_name,
            cmd_options,
            arg_options,
            kw_args,
            pos_args
        ) = self.parse_args(args)

        self.logger.debug(category_name)
        self.logger.debug(cmd_name)
        self.logger.debug(cmd_options)
        self.logger.debug(arg_options)
        self.logger.debug(kw_args)
        self.logger.debug(pos_args)
        
        # The first step of command resolution is to check if a 
        # user-defined category exists by the name provided in args.
        if find_spec(f"categories.{category_name.capitalize()}") is not None:
            # Import the category
            module = import_module( f"categories.{category_name.capitalize()}", "./" )
            category_class: type[Category] = getattr(module, f"{category_name.capitalize()}")

            if not hasattr(category_class, cmd_name):
                # If the command being invoked doesn't exist on the category, 
                # update the category to be an instance of core.OpenApiCategory
                category = OpenApiCategory()
                # Set the resource, operation, and options
                category.set_resource(category_name)
                category.set_operation(cmd_name)
                category.set_cmd_options(cmd_options)
                category.set_arg_options(arg_options)
                category.set_kw_args(kw_args)

                return (category, pos_args)
            
            # The category class has a method by the command name.
            # Instantiate the category class
            category = category_class()

            # Set the options and command
            category.set_command(cmd_name)
            category.set_cmd_options(cmd_options)
            category.set_arg_options(arg_options)
            category.set_kw_args(kw_args)

            # Return the category with command and options set.
            return (category, pos_args)

        # If a user-defined category doesn't exist, return an instance
        # of core.OpenApiCategory
        category = OpenApiCategory()

        # Set the resource, operation, and options
        category.set_resource(category_name)
        category.set_operation(cmd_name)
        category.set_cmd_options(cmd_options)
        category.set_arg_options(arg_options)
        category.set_kw_args(kw_args)

        return (category, pos_args)
        
        
    def parse_cmd_options(self, args: List[str]) -> List[str]:
        """Extract options from the arguments."""
        # Regex pattern for options.
        pattern = re.compile(rf"{self.cmd_option_pattern}")
        # First arg in the args list is the category.
        # For every option found in the args list, increment the command_index
        # by 1. If none are found, then the command name is at index 1.
        cmd_options = []
        for option in args:
            if pattern.match(option):
                cmd_options.append(option)
                self.command_index += 1
                continue
            break

        return cmd_options

    def parse_kw_args(self, args: List[str]) -> Dict[str, str]:
        """Parse keywords passed in as arguments."""
        # Regex pattern for keyword args and their values
        pattern = re.compile(rf"(?<=[\s]){self.kw_arg_tag_pattern}[\s]+{self.tag_value_pattern}(?=[\s])*", re.MULTILINE | re.UNICODE)
        return dict(pattern.findall(" " + " ".join(args)))

    def parse_arg_options(self, args: List[str]) -> Dict:
        # Regex pattern for arg options and their values
        pattern = re.compile(rf"(?<=[\s]){self.arg_option_tag_pattern}[\s]+{self.tag_value_pattern}(?=[\s])*", re.MULTILINE | re.UNICODE)
        return dict(pattern.findall(" " + " ".join(args)))

    def parse_args(self,
        args: List[str]) -> Tuple[
            str,
            str,
            List[str],
            Dict[str, str],
            Dict[str, str],
            List[str]
        ]:
        # Category name
        category_name: str = args[0]
        # Parse the options from the args. This also determines the
        # index of the command name via self.command_index
        cmd_options = self.parse_cmd_options(args[1:])
        # Set the command on the category.
        cmd_name: str = args[self.command_index]
        # Every element in the args list after the command index are arguments
        # for the category.
        command_args = args[self.command_index+1:]
        kw_args = self.parse_kw_args(command_args)
        arg_options = self.parse_arg_options(command_args)

        # Remove all options and keyword args from the args list. Only
        # positional arguments will remain
        pos_args = []
        kw_arg_indicies = []
        arg_option_indicies = []

        # Isolate positions arguments from the command args
        for index, item in enumerate(command_args):
            if re.match(rf"{self.kw_arg_tag_pattern}", item) is not None and index not in kw_arg_indicies:
                # Append the index of key
                kw_arg_indicies.append(index)
                # Append the index of the value
                kw_arg_indicies.append(index+1)
            if re.match(rf"{self.arg_option_tag_pattern}", item) is not None and index not in arg_option_indicies:
                # Append the index of key
                arg_option_indicies.append(index)
                # Append the index of the value
                arg_option_indicies.append(index+1)
        
        for index, item in enumerate(command_args):
            if index not in kw_arg_indicies and index not in arg_option_indicies:
                pos_args.append(item)

        return (
            category_name,
            cmd_name,
            cmd_options,
            arg_options,
            kw_args,
            pos_args
        )