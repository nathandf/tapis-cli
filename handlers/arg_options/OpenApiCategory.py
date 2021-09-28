from handlers.arg_options.ArgOptHandler import ArgOptHandler

class OpenApiCategory(ArgOptHandler):
    def __init__(self, arg_option_map = {
        "j": "jsonFileToKeywordArgs",
        "f": "fileContentsToPositionalArg"
    }):
        ArgOptHandler.__init__(self, arg_option_map=arg_option_map)
                