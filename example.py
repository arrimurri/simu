
import random

import simu


########################################################################
# Example of an agent, which moves randomly until mouse is pressed
# after which it tries to go to that position. This agent is rather
# stupid so it will get stuck if there are obstacles in its path.
class my_agent(simu.agent):

    def execute(self):

        mouse_pos = self.mouse()
        if mouse_pos != None:
            self.params['target'] = mouse_pos

        direction = None

        if self.name == 'agent5':
            self.talk('agent0', "ASDF")
            self.radar()


        if 'target' in self.params:
            target = self.params['target']
            pos = self.get_position()
            if pos[0] - target[0] < 0:
                direction = 'right'
            elif pos[0] - target[0] > 0:
                direction = 'left'
            elif pos[1] - target[1] < 0:
                direction = 'up'
            elif pos[1] - target[1] > 0:
                direction = 'down'
                
            self.move(direction)

        else:    
            self.move(random.choice(['up', 'down', 'left', 'right']))







# Initialize the simulator
S = simu.simu(walls = [[13, 25, 30, 25], [10, 15, 25, 15], [11, 5, 11, 16], [24, 5, 24, 16]])

# Add some agents of class my_agent to the bottom of the window starting
# from origo..
for i in xrange(20):
    S.add_agent(my_agent('stupid_agent' + str(i), (255, 255, 0)), (i, 0))

# Run the simulation
S.run()

