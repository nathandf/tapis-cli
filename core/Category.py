from core.Logger import Logger
import sys, re, types

class Category:
    options = []
    command = "help"
    logger = None
    exit = sys.exit

    def __init__(self):
        self.logger = Logger()

    def help(self, **args):
        """
        \nGeneral usage:
        $tapis [category] [command] [args]
        \nExamples:
        - tapis systems get [systemId]
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
        if command not in dir(self):
            self.logger.error(f"Category {type(self).__name__} has no command '{command}'")
            self.exit(1)
        self.command = command
    
    def set_options(self, options: list):
        self.options = options

    def execute(self, args) -> None:
        method = getattr(self, self.command)
        method(*args)

    def get_methods(self, instance: object) -> list:

        # Get all props of of the instance
        class_props = dir(instance)

        # Remove the dunders
        props = []
        pattern = re.compile(r"^[_]{2}[\w]+")
        for prop in class_props:
            if not re.match(pattern, prop):
                props.append(prop)

        # Remove all class properties that are not functions
        methods = []
        for prop_name in props:
            prop = getattr(instance, prop_name)
            if isinstance(prop, types.MethodType):
                methods.append(prop_name)

        return methods