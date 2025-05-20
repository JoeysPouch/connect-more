class Animation:
    def __init__(self, frames, positions, looping, pause_game):
        self.frames = frames
        self.positions = positions
        self.looping = looping
        self.pause_game = pause_game
        self.current_frame = -1
        self.current_position = -1
        self.complete = False

    def get_frame_and_pos(self):
        if self.current_frame + 1 < len(self.frames):
            self.current_frame += 1
        elif len(self.frames) >= len(self.positions):
            if self.looping:
                self.current_frame = 0
                self.current_position = -1
            else:
                self.complete = True

        if self.current_position + 1 < len(self.positions):
            self.current_position += 1
        elif len(self.frames) <= len(self.positions):
            if self.looping:
                self.current_frame = 0
                self.current_position = 0
            else:
                self.complete = True

        return self.frames[self.current_frame], self.positions[self.current_position]

