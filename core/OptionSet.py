from typing import List
from core.Option import Option

class OptionSet:
    options: List[type[Option]]
    def __init__(self, options: List[type[Option]]):
        self.options = options

    def get_names(self) -> List[str]:
        return [option.name for option in self.options]

    def get_by_name(self, name) -> type[Option]:
        for option in self.options:
            if option.name == name:
                return option

        return