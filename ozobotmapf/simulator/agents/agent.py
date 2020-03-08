class Agent:
    def __init__(self, agent_id, raw_plans, ozomap):
        self.id = agent_id
        self.positions = raw_plans['pos_list']
        self.steps = raw_plans['steps']
        self.ozomap = ozomap

        self.active_path = set()
        self.direction_arrow = None  # TODO: find arrow

    def update(self):
        pass

    def get_active_path(self):
        return self.active_path
