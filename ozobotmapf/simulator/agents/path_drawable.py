from ozobotmapf.utils.constants import Colors


class PathDrawable:
    def __init__(self, drawable, time, duration):
        self.drawable = drawable
        self.valid_until = time + duration

    def is_valid(self, time):
        return True if time <= self.valid_until else False


class UTurnCode(PathDrawable):
    def __init__(self, drawable, time, duration):
        super().__init__(drawable, time, duration)
        self.last_switch = time
        self.next_switch = time + 45
        self.current_color = 0
        self.colors = [Colors.RED, Colors.YELLOW, Colors.CYAN, Colors.YELLOW]
        self.drawable.color = self.colors[self.current_color]

    def is_valid(self, time):
        if time >= self.next_switch:
            self.last_switch = self.next_switch
            self.next_switch = self.next_switch + 45
            self.current_color += 1
            self.drawable.color = self.colors[self.current_color % 4]

        return True if time <= self.valid_until else False
