from handlers.arg_options.ArgOptionHandler import ArgOptionHandler

class OpenApiCategory(ArgOptionHandler):
    def __init__(self, arg_option_map = {
        "j": "jsonFileToKeywordArgs",
        "f": "fileContentsToPositionalArg"
    }):
        ArgOptionHandler.__init__(self, arg_option_map=arg_option_map)
                