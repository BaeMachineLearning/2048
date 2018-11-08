import tkinter as tk

UNIT = 100
WIDTH = 4
HEIGHT = 4
POSSIBLE_ACTIONS = [0, 1, 2, 3]  # 상, 하, 좌, 우
ACTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # 좌표로 나타낸 행동

class GraphicDisplay(tk.Tk):
    def __init__(self):
        super(GraphicDisplay, self).__init__()
        self.title('2048')
        self.geometry('{0}x{1}'.format(WIDTH * UNIT, HEIGHT * UNIT + 50))
        self.canvas = self._build_canvas()
    
    def _build_canvas(self):
        canvas = tk.Canvas(self, bg='white', width=WIDTH * UNIT, height=HEIGHT * UNIT)
        
        for col in range(0, WIDTH * UNIT, UNIT):
            canvas.create_line(col, 0, col, HEIGHT * UNIT)
        for row in range(0, HEIGHT * UNIT, UNIT):
            canvas.create_line(0, row, WIDTH * UNIT, row)
        
        up_button = tk.Button(self, text="Up", command=self.up)
        up_button.configure(width=10)
        canvas.create_window(WIDTH * UNIT * 0.125, HEIGHT * UNIT + 10, window=up_button)
        down_button = tk.Button(self, text="Down", command=self.down)
        down_button.configure(width=10)
        canvas.create_window(WIDTH * UNIT * 0.375, HEIGHT * UNIT + 10, window=down_button)
        left_button = tk.Button(self, text="Left", command=self.left)
        left_button.configure(width=10)
        canvas.create_window(WIDTH * UNIT * 0.625, HEIGHT * UNIT + 10, window=left_button)
        right_button = tk.Button(self, text="Right", command=self.right)
        right_button.configure(width=10)
        canvas.create_window(WIDTH * UNIT * 0.875, HEIGHT * UNIT + 10, window=right_button)

        canvas.pack()
        return canvas

    def up(self):
        pass
    
    def down(self):
        pass
    
    def left(self):
        pass

    def right(self):
        pass

class Game:
    def __init__(self):
        self.states = [[0] * WIDTH for _ in range(HEIGHT)]

    def state_after_action(self, state, action):
        if action == 0:
            for column in range(WIDTH):
                new_column = []
                for row in range(HEIGHT):
                    state = states[column][row]
                    if state > 0:
                        if new_column.last == state:
                            new_column.last += state
                        else:
                            new_column.append(state)
                states[column] = new_column                    
        elif action == 1:
            pass
        elif action == 2:
            pass
        else:
            pass

    def get_reward(self, state, action):
        next_state = self.state_after_action(state, action)
        reward = 0
        for column in range(WIDTH):
            for row in range(HEIGHT):
                reward += states[column][row]
        return reward