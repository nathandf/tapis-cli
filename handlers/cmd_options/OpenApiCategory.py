from handlers.cmd_options.CmdOptHandler import CmdOptHandler

class OpenApiCategory(CmdOptHandler):
    def __init__(self, cmd_option_map = {
        "t": "tableView"
    }):
        CmdOptHandler.__init__(self, cmd_option_map=cmd_option_map)

    def tableView():
        pass

                