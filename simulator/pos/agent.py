class AgentPos:
    def __init__(
        self,
        wealth: float = 0.,
        cost: float = 0.,
        step: int = 5000
    ):
        self._wealth = wealth
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
        self._wealth -= self._cost

        if self._round % self._step == 0:
            self._history.append(amount)

    @property
    def history(self):
        return self._history

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, new_step):
        self._step = new_step

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, new_cost):
        self._cost = new_cost


if __name__ == "__main__":
    agent = AgentPos(100.)

    print(agent.wealth)
    print(agent.history)

    for i in range(100):
        agent.wealth = i

    print(agent.wealth)
    print(agent.history)
