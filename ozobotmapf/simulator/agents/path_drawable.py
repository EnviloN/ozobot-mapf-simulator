from ozobotmapf.utils.constants import Colors


class PathDrawable:
    def __init__(self, drawable, time, duration):
        self.drawable = drawable
        self.valid_until = time + duration

    def is_valid(self, time):
        return True if time <= self.valid_until else False

    def update(self, time):
        pass


class PathSegment(PathDrawable):
    def __init__(self, drawable, time, duration, is_colored):
        super().__init__(drawable, time, duration)
        self.is_colored = is_colored
        colored_time = duration / 3
        self.color_times = [time + colored_time, time + 2*colored_time, time + 3*colored_time]
        self.colors = [Colors.BLUE, Colors.BLACK, Colors.RED]
        if self.is_colored:
            self.drawable.color = self.colors[0]

    def update(self, time):
        if self.is_colored:
            if time <= self.color_times[0]:
                self.drawable.color = self.colors[0]
            elif time <= self.color_times[1]:
                self.drawable.color = self.colors[1]
            else:
                self.drawable.color = self.colors[2]


class TurnSegment(PathDrawable):
    def __init__(self, drawable, time, duration, is_colored):
        super().__init__(drawable, time, duration)
        self.is_colored = is_colored
        if self.is_colored:
            self.drawable.color = Colors.BLUE

    def update(self, time):
        pass


class UTurnCode(PathDrawable):
    def __init__(self, drawable, time, duration):
        super().__init__(drawable, time, duration)
        self.last_switch = time
        self.next_switch = time + 45
        self.current_color = 0
        self.colors = [Colors.RED, Colors.YELLOW, Colors.CYAN, Colors.YELLOW]
        self.drawable.color = self.colors[self.current_color]

    def update(self, time):
        if time >= self.next_switch:
            self.last_switch = self.next_switch
            self.next_switch = self.next_switch + 45
            self.current_color += 1
            self.drawable.color = self.colors[self.current_color % 4]
