from core.Option import Option
from core.OptionRegistrar import OptionRegistrar

option_registrar = OptionRegistrar()

option_registrar.register("OpenApiCategory", [
    Option("j", aliases=["json", "jk"], usage="a json filename",
        params=("filename"), handler="jsonFileToKeywordArgs"),
    Option("f", aliases=["file, contents"], usage="a filename",
        params=("filename"), handler="fileContentsToPositionalArg")
])