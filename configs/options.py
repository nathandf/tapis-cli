from core.Option import Option
from core.OptionRegistrar import OptionRegistrar

option_registrar = OptionRegistrar()

option_registrar.register("core.all", [
    Option("-v", aliases=["-verbose"], usage="show additional information for a command invocation",
    context="cmd"),
    Option("-h", aliases=["-help"], usage="display help information for a command",
    context="cmd")
])

option_registrar.register("OpenApiCategory", [
    Option("-j", aliases=["-json", "-jk"], usage="a json filename",
        params=("filename"), handler="jsonFileToKeywordArgs"),
    Option("-f", aliases=["-file, -contents"], usage="a filename",
        params=("filename"), handler="fileContentsToPositionalArg")
])

option_registrar.use("core.all", "OpenApiCategory")