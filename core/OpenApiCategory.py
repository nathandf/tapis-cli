from tabulate import tabulate

import core.handlers

from configs import settings
from core.Category import Category
from core.Authenticator import Authenticator as Auth

class OpenApiCategory(Category):
    """
    Handles the parsing and execution of commands specified in the OpenAPI specs.

    Different tools, such as Tapipy, may inherit from this to specify their own
    specific categories and commands.
    """
    operation = None
    resource = None

    def __init__(self):
        Category.__init__(self)
        try:
            self.client = Auth().authenticate()
            if self.client == None:
                self.exit()
        except SystemExit:
            self.exit()
        except:
            raise ValueError(f"Unable to authenticate user using AUTH_METHOD {settings.AUTH_METHOD}\n")

    def execute(self, args) -> None:
        """Overwrites the execute method to call the Tapipy client directly."""
        try:
            for option in self.option_set:
                if option.name not in self.arg_options:
                    continue
                if not hasattr(core.handlers, option.handler):
                    raise ValueError(f"Option handler '{option.handler} does not exist'")

                fn = getattr(core.handlers, option.handler)
                args = fn(self, args)

            # Check that all keyword args for a given operation are
            # present.
            self.validate_kw_args()

            result = self.operation(*args, **self.kw_args)

            if type(result) == list:
                for _, item in enumerate(result):
                    self.logger.log(tabulate(vars(item).items(), tablefmt="fancy_grid"))
                
                return

            self.logger.log(tabulate(vars(result).items(), ["Key", "Value"], tablefmt="fancy_grid"))
            return

        except Exception as e:
            self.logger.error(e)

    def set_operation(self, operation_name: str) -> None:
        """Sets the operation to be performed upon execution."""
        try:
            self.operation = getattr(self.resource, operation_name)
            return
        except:
            self.logger.error(f"{type(self.resource).__name__} has no operation '{operation_name}'\n")
            self.exit(1)

    def set_resource(self, resource_name: str) -> None:
        """Gets the resource name for the OpenAPI command."""
        try:
            self.resource = getattr(self.client, resource_name)
            return
        except:
            self.logger.error(f"{type(self).__name__} has no resource '{resource_name}'\n")
            self.exit(1)

    def validate_kw_args(self):
        """Validates the keyword arguments required by an OpenAPI operation."""
        required_params = []
        for param in self.operation.path_parameters:
            if param.required:
                required_params.append(param.name)

        kw_arg_keys = self.kw_args.keys()
        for param in required_params:
            if param not in kw_arg_keys:
                raise Exception(f"'{param}' is a required keyword argument. Required keyword arguments: {required_params}")