import os, json

class ArgOptHandler:

    category = None
    args = []
    arg_option_map = {}

    def __init__(self, arg_option_map={}):
        self.arg_option_map = arg_option_map

    def handle(self, category, args):
        self.category = category
        self.args = args

        for option in self.category.arg_options.keys():
            if option not in self.arg_option_map:
                raise ValueError(f"Handler '{type(self).__name__}' is not configured to accept '-{option}' as an option")

            if not hasattr(self, self.arg_option_map[option]):
                raise Exception(f"Handler function '{self.arg_option_map[option]}' exists")

            fn = getattr(self, self.arg_option_map[option])
            try:
                fn()
            except Exception as e:
                raise Exception(e)

        return self.args

    def jsonFileToKeywordArgs(self):
        _, extension = os.path.splitext(self.category.arg_options["j"])
        # Check that the extension of the file is '.json'
        if extension != ".json":
            raise ValueError(f"Using argument option '-j' requires a json file argument. Provided: '{extension}' ")
        # Convert the definition file into a json object
        obj = json.loads(open(self.category.arg_options["j"], "r").read())
        for item, value in obj.items():
            self.category.keyword_args[item] = value
        
        return

    def fileContentsToPositionalArg(self):
        file_contents = open(self.category.arg_options["f"], "rb").read()
        self.args.append(file_contents)

        return