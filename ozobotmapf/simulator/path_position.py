from ozobotmapf.utils.constants import Directions


class PathPosition:
    def __init__(self, time, max_time):
        if time < 0:
            self.time = 0
        elif time > max_time:
            self.time = max_time
        else:
            self.time = time

        self.prev_t, self.curr_t, self.next_t = None, None, None
        self.from_direction, self.to_direction = None, None
        self.enter_time, self.middle_time, self.leave_time = 0, 0, 0
        self.offset = 0
        self.is_first_half = False

    def set_position_window(self, prev_t, curr_t, next_t):
        self.prev_t = prev_t
        self.curr_t = curr_t
        self.next_t = next_t

        self.from_direction = curr_t.direction_to(prev_t)
        self.to_direction = curr_t.direction_to(next_t)

    def set_time_window(self, enter, middle, leave):
        self.enter_time = enter
        self.middle_time = middle
        self.leave_time = leave

        if enter <= self.time < middle:
            self.offset = (self.time - enter) / (middle - enter)
            self.is_first_half = True
        else:
            self.offset = (self.time - middle) / (leave - middle)
            self.is_first_half = False

    def get_point_from_position(self):
        if self.is_first_half:
            enter, middle = self.curr_t.get_edge_middle(self.from_direction), self.curr_t.get_middle()
            position = enter.offset_to(middle, self.offset)
        else:
            middle, leave = self.curr_t.get_middle(), self.curr_t.get_edge_middle(self.to_direction)
            position = middle.offset_to(leave, self.offset)

        return position
