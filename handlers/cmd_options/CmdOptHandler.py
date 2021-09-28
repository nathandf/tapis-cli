import os, json

class CmdOptHandler:

    category = None
    result = None
    cmd_option_map = {}

    def __init__(self, cmd_option_map={}):
        self.cmd_option_map = cmd_option_map

    def handle(self, category, result):
        self.category = category
        self.result = result

        for option in self.category.cmd_options.keys():
            if option not in self.cmd_option_map:
                raise ValueError(f"Handler '{type(self).__name__}' is not configured to accept '-{option}' as an option")

            if not hasattr(self, self.cmd_option_map[option]):
                raise Exception(f"Handler function '{self.cmd_option_map[option]}' exists")

            fn = getattr(self, self.cmd_option_map[option])
            try:
                fn()
            except Exception as e:
                raise Exception(e)

        return self.result