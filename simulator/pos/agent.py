class PosAgent:
    def __init__(
        self,
        wealth: float = 0.,
        validate_cost: float = 0.
    ):
        self.wealth = wealth
        self.validate_cost = validate_cost


if __name__ == "__main__":
    agent = PosAgent(100.)

    print(agent.wealth)

    for i in range(100):
        agent.wealth = i

    print(agent.wealth)
