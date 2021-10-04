from typing import List

from core.Option import Option, HandlerContext

class OptionRegistrar:

    option_sets = {}
    registered_names = []
    registered_aliases = []

    def register(self, category: str, options: List[type[Option]]) -> None:

        # Do not allow options to be registered for a single category more than once
        if hasattr(self.option_sets, category):
            raise(f"Category '{category}' already has registered options")

        self.option_sets[category] = []
        # Validate the uniqueness of option names and aliases
        for option in options:
            if option.name in self.registered_names:
                raise ValueError(f"Option naming collision: Option already registered with name '{option.name}'")
            if option.name in self.registered_aliases:
                    raise ValueError(f"Option naming collision: Alias already exists with the name '{option.name}'")

            self.registered_names.append(option.name)
            
            for alias in option.aliases:
                if alias in self.registered_names:
                    raise ValueError(f"Alias naming collision: Option already registered with name '{alias}'")
                if alias in self.registered_aliases:
                    raise ValueError(f"Alias naming collision: Alias '{alias}' is already registered")
                
            self.registered_aliases = self.registered_aliases + option.aliases

            self.option_sets[category].append(option)

        # Reset the value of registered names and aliases for each call of the
        # register function
        self.registered_names = []
        self.registered_aliases = []

        return

    def get_option_set(self, category, context: type[HandlerContext]=None) -> List[type[Option]]:
        options = []
        if category in self.option_sets:
            # Return all options if no context is specified
            if context == None:
                return self.option_sets[category]

            for option in self.option_sets[category]:
                if option.context == context:
                    options.append(option)
                
        return options

    # Combine the options of one category to another. Specific options
    # can be selected by providing a list with the options' name in the
    # options keyword. If strict is set to True, an error will be thrown
    # categories contain duplicate option names. Otherwise, the options 
    # in the to_category will be overwritten.
    # TODO implement
    def use(self, to_category, from_category, options=[], strict=True):
        pass
