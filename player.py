from environment import GraphicDisplay
from environment import Environment

class PolicyIteration:
    def __init__(self, environment):
        self.environment = environment
        
if __name__ == "__main__":
    print("Start")
    environment = Environment()
    player = PolicyIteration(environment)
    display = GraphicDisplay(player)
    display.mainloop()
    print("End")