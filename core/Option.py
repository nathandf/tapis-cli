from enum import Enum

class HandlerPrecedence(Enum):
    CMD = "cmd"
    BEFORE = "before"
    AFTER = "after"

class Option:
    def __init__(self,
        name: str,
        aliases: list = [],
        usage: str = None,
        params: tuple = (),
        handler: str = None,
        precedence: HandlerPrecedence = "before",
        dependencies: list = []
    ):
        self.name = name
        self.aliases = aliases
        self.usage = usage
        self.params = params
        self.handler = handler
        self.precedence = precedence
        self.dependencies = dependencies
