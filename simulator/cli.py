from enum import Enum
import curses


stdscr = curses.initscr()
curses.start_color()
curses.use_default_colors()


class Color(Enum):
    WHITE = 0
    CYAN = 1
    MAGENTA = 2
    YELLOW = 3
    RED = 4
    GREEN = 5
    BLUE = 6


curses.init_pair(1, curses.COLOR_CYAN, -1)
curses.init_pair(2, curses.COLOR_MAGENTA, -1)
curses.init_pair(3, curses.COLOR_YELLOW, -1)
curses.init_pair(4, curses.COLOR_RED, -1)
curses.init_pair(5, curses.COLOR_GREEN, -1)
curses.init_pair(6, curses.COLOR_BLUE, -1)


COMMAND_Y_LOCATION = 10
OPTION_X_LOCATION = 30
MAX_LEN = 60
MSG_DOUBLE_SPLIT_LINE = "=" * MAX_LEN
MSG_SINGLE_SPLIT_LINE = "-" * MAX_LEN

ASCII_ART_SUPERNOVA = """
 ██▓ ███▄    █   █████▒██▓    ▄▄▄     ▄▄▄█████▓ ██▓ ▒█████   ███▄    █ 
▓██▒ ██ ▀█   █ ▓██   ▒▓██▒   ▒████▄   ▓  ██▒ ▓▒▓██▒▒██▒  ██▒ ██ ▀█   █ 
▒██▒▓██  ▀█ ██▒▒████ ░▒██░   ▒██  ▀█▄ ▒ ▓██░ ▒░▒██▒▒██░  ██▒▓██  ▀█ ██▒
░██░▓██▒  ▐▌██▒░▓█▒  ░▒██░   ░██▄▄▄▄██░ ▓██▓ ░ ░██░▒██   ██░▓██▒  ▐▌██▒
░██░▒██░   ▓██░░▒█░   ░██████▒▓█   ▓██▒ ▒██▒ ░ ░██░░ ████▓▒░▒██░   ▓██░
░▓  ░ ▒░   ▒ ▒  ▒ ░   ░ ▒░▓  ░▒▒   ▓▒█░ ▒ ░░   ░▓  ░ ▒░▒░▒░ ░ ▒░   ▒ ▒ 
 ▒ ░░ ░░   ░ ▒░ ░     ░ ░ ▒  ░ ▒   ▒▒ ░   ░     ▒ ░  ░ ▒ ▒░ ░ ░░   ░ ▒░
 ▒ ░   ░   ░ ░  ░ ░     ░ ░    ░   ▒    ░       ▒ ░░ ░ ░ ▒     ░   ░ ░ 
 ░           ░            ░  ░     ░  ░         ░      ░ ░           ░ 
"""


def curses_intro():
    stdscr.addstr("@hardlucidpark's\n")
    stdscr.addstr(ASCII_ART_SUPERNOVA)
    stdscr.addstr("\n\n")
    stdscr.addstr(" " * 22 + "Press any key to start ...", curses.color_pair(Color.RED.value))
    stdscr.getkey()  # pause


def curses_command(command: str, description: str = "", colored_description: str = "", prefix: str = ""):
    stdscr.addstr(prefix)
    stdscr.addstr(command, curses.color_pair(Color.MAGENTA.value) | curses.A_BOLD)
    stdscr.addstr(description)
    stdscr.addstr(colored_description, curses.color_pair(Color.MAGENTA.value))


def curses_addstr_helper(y: int, x: int, name: str, value: str, prefix: str = "", color: Color = Color.WHITE):
    if type(name) != str:
        name = str(name)
    if type(value) != str:
        value = str(value)
    if type(prefix) != str:
        prefix = str(prefix)

    stdscr.addstr(y, x, prefix)
    stdscr.addstr(name, curses.color_pair(color.value))
    stdscr.addstr(y, OPTION_X_LOCATION, ": ")
    l = stdscr.getyx()[1]
    if l + len(value) > MAX_LEN:
        stdscr.addstr(value[:-(l + len(value) - MAX_LEN)])
        stdscr.addstr(y, MAX_LEN - 3, "...")
    else:
        stdscr.addstr(value)


def get_keys():
    while True:
        keys = stdscr.getstr().decode()
        keys = keys.split()
        if len(keys) > 0:
            return keys


def curses_keys(keys: list):
    # log  # TODO
    return keys


if __name__ == "__main__":
    curses_intro()
    curses.endwin()
