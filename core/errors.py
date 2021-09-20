class CLIBaseError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"message: {self.message}"

    def __repr__(self):
        return str(self)

class InvalidCategoryError(CLIBaseError):
    pass

class InvalidCommandError(CLIBaseError):
    pass
        