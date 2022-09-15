from re import L
import numpy as np


class Env:
    def __init__(
        self,
        _numValidator: int,
        _bondedRatio: float,
        _stakingRatio: float,
        _Inflation: float,
        _TotalSupply: float,
        _GoalBonded: float = None,
        _BlocksPerYr: float = None,
        _InflationRateChange: float = None,
        _InflationMax: float = None,
        _InflationMin: float = None,
        step: int = 52596
    ):
        # https://docs.cosmos.network/v0.46/modules/mint/03_begin_block.html

        # init & changable
        self.bondedAmount = _bondedRatio * _TotalSupply
        self.stakingRatio = _stakingRatio
        self.validators = self._dist_validators(_numValidator, self.bondedAmount)

        # state
        self.Inflation = _Inflation  # (%)
        self.TotalSupply = _TotalSupply
        self.blockNumber = 0

        # pre-defined
        self.GoalBonded = _GoalBonded or 0.67  # (%)
        self.BlocksPerYr = _BlocksPerYr or 6311520  # 365.25 days * 24 hours * 60 minutes * 60 seconds / 5 second
        self.InflationRateChange = _InflationRateChange or 0.13  # (%)
        self.InflationMax = _InflationMax or 0.20  # (%)
        self.InflationMin = _InflationMin or 0.07  # (%)

        # options
        self.step = step

    def _dist_validators(self, size, amount, alpha=1.16, lower=1., upper=None):
        s = np.random.pareto(alpha, size) + lower
        if upper != None:
            s = s[s < upper]  # kill outliers
        s /= sum(s)
        s *= amount
        return s  # TODO: floating errors

    def setBondedAmount(self, _newBondedAmount: float):
        self.bondedAmount = _newBondedAmount

    def setStakingRatio(self, _newStakingRatio: float):
        self.stakingRatio = _newStakingRatio

    def setStep(self, _newStep: int):
        self.step = _newStep

    def bondedRatio(self) -> (float):
        return self.bondedAmount / self.TotalSupply

    def NextInflationRate(self) -> (float):
        # The target annual inflation rate is recalculated each block.
        # The inflation is also subject to a rate change (positive or negative)
        # depending on the distance from the desired ratio (67%).
        # The maximum rate change possible is defined to be 13% per year,
        # however the annual inflation is capped as between 7% and 20%.
        inflationRateChangePerYear = (1 - self.bondedRatio() / self.GoalBonded) * self.InflationRateChange
        inflationRateChange = inflationRateChangePerYear / self.BlocksPerYr

        # increase the new annual inflation for this next cycle
        inflation = self.Inflation + inflationRateChange
        if inflation > self.InflationMax:
            inflation = self.InflationMax

        if inflation < self.InflationMin:
            inflation = self.InflationMin

        return inflation

    def NextAnnualProvision(self) -> (float):
        # NextAnnualProvisions
        # Calculate the annual provisions based on current total supply and inflation rate.
        # This parameter is calculated once per block.
        return self.Inflation * self.TotalSupply

    def BlockProvision(self) -> (float):
        # BlockProvision
        # Calculate the provisions generated for each block based on current annual provisions.
        return self.NextAnnualProvision() / self.BlocksPerYr

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
                [self.validators]
                [self.NextAnnualProvision()],
                [self.BlockProvision()],
            )

        bondedAmounts = list()
        stakingRatios = list()
        inflations = list()
        totalSupplies = list()
        blockNumbers = list()
        validators = list()
        annualProvisions = list()
        blockProvisions = list()

        for b in range(blocks):
            inflation = self.NextInflationRate()
            annualProvision = self.NextAnnualProvision()
            blockProvision = self.BlockProvision()

            # transition
            self.Inflation = inflation

            stakingAmount = blockProvision * self.stakingRatio
            self.bondedAmount += stakingAmount
            self.validators += self._mint_validators(stakingAmount)

            self.TotalSupply += blockProvision
            self.blockNumber += 1

            # log
            if self.blockNumber % self.step == 0:
                e = self.status()
                bondedAmounts.append(e[0])
                stakingRatios.append(e[1])
                inflations.append(e[2])
                totalSupplies.append(e[3])
                blockNumbers.append(e[4])
                validators.append(e[5])

                annualProvisions.append(annualProvision)
                blockProvisions.append(blockProvision)

        return (
            bondedAmounts,
            stakingRatios,
            inflations,
            totalSupplies,
            blockNumbers,
            validators,
            annualProvisions,
            blockProvisions
        )

    def status(self):
        return (
            self.bondedAmount,
            self.stakingRatio,
            self.Inflation,
            self.TotalSupply,
            self.blockNumber,
            self.validators
        )

    def fairness(self):
        pass


if __name__ == "__main__":
    env = Env(
        10,  # _numValidator
        0.5,  # _bondedRatio
        0.6,  # _stakingRatio
        0.1,  # _Inflation
        1000000000  # _TotalSupply
    )

    print(env.validators)
    print(sum(env.validators))
    print(env.TotalSupply)
    print(env.bondedAmount)

    env.transition(1000000)

    print("\n")
    print(env.validators)
    print(sum(env.validators))
    print(env.TotalSupply)
    print(env.bondedAmount)
