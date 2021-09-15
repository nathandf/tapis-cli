from core.Router import Router
import sys

def main():
    # Resolve the category, command, options, and arguments, then execute it
    (category, args) = Router().resolve(sys.argv[1:])
    category.execute(args)
    
if __name__ == "__main__":
    main()