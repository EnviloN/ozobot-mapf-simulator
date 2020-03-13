from ozobotmapf.simulator.agents.agent import Agent
from ozobotmapf.graphics.drawables import Line


class DummyAgent(Agent):
    """
    This agent implementation is displaying it's whole path (plan) during each update.
    """
    def __init__(self, agent_id, raw_plans, ozomap, config):
        super().__init__(agent_id, raw_plans, ozomap, config)

    def update_path(self, time):
        self.active_path.clear()
        for i in range(1, len(self.positions)):
            start = self.positions[i-1].get_middle()
            end = self.positions[i].get_middle()
            self.active_path.add_drawable(Line(start, end, self.config.line_width))
