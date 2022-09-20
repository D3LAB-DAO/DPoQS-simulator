from typing import List
from math import sqrt


class WeightedEdge:
    def __init__(
        self,
        from_,
        to_,
        amount_: float
    ):
        if from_ == to_:
            raise ValueError

        self._from = from_
        self._to = to_
        self.amount = amount_


class DpoqsAgent:
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

    """delegates"""

    def is_delegate(self, to_):
        for e in self._delegates:
            if (e._from == self) and (e._to == to_) and (e.amount != 0):
                return e
        return None

    def get_delegates(self, option: str = "amount"):
        if option == "amount":
            return [e.amount for e in self._delegates]
        elif option == "from":
            return [e._from for e in self._delegates]
        elif option == "to":
            return [e._to for e in self._delegates]

    @property
    def delegates(self):
        return [e.amount for e in self._delegates]

    @delegates.setter
    def delegates(self, new_delegates):
        for i in range(len(self._delegates)):
            self._delegates[i].amount = new_delegates[i]

    """delegatedes"""

    def is_delegated(self, from_):
        for e in self._delegatedes:
            if (e._from == from_) and (e._to == self) and (e.amount != 0):
                return e
        return None

    def get_delegatedes(self, option: str = "amount"):
        if option == "amount":
            return [e.amount for e in self._delegatedes]
        elif option == "from":
            return [e._from for e in self._delegatedes]
        elif option == "to":
            return [e._to for e in self._delegatedes]

    @property
    def delegatedes(self, option: str = "amount"):
        return [e.amount for e in self._delegatedes]

    @delegatedes.setter
    def delegatedes(self, new_delegatedes):
        for i in range(len(self._delegatedes)):
            self._delegatedes[i].amount = new_delegatedes[i]

    """total"""

    @property
    def total_delegate(self) -> (float):
        r = 0.
        for e in self._delegates:
            r += e.amount
        return r

    @property
    def total_sqrt_delegate(self) -> (float):
        r = 0.
        for e in self._delegates:
            r += sqrt(e.amount)
        return r

    @property
    def total_delegated(self) -> (float):
        r = 0.
        for e in self._delegatedes:
            r += e.amount
        return r

    @property
    def total_sqrt_delegated(self) -> (float):
        r = 0.
        for e in self._delegatedes:
            r += sqrt(e.amount)
        return r

    """power"""

    @property
    def power(self) -> (float):
        # Quadratic Funding
        if not self.is_validator:
            return 0
        else:
            return sqrt(self.wealth - self.total_delegate) + self.total_sqrt_delegated


def delegate(from_: DpoqsAgent, to_: DpoqsAgent, amount_: float):
    if from_ == to_:
        raise ValueError

    e = WeightedEdge(from_, to_, amount_)

    if amount_ > (from_.wealth - from_.total_delegate):
        raise ValueError

    if (from_.is_delegate(to_) != None) and (from_.is_delegate(to_) == to_.is_delegated(from_)):
        # and (to_.is_delegated(from_) != None)
        # exist
        from_.is_delegate(to_).amount += amount_
    else:
        # new
        from_._delegates.append(e)
        to_._delegatedes.append(e)

    if from_.total_delegate > from_.wealth:
        raise ValueError


# for AI agents
# def undelegate():
#     pass


if __name__ == "__main__":
    agent_1 = DpoqsAgent(wealth=100.)
    agent_2 = DpoqsAgent(wealth=400.)

    print("===")
    print(agent_2.is_delegate(agent_1) != None)
    print(agent_1.wealth, agent_1.total_delegate, agent_1.total_delegated, agent_1.power)
    print(agent_2.wealth, agent_2.total_delegate, agent_2.total_delegated, agent_2.power)
    print(agent_1.delegates, agent_2.delegates)
    print(agent_1.delegatedes, agent_2.delegatedes)

    delegate(agent_2, agent_1, 200.)
    print("===")
    print(agent_2.is_delegate(agent_1) != None)
    print(agent_1.wealth, agent_1.total_delegate, agent_1.total_delegated, agent_1.power)
    print(agent_2.wealth, agent_2.total_delegate, agent_2.total_delegated, agent_2.power)
    print(agent_1.delegates, agent_2.delegates)
    print(agent_1.delegatedes, agent_2.delegatedes)

    delegate(agent_2, agent_1, 100.)
    print("===")
    print(agent_2.is_delegate(agent_1) != None)
    print(agent_1.wealth, agent_1.total_delegate, agent_1.total_delegated, agent_1.power)
    print(agent_2.wealth, agent_2.total_delegate, agent_2.total_delegated, agent_2.power)
    print(agent_1.delegates, agent_2.delegates)
    print(agent_1.delegatedes, agent_2.delegatedes)

    # ValueError
    try:
        delegate(agent_2, agent_1, 2000.)
        print("===")
        print(agent_2.is_delegate(agent_1) != None)
        print(agent_1.wealth, agent_1.total_delegate, agent_1.total_delegated, agent_1.power)
        print(agent_2.wealth, agent_2.total_delegate, agent_2.total_delegated, agent_2.power)
        print(agent_1.delegates, agent_2.delegates)
        print(agent_1.delegatedes, agent_2.delegatedes)
    except (ValueError):
        print("===")
        print(agent_2.is_delegate(agent_1) != None)
        print("ValueError!")
