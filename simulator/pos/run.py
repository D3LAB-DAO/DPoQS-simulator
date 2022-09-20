from env import *

import os  # nopep8
import sys  # nopep8
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))  # nopep8

from cli import *
from log import *
from visual import *


# env
env = PosEnv(
    10,
    0.5, 0.6, 0.1, 1000000000,
    cost=0.3
)


# logs
bondedAmounts = list()
stakingRatios = list()
inflations = list()
totalSupplies = list()
blockNumbers = list()
annualProvisions = list()
blockProvisions = list()
validators = list()
nakamotoCoefs = list()


def curses_status(r: int):
    def curses_status_0_state():
        y = 0
        stdscr.addstr(y, 0, "State", curses.color_pair(Color.CYAN.value) | curses.A_BOLD); y += 1
        curses_addstr_helper(y, 0, "bondedAmount", env.bondedAmount, prefix="    "); y += 1
        curses_addstr_helper(y, 0, "stakingRatio", env.stakingRatio, prefix="    "); y += 1
        curses_addstr_helper(y, 0, "Inflation", env.Inflation, prefix="    ", color=Color.YELLOW); y += 1
        curses_addstr_helper(y, 0, "TotalSupply", env.TotalSupply, prefix="    "); y += 1
        curses_addstr_helper(y, 0, "blockNumber", env.blockNumber, prefix="    ", color=Color.YELLOW); y += 1
        curses_addstr_helper(y, 0, "step: ", env.step, color=Color.CYAN, prefix="    "); y += 1

    def curses_status_1_validator():
        y = 0
        stdscr.addstr(y, 0, "Validator", curses.color_pair(Color.CYAN.value) | curses.A_BOLD); y += 1
        curses_addstr_helper(y, 0, "numValidators", env.numValidators, prefix="    "); y += 1
        curses_addstr_helper(y, 0, "cost", env.cost, prefix="    "); y += 1
        curses_addstr_helper(y, 0, "Nakamoto Coef", env.nakamoto_coefficient, prefix="    ", color=Color.YELLOW); y += 1

    def curses_status_2_predefined():
        y = 0
        stdscr.addstr(y, 0, "Params", curses.color_pair(Color.CYAN.value) | curses.A_BOLD); y += 1
        curses_addstr_helper(y, 0, "GoalBonded", env.GoalBonded, prefix="    "); y += 1
        curses_addstr_helper(y, 0, "BlocksPerYr", env.BlocksPerYr, prefix="    "); y += 1
        curses_addstr_helper(y, 0, "InflationRateChange", env.InflationRateChange, prefix="    "); y += 1
        curses_addstr_helper(y, 0, "InflationMax", env.InflationMax, prefix="    "); y += 1
        curses_addstr_helper(y, 0, "InflationMin", env.InflationMin, prefix="    "); y += 1

    if r == 0:
        return curses_status_0_state
    elif r == 1:
        return curses_status_1_validator
    elif r == 2:
        return curses_status_2_predefined


def curses_help():
    def curses_help_addstr_helper(y: int, x: int, command: str, description: str, options: str = None, prefix: str = ""):
        stdscr.addstr(y, x, prefix)
        stdscr.addstr(command, curses.color_pair(Color.YELLOW.value) | curses.A_BOLD)
        stdscr.addstr(description)
        if options != None:
            stdscr.addstr(y, OPTION_X_LOCATION, options, curses.color_pair(Color.YELLOW.value))

    def curses_help_0_params():
        y = 0
        stdscr.addstr(y, 0, "Simulator Commands", curses.color_pair(Color.CYAN.value) | curses.A_BOLD); y += 1
        curses_help_addstr_helper(y, 0, "[N]", "nextBlocks", "<#_of_blocks>", prefix="    "); y += 1
        curses_help_addstr_helper(y, 0, "[B]", "bondedAmount", "<bonded_amount>", prefix="    "); y += 1
        curses_help_addstr_helper(y, 0, "[S]", "stakingRatio", "<%_of_staking_ratio>", prefix="    "); y += 1
        curses_help_addstr_helper(y, 0, "[C]", "cost", "<amount>", prefix="    "); y += 1

    def curses_help_1_logs():
        y = 0
        stdscr.addstr(y, 0, "Logs Commands", curses.color_pair(Color.CYAN.value) | curses.A_BOLD); y += 1
        # curses_help_addstr_helper(y, 0, "[R]", "reset", prefix="    "); y += 1  # TODO
        curses_help_addstr_helper(y, 0, "[P]", "step(window)", "<size_of_step>", prefix="    "); y += 1
        curses_help_addstr_helper(y, 0, "[K]", "saveFigs", "<name> [dpi]", prefix="    "); y += 1
        curses_help_addstr_helper(y, 0, "[L]", "saveLogs", "<name>", prefix="    "); y += 1

    r = 0
    while r >= 0 and r < 2:
        stdscr.clear()

        # commands
        x = 0; y = COMMAND_Y_LOCATION
        stdscr.addstr(y, 0, MSG_DOUBLE_SPLIT_LINE); y += 1
        stdscr.addstr(y, 0, ""); y += 1

        if r > 0:
            curses_command("[<]", description="prev")
        else:
            curses_command("[<]", colored_description="exit")

        if r < 1:
            curses_command("[>]", description="next", prefix="    ")
        else:
            curses_command("[>]", colored_description="exit", prefix="    ")

        # transition
        if r == 0:
            curses_help_0_params()
        elif r == 1:
            curses_help_1_logs()

        # input
        stdscr.addstr(y, 0, MSG_SINGLE_SPLIT_LINE); y += 1
        stdscr.addstr(y, 0, ""); y += 1
        i = stdscr.getkey()
        if i == ',' or i == '<': r -= 1
        elif i == '.' or i == '>': r += 1


def execute_transition(amount: int):
    global bondedAmounts
    global stakingRatios
    global inflations
    global totalSupplies
    global blockNumbers
    global annualProvisions
    global blockProvisions
    global validators
    global nakamotoCoefs

    e = env.transition(amount)
    bondedAmounts += e[0]
    stakingRatios += e[1]
    inflations += e[2]
    totalSupplies += e[3]
    blockNumbers += e[4]
    annualProvisions += e[5]
    blockProvisions += e[6]
    validators += e[7]
    nakamotoCoefs += e[8]


def curses_execute(keys: list):
    key = keys[0]

    if key == 'n' or key == 'N':
        amount = int(keys[1])
        execute_transition(amount)

    elif key == 'b' or key == 'B':
        amount = float(keys[1])
        env.setBondedAmount(amount)

    elif key == 's' or key == 'S':
        amount = float(keys[1])
        env.setStakingRatio(amount)

    elif key == 'p' or key == 'P':
        amount = float(keys[1])
        env.setStep(amount)

    elif key == 'k' or key == 'K':  # saveFigs
        dpi = 300
        if len(keys) == 3:
            dpi = int(keys[2])

        multi_draw_axis_3(
            keys[1] + "_state",  # name
            blockNumbers,  # x
            [bondedAmounts, totalSupplies],  # y1s
            inflations,  # y2
            stakingRatios,  # y3
            xlabel="blockNumbers",
            ylabels=[
                "amount",
                "inflation",
                "stakingRatio"
            ],
            legends=[
                "bondedAmount",
                "totalSupply",
                "inflation",
                "stakingRatio"
            ],
            dpi=dpi,
            save=True
        )

        multi_draw_axis_3(
            keys[1] + "_provs",  # name
            blockNumbers,  # x
            [inflations],  # y1s
            annualProvisions,  # y2
            blockProvisions,  # y3
            xlabel="blockNumbers",
            ylabels=[
                "inflation",
                "annualProvisions",
                "blockProvisions"
            ],
            legends=[
                "inflation",
                "annualProvision",
                "blockProvision"
            ],
            dpi=dpi,
            save=True
        )

        multi_draw(
            keys[1] + "_agents",  # name
            blockNumbers,  # x
            np.array(validators).T,  # ys
            xlabel="blockNumbers",
            ylabel="amount",
            dpi=dpi,
            save=True
        )

        multi_draw(
            keys[1] + "_coef",  # name
            blockNumbers,  # x
            [nakamotoCoefs],  # ys
            xlabel="blockNumbers",
            ylabel="nakamotoCoef",
            dpi=dpi,
            save=True
        )

    elif key == 'l' or key == 'L':  # saveLogs
        multi_logs(
            keys[1] + "_state",  # name
            blockNumbers,  # x
            [
                inflations,
                stakingRatios,
                bondedAmounts,
                totalSupplies
            ],  # ys
            legends=[
                "inflation",
                "stakingRatio",
                "bondedAmount",
                "totalSupply"
            ]
        )

        multi_logs(
            keys[1] + "_provs",  # name
            blockNumbers,  # x
            [
                inflations,
                stakingRatios,
                annualProvisions,
                blockProvisions
            ],  # ys
            legends=[
                "inflation",
                "stakingRatio",
                "annualProvision",
                "blockProvision"
            ]
        )

        multi_logs(
            keys[1] + "_agents",  # name
            blockNumbers,  # x
            validators,  # ys
            legends=["agent_" + str(i) for i in range(env.numValidators)],
            transposed=False
        )

        # TODO: detailed agent history log through agent_step

        multi_logs(
            keys[1] + "_coef",  # name
            blockNumbers,  # x
            [
                nakamotoCoefs
            ],  # ys
            legends=[
                "nakamotoCoef"
            ]
        )

    # WIP: keys


def curses_main():
    r = 0  # 0~2
    while True:
        stdscr.clear()

        curses_status(r)()

        # commands
        x = 0; y = COMMAND_Y_LOCATION
        stdscr.addstr(y, 0, MSG_DOUBLE_SPLIT_LINE); y += 1
        stdscr.addstr(y, 0, ""); y += 1
        curses_command("[H]", description="help")
        curses_command("[Q]", description="quit", prefix="    ")
        curses_command("[<]", description="prev_status", prefix="    ")
        curses_command("[>]", description="next_status", prefix="    ")

        # input
        stdscr.addstr(y, 0, MSG_SINGLE_SPLIT_LINE); y += 1
        stdscr.addstr(y, 0, ""); y += 1
        i = stdscr.getkey()
        if i == ':' or i == ';':
            keys = curses_keys(get_keys())  # transition
            curses_execute(keys)

        elif i == 'Q' or i == 'q':
            break
        elif i == 'H' or i == 'h':
            curses_help()

        elif i == ',' or i == '<':
            r = max(r - 1, 0)
        elif i == '.' or i == '>':
            r = min(r + 1, 2)


if __name__ == "__main__":
    # cli
    curses_intro()
    try:
        execute_transition(0)
        curses_main()
    except curses.error:
        print("curses.error: try resizing window (maybe not enough height)")
    finally:
        curses.endwin()
