import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# The background is set with 40 plus the number of the color, and the foreground with 30

# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


COLORS = {"WARNING": YELLOW, "INFO": CYAN, "DEBUG": BLUE, "CRITICAL": RED, "ERROR": RED}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


# Custom logger class with multiple destinations
class ColoredLogger(logging.Logger):
    FORMAT = (
        "[$BOLD%(asctime)-25s$RESET] - [$BOLD%(name)-10s$RESET] - [%(levelname)-18s] - "
        "%(message)-80s || ($BOLD%(filename)s$RESET:%(lineno)d)"
    )
    COLOR_FORMAT = formatter_message(FORMAT, True)

    def __init__(self, name, log_level=logging.DEBUG):
        logging.Logger.__init__(self, name, log_level)

        color_formatter = ColoredFormatter(self.COLOR_FORMAT)

        console = logging.StreamHandler()
        console.setFormatter(color_formatter)

        self.addHandler(console)


if __name__ == "__main__":
    test_logger = ColoredLogger("test_logger")
    test_logger.debug("DEBUG LOG")
    test_logger.info("INFO LOG")
    test_logger.warning("WARNING LOG")
    test_logger.error("ERROR LOG")
