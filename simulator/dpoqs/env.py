import numpy as np
from random import randint
from typing import List
from math import sqrt

try:
    from .agent import *
except(ImportError):
    from agent import *


LIMIT_NUM_VALIDATORS = 21


class DpoqsEnv:
    def __init__(
        self,
        numNodes: int,
        bondedRatio: float,
        stakingRatio: float,
        Inflation: float,
        TotalSupply: float,
        GoalBonded: float = None,
        BlocksPerYr: float = None,
        InflationRateChange: float = None,
        InflationMax: float = None,
        InflationMin: float = None,
        nodes: List[DpoqsAgent] = None,
        commission_fee: float = 0.05,
        validate_cost: float = 0.,
        delegate_cost: float = 0.,
        step: int = 52596
    ):
        # https://docs.cosmos.network/v0.46/modules/mint/03_begin_block.html

        # init & changable
        self.bondedAmount = bondedRatio * TotalSupply
        self.stakingRatio = stakingRatio

        self.numNodes = numNodes
        self._commission_fee = commission_fee
        self._validate_cost = validate_cost
        self._delegate_cost = delegate_cost

        if nodes is not None:
            self._nodes = nodes
        else:
            init_is_validators, init_wealthes = self._init_dist_nodes(self.numNodes, self.bondedAmount)
            self._nodes: List[DpoqsAgent] = list()
            for init_is_validator, init_wealth in zip(init_is_validators, init_wealthes):
                self._nodes.append(
                    DpoqsAgent(
                        is_validator=init_is_validator,
                        wealth=init_wealth,
                        commission_fee=self.commission_fee,
                        validate_cost=self.validate_cost,
                        delegate_cost=self.delegate_cost
                    )
                )  # TODO: commission fee & cost dist.
            self._init_delegate_nodes()

        # state
        self.Inflation = Inflation  # (%)
        self.TotalSupply = TotalSupply
        self.blockNumber = 0

        # pre-defined
        self.GoalBonded = GoalBonded or 0.67  # (%)
        self.BlocksPerYr = BlocksPerYr or 6311520  # 365.25 days * 24 hours * 60 minutes * 60 seconds / 5 second
        self.InflationRateChange = InflationRateChange or 0.13  # (%)
        self.InflationMax = InflationMax or 0.20  # (%)
        self.InflationMin = InflationMin or 0.07  # (%)

        # options
        self.step = step

    """Nodes"""

    def _init_dist_nodes(self, size, amount, alpha=1.16, lower=1., upper=None):
        s = np.random.pareto(alpha, size) + lower
        if upper != None:
            s = s[s < upper]  # kill outliers
        s /= sum(s)
        s *= amount
        _wealthes = np.sort(s)[::-1]  # TODO: floating errors

        _is_validators = [True if i < LIMIT_NUM_VALIDATORS else False for i in range(self.numNodes)]

        return _is_validators, _wealthes

    def _init_delegate_nodes(self):
        for i in range(LIMIT_NUM_VALIDATORS, self.numNodes):
            delegate(
                self._nodes[i],
                self._nodes[randint(0, LIMIT_NUM_VALIDATORS - 1)],
                self._nodes[i].wealth
            )

    @property
    def relationship(self):
        _r_delegatedes = list()
        for i in range(self.numNodes):
            if self._nodes[i].is_validator:
                _r_delegatedes.append(self._nodes[i].delegatedes)
        return _r_delegatedes

    @property
    def nodes(self):
        return [self._nodes[i].wealth for i in range(self.numNodes)]

    @property
    def validators_wealth(self) -> (np.array):
        _validators = list()
        for i in range(self.numNodes):
            if self._nodes[i].is_validator:
                _validators.append(self._nodes[i].wealth)
        return np.array(_validators)

    @property
    def validators_sqrt_wealth(self) -> (np.array):
        _validators = list()
        for i in range(self.numNodes):
            if self._nodes[i].is_validator:
                _validators.append(sqrt(self._nodes[i].wealth))
        return np.array(_validators)

    @property
    def validators_powers(self) -> (np.array):
        _power = list()
        for i in range(self.numNodes):
            if self._nodes[i].is_validator:
                _power.append(self._nodes[i].power)
        return np.array(_power)

    # def add_validator(self):
    #     pass

    # def remove_validator(self):
    #     pass

    @property
    def commission_fee(self):
        return self._commission_fee

    @commission_fee.setter
    def commission_fee(self, new_commission_fee):
        self._commission_fee = new_commission_fee
        for i in range(self._nodes):
            self._nodes[i].commission_fee = new_commission_fee

    @property
    def validate_cost(self):
        return self._validate_cost

    @validate_cost.setter
    def validate_cost(self, new_validate_cost):
        self._validate_cost = new_validate_cost
        for i in range(self._nodes):
            self._nodes[i].validate_cost = new_validate_cost

    @property
    def delegate_cost(self):
        return self._delegate_cost

    @delegate_cost.setter
    def delegate_cost(self, new_delegate_cost):
        self._delegate_cost = new_delegate_cost
        for i in range(self._nodes):
            self._nodes[i].delegate_cost = new_delegate_cost

    """Env"""

    def setBondedAmount(self, _newBondedAmount: float):
        # TODO: setter
        self.bondedAmount = _newBondedAmount

    def setStakingRatio(self, _newStakingRatio: float):
        # TODO: setter
        self.stakingRatio = _newStakingRatio

    def setStep(self, _newStep: int):
        # TODO: setter
        self.step = _newStep

    """Transition"""

    @property
    def bondedRatio(self) -> (float):
        return self.bondedAmount / self.TotalSupply

    @property
    def NextInflationRate(self) -> (float):
        # The target annual inflation rate is recalculated each block.
        # The inflation is also subject to a rate change (positive or negative)
        # depending on the distance from the desired ratio (67%).
        # The maximum rate change possible is defined to be 13% per year,
        # however the annual inflation is capped as between 7% and 20%.
        inflationRateChangePerYear = (1 - self.bondedRatio / self.GoalBonded) * self.InflationRateChange
        inflationRateChange = inflationRateChangePerYear / self.BlocksPerYr

        # increase the new annual inflation for this next cycle
        inflation = self.Inflation + inflationRateChange
        if inflation > self.InflationMax:
            inflation = self.InflationMax

        if inflation < self.InflationMin:
            inflation = self.InflationMin

        return inflation

    @property
    def NextAnnualProvision(self) -> (float):
        # NextAnnualProvisions
        # Calculate the annual provisions based on current total supply and inflation rate.
        # This parameter is calculated once per block.
        return self.Inflation * self.TotalSupply

    @property
    def BlockProvision(self) -> (float):
        # BlockProvision
        # Calculate the provisions generated for each block based on current annual provisions.
        return self.NextAnnualProvision / self.BlocksPerYr

    def _distribute_rewards(self, validator_rewards: np.array):
        j = 0
        for i in range(self.numNodes):
            if self._nodes[i].is_validator:
                _total_amount = validator_rewards[j]; j += 1
                _fee = _total_amount * self._nodes[i].commission_fee

                _dist: np.array =\
                    np.array([self._nodes[i].wealth] + self._nodes[i].delegatedes) /\
                    (self._nodes[i].wealth + self._nodes[i].total_delegated) *\
                    (_total_amount * (1. - self._nodes[i].commission_fee))  # TODO: floating errors

                # my delegation
                self._nodes[i].wealth += _fee
                self._nodes[i].wealth += _dist[0]
                self._nodes[i].wealth -= self._nodes[i].validate_cost

                # delegators
                self._nodes[i].delegatedes += _dist[1:]  # amount
                for d, e in enumerate(self._nodes[i]._delegatedes):
                    e._from.wealth += _dist[d + 1]  # real wealth
                    e._from.wealth -= e._from.delegate_cost

    def _mint_powers(self, amount):
        ratio = self.validators_powers / sum(self.validators_powers)
        return ratio * amount  # TODO: floating errors

    def transition(self, blocks: int):
        if blocks == 0:
            return (
                [self.bondedAmount],
                [self.stakingRatio],
                [self.Inflation],
                [self.TotalSupply],
                [self.blockNumber],
                [self.NextAnnualProvision],
                [self.BlockProvision],
                [self.nodes],
                [self.nakamoto_coefficient_powers],
                [self.nakamoto_coefficient_wealth]
            )

        bondedAmounts = list()
        stakingRatios = list()
        inflations = list()
        totalSupplies = list()
        blockNumbers = list()
        annualProvisions = list()
        blockProvisions = list()
        nodes = list()
        nakamotoCoef_power = list()
        nakamotoCoef_validator = list()

        for _ in range(blocks):
            inflation = self.NextInflationRate
            annualProvision = self.NextAnnualProvision
            blockProvision = self.BlockProvision

            # transition
            self.Inflation = inflation
            _stakingAmount = blockProvision * self.stakingRatio  # TODO: each
            self.bondedAmount += _stakingAmount
            self.TotalSupply += blockProvision
            self.blockNumber += 1
            self._distribute_rewards(np.array(self._mint_powers(_stakingAmount)))

            # log
            if self.blockNumber % self.step == 0:
                e = self.status()
                bondedAmounts.append(e[0])
                stakingRatios.append(e[1])
                inflations.append(e[2])
                totalSupplies.append(e[3])
                blockNumbers.append(e[4])

                annualProvisions.append(annualProvision)
                blockProvisions.append(blockProvision)

                nodes.append(e[5])
                nakamotoCoef_power.append(e[6])
                nakamotoCoef_validator.append(e[7])

        return (
            bondedAmounts,
            stakingRatios,
            inflations,
            totalSupplies,
            blockNumbers,
            annualProvisions,
            blockProvisions,
            nodes,
            nakamotoCoef_power,
            nakamotoCoef_validator
        )

    def status(self):
        return (
            self.bondedAmount,
            self.stakingRatio,
            self.Inflation,
            self.TotalSupply,
            self.blockNumber,

            self.nodes,
            self.nakamoto_coefficient_powers,
            self.nakamoto_coefficient_wealth
        )

    """Fairness & Decentralization"""

    @property
    def nakamoto_coefficient_powers(self):
        # maybe same
        _bonded_sqrt_amount = sum(self.validators_powers)
        sorted_powers = np.sort(self.validators_powers)[::-1]
        for i in range(1, len(sorted_powers) + 1):
            # print(i, sum(sorted_powers[:i]))
            if sum(sorted_powers[:i]) > (_bonded_sqrt_amount / 3):
                return i
        return self.numNodes

    # @property
    # def (self):

    @property
    def nakamoto_coefficient_wealth(self):
        # maybe slightly decrease
        _bonded_sqrt_amount = sum(self.validators_powers)
        sorted_validators = np.sort(self.validators_sqrt_wealth)[::-1]
        for i in range(1, len(sorted_validators) + 1):
            # print(i, sum(sorted_validators[:i]))
            if sum(sorted_validators[:i]) > (_bonded_sqrt_amount / 3):
                return i
        return self.numNodes


if __name__ == "__main__":
    env = DpoqsEnv(
        50,  # numNodes
        0.5,  # bondedRatio
        0.6,  # stakingRatio
        0.1,  # Inflation
        1000000000,  # TotalSupply
        validate_cost=0.3,  # validate_cost
        delegate_cost=0.01  # delegate_cost
    )

    print("")
    print("nakamoto_coef_powers:\t", env.nakamoto_coefficient_powers)
    print("nakamoto_coef_wealth:\t", env.nakamoto_coefficient_wealth)
    print("powers:\t\t\t", sum(env.validators_powers))
    print("wealth:\t\t\t", sum(env.validators_wealth))

    print("")
    print("Reward Distribution", end='\r')
    env._distribute_rewards(
        np.array([100000000 for _ in range(len(env.validators_wealth))])
    )  # test purpose
    print(" " * 30, end='\r')
    print("Transition 400000", end='\r')
    env.transition(400000)
    print(" " * 30, end='\r')

    print("nakamoto_coef_powers:\t", env.nakamoto_coefficient_powers)
    print("nakamoto_coef_wealth:\t", env.nakamoto_coefficient_wealth)
    print("powers:\t\t\t", sum(env.validators_powers))
    print("wealth:\t\t\t", sum(env.validators_wealth))
