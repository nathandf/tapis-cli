from core.TapipyCategory import TapipyCategory

from handlers.arg_options.OpenApiCategory import OpenApiCategory as ArgOptHandler

# TODO Use client initialization logic from Tapipy in OpenApiCategory
class OpenApiCategory(TapipyCategory):
    """
    Handles the parsing and execution of commands specified in the OpenAPI specs.

    Different tools, such as Tapipy, may inherit from this to specify their own
    specific categories and commands.
    """
    operation = None
    resource = None

    def __init__(self):
        TapipyCategory.__init__(self)

    def execute(self, args) -> None:
        """Overwrites the execute method to call the Tapipy client directly."""
        try:
            # Handle argument options.
            # NOTE: Arg option handler may update the state of the category.
            arg_opt_handler = ArgOptHandler()
            args = arg_opt_handler.handle(self, args)

            # Check that all keyword args for a given operation are
            # present.
            self.validate_keyword_args()

            if len(args) == 0 and len(self.keyword_args) == 0:
                result = self.operation()
            elif len(args) > 0 and len(self.keyword_args) == 0:
                result = self.operation(*args)
            elif len(args) == 0 and len(self.keyword_args) > 0:
                result = self.operation(**self.keyword_args)
            else:
                result = self.operation(*args, **self.keyword_args)

            if type(result) == enumerate or type(result) == list:
                for item in result:
                    self.logger.log(item)
                return

            self.logger.log(result)
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

    def validate_keyword_args(self):
        """Validates the keyword arguments required by an OpenAPI operation."""
        required_params = []
        for param in self.operation.path_parameters:
            if param.required:
                required_params.append(param.name)

        keyword_arg_keys = self.keyword_args.keys()
        for param in required_params:
            if param not in keyword_arg_keys:
                raise Exception(f"'{param}' is a required keyword argument. Required keyword arguments: {required_params}")