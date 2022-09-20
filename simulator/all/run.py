from random import randint
from typing import List

import os  # nopep8
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))  # nopep8

from pos.env import PosEnv, PosAgent
from dpos.env import DposEnv, DposAgent
from dpos.agent import delegate as dpos_delegate
from dpoqs.env import DpoqsEnv, DpoqsAgent
from dpoqs.agent import delegate as dpoqs_delegate

from cli import *
from log import *
from visual import *


LIMIT_NUM_VALIDATORS = 21

NUM_NODES = 50
BONDED_RATIO = 0.5
STAKING_RATIO = 0.6
INFLATION = 0.1
TOTAL_SUPPLY = 1000000000
VALIDATION_COST = 0.3
DELEGATION_COST = 0.01


def init_nodes(num_nodes, bonded_amount, commission_fee, validate_cost, delegate_cost):
    def _init_dist_nodes(size, amount, alpha=1.16, lower=1., upper=None):
        s = np.random.pareto(alpha, size) + lower
        if upper != None:
            s = s[s < upper]  # kill outliers
        s /= sum(s)
        s *= amount
        _wealthes = np.sort(s)[::-1]  # TODO: floating errors
        return _wealthes

    init_is_validators = [True if i < LIMIT_NUM_VALIDATORS else False for i in range(num_nodes)]
    init_wealthes = _init_dist_nodes(num_nodes, bonded_amount)

    pos_nodes = [
        PosAgent(
            wealth=init_wealth,
            validate_cost=validate_cost
        ) for init_wealth in init_wealthes
    ]
    dpos_nodes = [
        DposAgent(
            is_validator=init_is_validator,
            wealth=init_wealth,
            commission_fee=commission_fee,
            validate_cost=validate_cost,
            delegate_cost=delegate_cost
        ) for (init_is_validator, init_wealth) in zip(init_is_validators, init_wealthes)
    ]
    dpoqs_nodes = [
        DpoqsAgent(
            is_validator=init_is_validator,
            wealth=init_wealth,
            commission_fee=commission_fee,
            validate_cost=validate_cost,
            delegate_cost=delegate_cost
        ) for (init_is_validator, init_wealth) in zip(init_is_validators, init_wealthes)
    ]

    return pos_nodes, dpos_nodes, dpoqs_nodes


# agents & envs
pos_nodes, dpos_nodes, dpoqs_nodes = init_nodes(
    NUM_NODES,
    BONDED_RATIO * TOTAL_SUPPLY,
    commission_fee=0.05,
    validate_cost=VALIDATION_COST, delegate_cost=DELEGATION_COST
)
pos_env = PosEnv(
    NUM_NODES,
    BONDED_RATIO, STAKING_RATIO, INFLATION, TOTAL_SUPPLY,
    nodes=pos_nodes,
    validate_cost=VALIDATION_COST
)
dpos_env = DposEnv(
    NUM_NODES,
    BONDED_RATIO, STAKING_RATIO, INFLATION, TOTAL_SUPPLY,
    nodes=dpos_nodes,
    validate_cost=VALIDATION_COST, delegate_cost=DELEGATION_COST
)
dpoqs_env = DpoqsEnv(
    NUM_NODES,
    BONDED_RATIO, STAKING_RATIO, INFLATION, TOTAL_SUPPLY,
    nodes=dpoqs_nodes,
    validate_cost=VALIDATION_COST, delegate_cost=DELEGATION_COST
)

rands = [randint(0, LIMIT_NUM_VALIDATORS - 1) for _ in range(NUM_NODES - LIMIT_NUM_VALIDATORS)]
# init_delegates(dpos_env)
for i in range(LIMIT_NUM_VALIDATORS, NUM_NODES):
    dpos_delegate(
        dpos_env._nodes[i],
        dpos_env._nodes[rands[i - LIMIT_NUM_VALIDATORS]],
        dpos_env._nodes[i].wealth
    )
# init_delegates(dpoqs_env)
for i in range(LIMIT_NUM_VALIDATORS, NUM_NODES):
    dpoqs_delegate(
        dpoqs_env._nodes[i],
        dpoqs_env._nodes[rands[i - LIMIT_NUM_VALIDATORS]],
        dpoqs_env._nodes[i].wealth
    )


# logs
class Data:
    def __init__(self):
        self.bondedAmounts = list()
        self.stakingRatios = list()
        self.inflations = list()
        self.totalSupplies = list()
        self.blockNumbers = list()
        self.annualProvisions = list()
        self.blockProvisions = list()
        self.nodes = list()
        self.nakamotoCoefs_powers = list()
        self.nakamotoCoefs_wealth = list()


pos_data = Data()
dpos_data = Data()
dpoqs_data = Data()


def curses_status(r: int, env_int: int):
    if env_int == 0:
        env = pos_env

        def curses_status_0_state():
            y = 0
            stdscr.addstr(y, 0, "PoS State", curses.color_pair(Color.CYAN.value) | curses.A_BOLD); y += 1
            curses_addstr_helper(y, 0, "bondedAmount", env.bondedAmount, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "stakingRatio", env.stakingRatio, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "Inflation", env.Inflation, prefix="    ", color=Color.YELLOW); y += 1
            curses_addstr_helper(y, 0, "TotalSupply", env.TotalSupply, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "blockNumber", env.blockNumber, prefix="    ", color=Color.YELLOW); y += 1
            curses_addstr_helper(y, 0, "step: ", env.step, color=Color.CYAN, prefix="    "); y += 1

        def curses_status_1_validator():
            y = 0
            stdscr.addstr(y, 0, "PoS Validator", curses.color_pair(Color.CYAN.value) | curses.A_BOLD); y += 1
            curses_addstr_helper(y, 0, "numNodes", env.numNodes, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "cost", env.validate_cost, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "Nakamoto Coef", env.nakamoto_coefficient, prefix="    ", color=Color.YELLOW); y += 1

        def curses_status_2_predefined():
            y = 0
            stdscr.addstr(y, 0, "PoS Params", curses.color_pair(Color.CYAN.value) | curses.A_BOLD); y += 1
            curses_addstr_helper(y, 0, "GoalBonded", env.GoalBonded, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "BlocksPerYr", env.BlocksPerYr, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "InflationRateChange", env.InflationRateChange, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "InflationMax", env.InflationMax, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "InflationMin", env.InflationMin, prefix="    "); y += 1

    elif env_int == 1:
        env = dpos_env

        def curses_status_0_state():
            y = 0
            stdscr.addstr(y, 0, "DPoS State", curses.color_pair(Color.CYAN.value) | curses.A_BOLD); y += 1
            curses_addstr_helper(y, 0, "bondedAmount", env.bondedAmount, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "stakingRatio", env.stakingRatio, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "Inflation", env.Inflation, prefix="    ", color=Color.YELLOW); y += 1
            curses_addstr_helper(y, 0, "TotalSupply", env.TotalSupply, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "blockNumber", env.blockNumber, prefix="    ", color=Color.YELLOW); y += 1
            curses_addstr_helper(y, 0, "step: ", env.step, color=Color.CYAN, prefix="    "); y += 1

        def curses_status_1_validator():
            y = 0
            stdscr.addstr(y, 0, "DPoS Validator", curses.color_pair(Color.CYAN.value) | curses.A_BOLD); y += 1
            curses_addstr_helper(y, 0, "numNodes", env.numNodes, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "validate_cost", env.validate_cost, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "delegate_cost", env.delegate_cost, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "Nakamoto Coef Powers", env.nakamoto_coefficient_powers, prefix="    ", color=Color.YELLOW); y += 1
            curses_addstr_helper(y, 0, "Nakamoto Coef Wealth", env.nakamoto_coefficient_wealth, prefix="    ", color=Color.YELLOW); y += 1

        def curses_status_2_predefined():
            y = 0
            stdscr.addstr(y, 0, "DPoS Params", curses.color_pair(Color.CYAN.value) | curses.A_BOLD); y += 1
            curses_addstr_helper(y, 0, "GoalBonded", env.GoalBonded, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "BlocksPerYr", env.BlocksPerYr, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "InflationRateChange", env.InflationRateChange, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "InflationMax", env.InflationMax, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "InflationMin", env.InflationMin, prefix="    "); y += 1

    elif env_int == 2:
        env = dpoqs_env

        def curses_status_0_state():
            y = 0
            stdscr.addstr(y, 0, "DPoQS State", curses.color_pair(Color.CYAN.value) | curses.A_BOLD); y += 1
            curses_addstr_helper(y, 0, "bondedAmount", env.bondedAmount, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "stakingRatio", env.stakingRatio, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "Inflation", env.Inflation, prefix="    ", color=Color.YELLOW); y += 1
            curses_addstr_helper(y, 0, "TotalSupply", env.TotalSupply, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "blockNumber", env.blockNumber, prefix="    ", color=Color.YELLOW); y += 1
            curses_addstr_helper(y, 0, "step: ", env.step, color=Color.CYAN, prefix="    "); y += 1

        def curses_status_1_validator():
            y = 0
            stdscr.addstr(y, 0, "DPoQS Validator", curses.color_pair(Color.CYAN.value) | curses.A_BOLD); y += 1
            curses_addstr_helper(y, 0, "numNodes", env.numNodes, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "validate_cost", env.validate_cost, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "delegate_cost", env.delegate_cost, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "Nakamoto Coef Powers", env.nakamoto_coefficient_powers, prefix="    ", color=Color.YELLOW); y += 1
            curses_addstr_helper(y, 0, "Nakamoto Coef Wealth", env.nakamoto_coefficient_wealth, prefix="    ", color=Color.YELLOW); y += 1

        def curses_status_2_predefined():
            y = 0
            stdscr.addstr(y, 0, "DPoQS Params", curses.color_pair(Color.CYAN.value) | curses.A_BOLD); y += 1
            curses_addstr_helper(y, 0, "GoalBonded", env.GoalBonded, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "BlocksPerYr", env.BlocksPerYr, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "InflationRateChange", env.InflationRateChange, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "InflationMax", env.InflationMax, prefix="    "); y += 1
            curses_addstr_helper(y, 0, "InflationMin", env.InflationMin, prefix="    "); y += 1

    else:
        raise ValueError

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
        curses_help_addstr_helper(y, 0, "[V]", "validate_cost", "<amount>", prefix="    "); y += 1
        curses_help_addstr_helper(y, 0, "[C]", "delegate_cost", "<amount>", prefix="    "); y += 1

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
    global pos_data
    global dpos_data
    global dpoqs_data

    for env, data in zip([pos_env, dpos_env, dpoqs_env], [pos_data, dpos_data, dpoqs_data]):
        e = env.transition(amount)

        data.bondedAmounts += e[0]
        data.stakingRatios += e[1]
        data.inflations += e[2]
        data.totalSupplies += e[3]
        data.blockNumbers += e[4]
        data.annualProvisions += e[5]
        data.blockProvisions += e[6]
        data.nodes += e[7]
        if env != pos_env:
            data.nakamotoCoefs_powers += e[8]
            data.nakamotoCoefs_wealth += e[9]
        else:
            data.nakamotoCoefs_wealth += e[8]


def curses_execute(keys: list):
    key = keys[0]

    if key == 'n' or key == 'N':
        amount = int(keys[1])
        execute_transition(amount)

    elif key == 'b' or key == 'B':
        amount = float(keys[1])
        for env in [pos_env, dpos_env, dpoqs_env]:
            env.setBondedAmount(amount)

    elif key == 's' or key == 'S':
        amount = float(keys[1])
        for env in [pos_env, dpos_env, dpoqs_env]:
            env.setStakingRatio(amount)

    elif key == 'v' or key == 'V':
        amount = float(keys[1])
        for env in [pos_env, dpos_env, dpoqs_env]:
            env.validate_cost = amount

    elif key == 'c' or key == 'C':
        amount = float(keys[1])
        for env in [dpos_env, dpoqs_env]:
            # no pos_env
            env.delegate_cost = amount

    elif key == 'p' or key == 'P':
        amount = float(keys[1])
        for env in [pos_env, dpos_env, dpoqs_env]:
            env.setStep(amount)

    elif key == 'k' or key == 'K':  # saveFigs
        dpi = 300
        if len(keys) == 3:
            dpi = int(keys[2])

        for (data, env_str) in zip([pos_data, dpos_data, dpoqs_data], ["pos", "dpos", "dpoqs"]):
            multi_draw_axis_3(
                keys[1] + "_" + env_str + "_state",  # name
                data.blockNumbers,  # x
                [data.bondedAmounts, data.totalSupplies],  # y1s
                data.inflations,  # y2
                data.stakingRatios,  # y3
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
                keys[1] + "_" + env_str + "_provs",  # name
                data.blockNumbers,  # x
                [data.inflations],  # y1s
                data.annualProvisions,  # y2
                data.blockProvisions,  # y3
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
                keys[1] + "_" + env_str + "_agents",  # name
                data.blockNumbers,  # x
                np.array(data.nodes).T,  # ys
                xlabel="blockNumbers",
                ylabel="amount",
                dpi=dpi,
                save=True
            )

            multi_draw(
                keys[1] + "_" + env_str + "_coef",  # name
                data.blockNumbers,  # x
                [data.nakamotoCoefs_powers, data.nakamotoCoefs_wealth] if env_str != "pos" else [data.nakamotoCoefs_wealth],  # ys
                xlabel="blockNumbers",
                ylabel="nakamotoCoef",
                legends=["powers", "wealth"] if env_str != "pos" else ["wealth"],
                dpi=dpi,
                save=True
            )

    elif key == 'l' or key == 'L':  # saveLogs
        for (data, env_str) in zip([pos_data, dpos_data, dpoqs_data], ["pos", "dpos", "dpoqs"]):
            multi_logs(
                keys[1] + "_" + env_str + "_state",  # name
                data.blockNumbers,  # x
                [
                    data.inflations,
                    data.stakingRatios,
                    data.bondedAmounts,
                    data.totalSupplies
                ],  # ys
                legends=[
                    "inflation",
                    "stakingRatio",
                    "bondedAmount",
                    "totalSupply"
                ]
            )

            multi_logs(
                keys[1] + "_" + env_str + "_provs",  # name
                data.blockNumbers,  # x
                [
                    data.inflations,
                    data.stakingRatios,
                    data.annualProvisions,
                    data.blockProvisions
                ],  # ys
                legends=[
                    "inflation",
                    "stakingRatio",
                    "annualProvision",
                    "blockProvision"
                ]
            )

            multi_logs(
                keys[1] + "_" + env_str + "_agents",  # name
                data.blockNumbers,  # x
                data.nodes,  # ys
                legends=["agent_" + str(i) for i in range(NUM_NODES)],
                transposed=False
            )

            # TODO: detailed agent history log through agent_step

            multi_logs(
                keys[1] + "_" + env_str + "_coef",  # name
                data.blockNumbers,  # x
                [data.nakamotoCoefs_powers, data.nakamotoCoefs_wealth] if env_str != "pos" else [data.nakamotoCoefs_wealth],  # ys
                legends=["powers", "wealth"] if env_str != "pos" else ["wealth"]
            )


def curses_main():
    r = 0  # 0~2
    e = 0  # 0: PoS, 1: DPoS, 2: DPoQS

    while True:
        stdscr.clear()

        curses_status(r, e)()

        # commands
        x = 0; y = COMMAND_Y_LOCATION
        stdscr.addstr(y, 0, MSG_DOUBLE_SPLIT_LINE); y += 1
        stdscr.addstr(y, 0, ""); y += 1
        curses_command("[H]", description="help", prefix="")
        curses_command("[Q]", description="quit", prefix="    ")
        curses_command("[<]", description="prev_status", prefix="    ")
        curses_command("[>]", description="next_status", prefix="    ")
        stdscr.addstr(y, 0, ""); y += 1
        curses_command("[{]", description="prev_env", prefix="")
        curses_command("[}]", description="next_env", prefix="    ")

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

        elif i == '[' or i == '{':
            e = max(e - 1, 0)
            # r = 0
        elif i == ']' or i == '}':
            e = min(e + 1, 2)
            # r = 0


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
