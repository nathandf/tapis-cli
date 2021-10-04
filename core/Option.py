from enum import Enum
from typing import Dict

class HandlerContext(Enum):
    CMD = "cmd"
    BEFORE = "before"
    AFTER = "after"

class Option:
    def __init__(self,
        name: str,
        aliases: list = [],
        usage: str = None,
        params: list[Dict[str, str]] = [],
        handler: str = None,
        context: HandlerContext = "before",
        required: bool = False,
        require: list = [],
        exclude: list = [],
        precedes: list = [],
        follows: list = []
    ):
        self.name = name
        self.aliases = aliases
        self.usage = usage
        self.params = params
        self.handler = handler
        self.context = context
        self.required = required
        self.require = require
        self.exclude = exclude
        self.precedes = precedes
        self.follows = follows
