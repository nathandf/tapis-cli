""" The main driver of the TAPIs command line tool. """

import sys

from core.Router import Router


def main():
    """ Resolve the category, command, options, and arguments, then execute them. """
    (category, args) = Router().resolve(sys.argv[1:])
    category.execute(args)
    
if __name__ == "__main__":
    main()