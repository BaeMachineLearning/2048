import tkinter as tk
import random, time, copy

UNIT = 100
WIDTH = 4
HEIGHT = 4
POSSIBLE_ACTIONS = [0, 1, 2, 3]  # 상, 하, 좌, 우
ACTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # 좌표로 나타낸 행동

class GraphicDisplay(tk.Tk):
    def __init__(self, player):
        super(GraphicDisplay, self).__init__()
        self.title('2048')
        self.player = player
        self.geometry('{0}x{1}'.format(WIDTH * UNIT, HEIGHT * UNIT + 50))
        self.canvas = self._build_canvas()
        self.texts = []

        self.player.environment.tick()
        self.update()

    def _build_button(self, text, command):
        button = tk.Button(self, text=text, command=command)
        button.configure(width=10)
        return button
    
    def _build_canvas(self):
        canvas = tk.Canvas(self, bg='white', width=WIDTH * UNIT, height=HEIGHT * UNIT)
        
        for column in range(0, WIDTH * UNIT, UNIT):
            canvas.create_line(column, 0, column, HEIGHT * UNIT)
        for row in range(0, HEIGHT * UNIT, UNIT):
            canvas.create_line(0, row, WIDTH * UNIT, row)
        
        canvas.create_window(WIDTH * UNIT * 0.125, HEIGHT * UNIT + 10, window=self._build_button("Up", self.up))
        canvas.create_window(WIDTH * UNIT * 0.375, HEIGHT * UNIT + 10, window=self._build_button("Down", self.down))
        canvas.create_window(WIDTH * UNIT * 0.625, HEIGHT * UNIT + 10, window=self._build_button("Left", self.left))
        canvas.create_window(WIDTH * UNIT * 0.875, HEIGHT * UNIT + 10, window=self._build_button("Right", self.right))
        canvas.pack()
        return canvas

    def reset(self):
        self.player.environment.states = [[0] * WIDTH for _ in range(HEIGHT)]
        self.update()

    def up(self):
        new_states = copy.deepcopy(self.player.environment.states)
        self.player.environment.up()
        if self.player.environment.HasChanged(self.player.environment.states, new_states):
            self.player.environment.tick()
        self.update()

    def down(self):
        new_states = copy.deepcopy(self.player.environment.states)
        self.player.environment.down()
        if self.player.environment.HasChanged(self.player.environment.states, new_states):
            self.player.environment.tick()
        self.update()

    def left(self):
        new_states = copy.deepcopy(self.player.environment.states)
        self.player.environment.left()
        if self.player.environment.HasChanged(self.player.environment.states, new_states):
            self.player.environment.tick()
        self.update()
    
    def right(self):
        new_states = copy.deepcopy(self.player.environment.states)
        self.player.environment.right()
        if self.player.environment.HasChanged(self.player.environment.states, new_states):
            self.player.environment.tick()
        self.update()

    def update(self):
        time.sleep(0.1)
        states = self.player.environment.states
        for text in self.texts:
            self.canvas.delete(text)

        for column in range(WIDTH):
            for row in range(HEIGHT):
                state = states[column][row]
                if state > 0:
                    x, y = 50 + UNIT * column, 50 + UNIT * row
                    font = ('Helvetica', str(20), 'normal')
                    text = self.canvas.create_text(x, y, fill="black", text=str(state), font=font)
                    self.texts.append(text)

class Environment:
    def __init__(self):
        self.states = [[0] * WIDTH for _ in range(HEIGHT)]

    def state_after_action(self, state, action):
        if action == 0:
            self.up()
        elif action == 1:
            self.down()
        elif action == 2:
            self.left()
        else:
            self.right()

    def get_reward(self, state, action):
        #next_state = self.state_after_action(state, action)
        reward = 0
        for column in range(WIDTH):
            for row in range(HEIGHT):
                reward += self.states[column][row]
        return reward
        
    def tick(self):
        empty_states = []
        for column in range(WIDTH):
            for row in range(HEIGHT):
                if self.states[column][row] == 0:
                    empty_states.append((column, row))
        
        empty_state = random.sample(empty_states, 1)[0]
        self.states[empty_state[0]][empty_state[1]] = 2

    def up(self):
        for column in range(WIDTH):
            new_column = []
            last_state = 0
            for row in range(HEIGHT):
                state = self.states[column][row]
                if state > 0:
                    if last_state == state:
                        new_column[-1] += state
                    else:
                        new_column.append(state)
                    last_state = state
            
            for _ in range(HEIGHT - len(new_column)):
                new_column.append(0)

            self.states[column] = new_column
    
    def down(self):
        self.states = self.rotate_cw(self.rotate_cw(self.states))
        self.up()
        self.states = self.rotate_cw(self.rotate_cw(self.states))
    
    def left(self):
        self.states = self.rotate_cw(self.states)
        self.up()
        self.states = self.rotate_cw(self.rotate_cw(self.rotate_cw(self.states)))

    def right(self):
        self.states = self.rotate_cw(self.rotate_cw(self.rotate_cw(self.states)))
        self.up()
        self.states = self.rotate_cw(self.states)

    def rotate_cw(self, states):
        new_states = [[0] * WIDTH for _ in range(HEIGHT)]
        new_states[0][0], new_states[1][0], new_states[2][0], new_states[3][0] = states[0][3], states[0][2], states[0][1], states[0][0]
        new_states[0][1], new_states[1][1], new_states[2][1], new_states[3][1] = states[1][3], states[1][2], states[1][1], states[1][0]
        new_states[0][2], new_states[1][2], new_states[2][2], new_states[3][2] = states[2][3], states[2][2], states[2][1], states[2][0]
        new_states[0][3], new_states[1][3], new_states[2][3], new_states[3][3] = states[3][3], states[3][2], states[3][1], states[3][0]
        return new_states

    def HasChanged(self, old_states, new_states):
        for column in range(WIDTH):
            for row in range(HEIGHT):
                if new_states[column][row] != self.states[column][row]:
                    return True

        return False