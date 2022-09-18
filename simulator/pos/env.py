from wsgiref.validate import validator
import numpy as np

from agent import *


class PosEnv:
    def __init__(
        self,
        numValidators: int,
        bondedRatio: float,
        stakingRatio: float,
        Inflation: float,
        TotalSupply: float,
        GoalBonded: float = None,
        BlocksPerYr: float = None,
        InflationRateChange: float = None,
        InflationMax: float = None,
        InflationMin: float = None,
        cost: float = 0.,
        step: int = 52596
    ):
        # agent_step: int = 5000  # TODO

        # https://docs.cosmos.network/v0.46/modules/mint/03_begin_block.html

        # init & changable
        self.bondedAmount = bondedRatio * TotalSupply
        self.stakingRatio = stakingRatio

        self.numValidators = numValidators
        init_wealthes = self._dist_validators(numValidators, self.bondedAmount)
        self._agents = list()
        for init_wealth in init_wealthes:
            self._agents.append(AgentPos(wealth=init_wealth, cost=cost))  # TODO: cost dist.
        self._cost = cost

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

    """Validators"""

    def _dist_validators(self, size, amount, alpha=1.16, lower=1., upper=None):
        s = np.random.pareto(alpha, size) + lower
        if upper != None:
            s = s[s < upper]  # kill outliers
        s /= sum(s)
        s *= amount
        return np.sort(s)[::-1]  # TODO: floating errors

    @property
    def validators(self) -> (np.array):
        return np.array([self._agents[i].wealth for i in range(self.numValidators)])

    @validators.setter
    def validators(self, newValidators: np.array):
        for i in range(self.numValidators):
            self._agents[i].wealth = newValidators[i] - self._agents[i].cost

    # def add_validator(self):
    #     pass

    # def remove_validator(self):
    #     pass

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, new_cost):
        self._cost = new_cost
        for i in range(self.numValidators):
            self._agents[i].cost = new_cost

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

    def _mint_validators(self, amount):
        ratio = self.validators / sum(self.validators)
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
                [self.validators],
                [self.nakamoto_coefficient]
            )

        bondedAmounts = list()
        stakingRatios = list()
        inflations = list()
        totalSupplies = list()
        blockNumbers = list()
        annualProvisions = list()
        blockProvisions = list()
        validators = list()
        nakamotoCoef = list()

        for b in range(blocks):
            inflation = self.NextInflationRate
            annualProvision = self.NextAnnualProvision
            blockProvision = self.BlockProvision

            # transition
            self.Inflation = inflation
            _stakingAmount = blockProvision * self.stakingRatio
            self.bondedAmount += _stakingAmount
            self.TotalSupply += blockProvision
            self.blockNumber += 1
            self.validators += self._mint_validators(_stakingAmount)

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

                validators.append(e[5])
                nakamotoCoef.append(e[6])
        return (
            bondedAmounts,
            stakingRatios,
            inflations,
            totalSupplies,
            blockNumbers,
            annualProvisions,
            blockProvisions,
            validators,
            nakamotoCoef
        )

    def status(self):
        return (
            self.bondedAmount,
            self.stakingRatio,
            self.Inflation,
            self.TotalSupply,
            self.blockNumber,

            self.validators,
            self.nakamoto_coefficient
        )

    """Fairness & Decentralization"""

    @property
    def nakamoto_coefficient(self):
        sorted_validators = np.sort(self.validators)[::-1]
        for i in range(1, len(sorted_validators) + 1):
            # print(i, sum(sorted_validators[:i]))
            if sum(sorted_validators[:i]) > (self.bondedAmount / 3):
                return i

    # @property
    # def (self):


if __name__ == "__main__":
    env = PosEnv(
        10,  # numValidators
        0.5,  # bondedRatio
        0.6,  # stakingRatio
        0.1,  # Inflation
        1000000000,  # TotalSupply
        cost=0.3
    )

    # print(env.validators)
    print(sum(env.validators))
    print(env.TotalSupply)
    print(env.bondedAmount)
    print(env.nakamoto_coefficient)

    env.transition(400000)
    print("")

    # print(env.validators)
    print(sum(env.validators))
    print(env.TotalSupply)
    print(env.bondedAmount)
    print(env.nakamoto_coefficient)
