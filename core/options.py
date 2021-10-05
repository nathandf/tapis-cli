from core.Option import Option
from core.OptionRegistrar import OptionRegistrar

option_registrar = OptionRegistrar()

option_registrar.register("core", [
    Option("-a", aliases=["-verbose"], usage="show additional information for a command invocation",
        context="cmd"),
    Option("-b", aliases=["-help"], usage="display help information for a command",
        context="cmd", handler="help")
])

option_registrar.register("TapipyCategory", [
    Option("-v", aliases=["-verbose"], usage="show additional information for a command invocation",
        context="cmd"),
    Option("-h", aliases=["-help"], usage="display help information for a command",
        context="cmd", handler="help"),
    Option("-j", aliases=["-json", "-jk"], usage="a json filename",
        params=("filename"), handler="jsonFileToKeywordArgs"),
    Option("-f", aliases=["-file, -contents"], usage="a filename",
        params=("filename"), handler="fileContentsToPositionalArg")
])

option_registrar.uses("TapipyCategory", "core")