from typing import List


class WeightedEdge:
    def __init__(
        self,
        from_: int,
        to_: int,
        amount_: float
    ):
        if from_ == to_:
            raise ValueError

        self._from = from_
        self._to = to_
        self.amount = amount_


class DposAgent:
    def __init__(
        self,
        is_validator: bool = True,
        wealth: float = 0.,
        delegates: List[WeightedEdge] = None,
        delegatedes: List[WeightedEdge] = None,
        commission_fee: float = 0.05,
        validate_cost: float = 0.,
        delegate_cost: float = 0.
    ):
        self.is_validator = is_validator  # True if validator, False if delegator
        self.commission_fee = commission_fee

        self.wealth = wealth
        self._delegates: List[WeightedEdge] = delegates or list()
        self._delegatedes: List[WeightedEdge] = delegatedes or list()

        self.validate_cost = validate_cost
        self.delegate_cost = delegate_cost

    @property
    def delegates(self):
        return [e.amount for e in self._delegates]

    @delegates.setter
    def delegates(self, new_delegates):
        for i in range(len(self._delegates)):
            self._delegates[i].amount = new_delegates[i]

    @property
    def delegatedes(self):
        return [e.amount for e in self._delegatedes]

    @delegatedes.setter
    def delegatedes(self, new_delegatedes):
        for i in range(len(self._delegatedes)):
            self._delegatedes[i].amount = new_delegatedes[i]

    @property
    def total_delegate(self) -> (float):
        r = 0.
        for e in self._delegates:
            r += e.amount
        return r

    @property
    def total_delegated(self) -> (float):
        r = 0.
        for e in self._delegatedes:
            r += e.amount
        return r

    @property
    def power(self) -> (float):
        return 0 if not self.is_validator else self.wealth - self.total_delegate + self.total_delegated


def delegate(from_: DposAgent, to_: DposAgent, amount_: float):
    if from_ == to_:
        raise ValueError

    e = WeightedEdge(from_, to_, amount_)

    if amount_ > (from_.wealth - from_.total_delegate):
        raise ValueError

    from_._delegates.append(e)

    if from_.total_delegate > from_.wealth:
        raise ValueError

    to_._delegatedes.append(e)


# for AI agents
# def undelegate():
#     pass


if __name__ == "__main__":
    agent_1 = DposAgent(wealth=100.)
    agent_2 = DposAgent(wealth=400.)
    print("===")
    print(agent_1.wealth, agent_1.total_delegate, agent_1.total_delegated, agent_1.power)
    print(agent_2.wealth, agent_2.total_delegate, agent_2.total_delegated, agent_2.power)

    delegate(agent_2, agent_1, 200.)
    print("===")
    print(agent_1.wealth, agent_1.total_delegate, agent_1.total_delegated, agent_1.power)
    print(agent_2.wealth, agent_2.total_delegate, agent_2.total_delegated, agent_2.power)

    delegate(agent_2, agent_1, 100.)
    print("===")
    print(agent_1.wealth, agent_1.total_delegate, agent_1.total_delegated, agent_1.power)
    print(agent_2.wealth, agent_2.total_delegate, agent_2.total_delegated, agent_2.power)

    # ValueError
    try:
        delegate(agent_2, agent_1, 2000.)
        print("===")
        print(agent_1.wealth, agent_1.total_delegate, agent_1.total_delegated, agent_1.power)
        print(agent_2.wealth, agent_2.total_delegate, agent_2.total_delegated, agent_2.power)
    except (ValueError):
        print("===")
        print("ValueError!")
