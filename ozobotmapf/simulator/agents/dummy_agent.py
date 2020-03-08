from ozobotmapf.simulator.agents.agent import Agent


class DummyAgent(Agent):
    def __init__(self, agent_id, raw_plans, ozomap):
        super().__init__(agent_id, raw_plans, ozomap)

    def update(self):
        pass
