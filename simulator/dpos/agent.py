class AgentDpos:
    # global class_id
    # class_id = 0

    def __init__(
        self,
        is_validator: bool,
        wealth: float = 0.,
        cost: float = 0.,
        step: int = 10
    ):
        # self._id = AgentDpos.class_id; AgentDpos.class_id += 1

        self.is_validator = is_validator  # True for Validator, False for Delegator

        self._wealth = wealth
        self._delegated = 0.
        self._history = [wealth]
        self._cost = cost

        self._round = 0
        self._step = step

    @property
    def wealth(self):
        return self._wealth

    @wealth.setter
    def wealth(self, amount):
        self._round += 1

        self._wealth = amount

        if self._round % self._step == 0:
            self._history.append(amount)

    @wealth.setter
    def wealth_cost(self, amount):
        self._round += 1

        self._wealth = amount
        if self.is_validator:
            self._wealth -= self._cost
        else:
            pass  # delegator has no cost

        if self._round % self._step == 0:
            self._history.append(amount)

    @property
    def delegated(self):
        return self._delegated

    @wealth.setter
    def wealth(self, amount):
        self._round += 1

        self._wealth = amount

        if self._round % self._step == 0:
            self._history.append(amount)

    @property
    def wealth_and_delegated(self):
        return self._wealth + self._delegated

    @property
    def history(self):
        return self._history

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, new_step):
        self._step = new_step

    def delegate(self, to_):
        # delegate all amount
        self.wealth


if __name__ == "__main__":
    agent = AgentDpos(100., is_validator=True)

    print(agent.wealth)
    print(agent.history)

    for i in range(100):
        agent.wealth = i

    print(agent.wealth)
    print(agent.history)
