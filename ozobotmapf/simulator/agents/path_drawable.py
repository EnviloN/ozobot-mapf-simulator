class PathDrawable:
    def __init__(self, drawable, time, duration):
        self.drawable = drawable
        self.valid_until = time + duration

    def is_valid(self, time):
        return True if time <= self.valid_until else False
