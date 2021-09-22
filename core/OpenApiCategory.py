from core.TapipyCategory import TapipyCategory

# TODO Use client initialization logic from Tapipy in OpenApiCategory
class OpenApiCategory(TapipyCategory):
    """
    Overwrites the execute method to access the
    Tapipy client directly
    """
    operation = None
    resource = None

    def __init__(self):
        TapipyCategory.__init__(self)

    def execute(self, args) -> None:
        if len(args) > 0:
            result = self.operation(*args)
        else:
            result = self.operation()

        print(result)

        return

    def set_operation(self, operation_name: str) -> None:
        try:
            self.operation = getattr(self.resource, operation_name)
            return
        except:
            self.logger.error(f"{type(self.resource).__name__} has no operation '{operation_name}'\n")
            self.exit(1)

    def set_resource(self, resource_name: str) -> None:
        try:
            self.resource = getattr(self.client, resource_name)
            return
        except:
            self.logger.error(f"{type(self).__name__} has no resource '{resource_name}'\n")
            self.exit(1)
