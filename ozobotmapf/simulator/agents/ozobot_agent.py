from ozobotmapf.simulator.agents.agent import Agent


class OzobotAgent(Agent):
    def __init__(self, agent_id, raw_plans, ozomap, config):
        super().__init__(agent_id, raw_plans, ozomap, config)
