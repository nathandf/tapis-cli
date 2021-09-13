class styles:
    DEBUG = '\033[95m'
    BLUE = '\033[94m'
    SUCCESS = '\033[92m'
    INFO = '\033[96m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Logger:
    def complete(self, message):
        print(f"{styles.SUCCESS}{styles.BOLD}✓{styles.RESET} {message}")

    def failed(self, message):
        print(f"{styles.ERROR}{styles.BOLD}x{styles.RESET} {message}")

    def success(self, message):
        print(f"\n{styles.SUCCESS}Success:{styles.RESET} {message}\n")

    def log(self, message=""):
        print(message)

    def info(self, message=""):
        print(f"\n{styles.INFO}Info:{styles.RESET} {message}\n")

    def warn(self, message=""):
        print(f"{styles.WARNING}Warning:{styles.RESET} {message}")

    def error(self, message=""):
        print(f"\n{styles.ERROR}Error:{styles.RESET} {message}\n")

    def debug(self, message=""):
        print(f"{styles.DEBUG}########## DEBUG ##########{styles.RESET}\n{message}\n{styles.DEBUG}######## END DEBUG ########{styles.RESET}")
    
