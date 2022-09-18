class AgentPos:
    def __init__(
        self,
        wealth: float = 0.,
        cost: float = 0.
    ):
        self.wealth = wealth
        self.cost = cost


if __name__ == "__main__":
    agent = AgentPos(100.)

    print(agent.wealth)

    for i in range(100):
        agent.wealth = i

    print(agent.wealth)
