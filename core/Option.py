from enum import Enum

class HandlerContext(Enum):
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
        context: HandlerContext = "before",
        dependencies: list = []
    ):
        self.name = name
        self.aliases = aliases
        self.usage = usage
        self.params = params
        self.handler = handler
        self.context = context
        self.dependencies = dependencies
