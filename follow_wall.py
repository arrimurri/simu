
import random

import simu


########################################################################
# Example of an agent, which moves randomly untill finding a wall
# and then follows the wall.
class follow_wall_agent(simu.agent):

    def execute(self):

        sd = self.get_sensor_data()
        if sd[1] == -1 and sd[3] != -1 or sd[7] == sd[1] == -1:
            self.move('right')
        elif sd[3] == -1 and sd[5] != -1 or sd[1] == sd[3] == -1:
            self.move('down')
        elif sd[5] == -1 and sd[7] != -1 or sd[3] == sd[5] == -1:
            self.move('left')
        elif sd[7] == -1 and sd[1] != -1 or sd[5] == sd[7] == -1:
            self.move('up')
        elif sd[0] == -1:
            self.move('up')
        elif sd[6] == -1:
            self.move('left')
        elif sd[4] == -1:
            self.move('down')
        elif sd[2] == -1:
            self.move('right')
        else:
            self.move(random.choice(('up', 'right', 'down', 'left')))


# Initialize the simulator and walls. All the walls have to be horizontal or vertical.
S = simu.simu(walls = [[13, 25, 30, 25], [10, 15, 25, 15], [11, 5, 11, 16], [24, 5, 24, 16]])

# Add some follow_wall_agents to random positions.
for i in xrange(50):
    S.add_agent(follow_wall_agent('agent' + str(i), (255, 255, 0)), \
                                 (random.randint(0, 39), random.randint(0, 39)))

# Run the simulation
S.run()

