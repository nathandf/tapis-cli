import os, json

def help(category):
    if hasattr(category, "help"):
        category.override_exec = True
        category.help()
        return
    
    category.logger.warn(f"Category '{type(category).__name__}' has no help option for the {category.command} command")


def jsonFileToKeywordArgs(category, args):
    _, extension = os.path.splitext(category.arg_options["-j"])
    # Check that the extension of the file is '.json'
    if extension != ".json":
        raise Exception(f"Using argument option '-j' requires a json file argument. Provided: '{extension}'")
    # Convert the definition file into a json object
    obj = json.loads(open(category.arg_options["-j"], "r").read())
    for item, value in obj.items():
        category.kw_args[item] = value
    
    return args

def fileContentsToPositionalArg(category, args):
    file_contents = open(category.arg_options["-f"], "rb").read()
    args.append(file_contents)

    return args