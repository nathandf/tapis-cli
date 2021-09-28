from enum import Enum

class HandlerPrecedence(Enum):
    FIRST = "before"
    LAST = "after",
    NONE = None

class Option:
    def __init__(self,
        name: str,
        aliases: list = [],
        usage: str = None,
        params: tuple = (),
        handler: str = None,
        precedence: HandlerPrecedence = "before"
        
    ):
        self.name = name
        self.aliases = aliases
        self.usage = usage
        self.params = params
        self.handler = handler
        self.precedence = precedence
