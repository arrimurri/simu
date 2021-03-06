
import random
import math

import simu


# Consult python documentation in http://www.python.org


########################################################################
# Put all your code for the chaser agent into this class. You have
# to implement the execute method, but you can also add other methods
# as well. Just make sure that the method names are different from
# those of the agent class in the simu module.
class chaser_agent(simu.agent):

    # Do not add parameters to the call of this method, i.e.
    # the agents must be initialized with only name and color
    # parameters.
    def __init__(self, name, color):

        super(chaser_agent, self).__init__(name, color)
        # Add possible initialization below this line. At this
        # point many of the properties of the agent are not fully
        # initilized yet. E.g. you cannot get the position of the
        # agent yet, etc.

        self.wall_positions = {}




    # This is the method everybody has to implement. The execution
    # of code is not fully deterministic, meaning all the agents
    # are executed in random order at each time point.
    def execute(self):


        # Some examples below.
        # You should implement your agents using only the methods
        # shown in the examples below. You can also implement your
        # own helper methods using standard python API. You CAN NOT
        # change anything in the simu.py file or use methods found
        # in there if they are not listed in the examples below.

        # My name is this string.
        #self.name

        # My id is this integer.
        #self.id

        # Get names of all other agents in the system as a python list.
        #agents =  self.get_agent_names()

        # Get id of an agent of name NAME, e.g.
        #NAME = 'target'
        #ID = self.get_agent_id(NAME)

        # Get the sensor data as a python numpy array. -1 means
        # obstacle (wall), 0 means the position is free
        # and 1, 2, 3, ... means the position is occupied by an
        # agent of that id. The order of cells is clockwise starting
        # from the upper left corner of the 3x3 grid.
        # See the wall following agent example follow_wall.py.
        #sd = self.get_sensor_data()

        # Get my own position as a tuple (x, y)
        #position = self.get_position()

        # Get agent chaser0 position as a tuple (x, y)
        #position = self.get_position('chaser0')

        # Get the target position as a tuple (x, y)
        #position = self.get_position('target')

        # Talk to agent chaser3. The message can be any python object.
        #self.talk('chaser3', 1)

        # Retrieve possible messages from other agents. Returns
        # a dictionary as { 'sender0' : msg, sender1 : msg }, where
        # senders probably are chaser0, chaser1, ...
        #msgs = self.listen()

        # Do something with the possible message from chaser2
        #if msgs.has_key('chaser2'):
        #    msg2 = msgs['chaser2']
        #    self.helper_method(msg2, 0)

        # Store some info for the next execution. some_key and
        # some_info can be any python object, e.g.
        #some_key = 'ASDF'
        #some_info = (1, 2, 3)
        #self.params[some_key] = some_info

        # Retrieve some info stored earlier. some_key and
        # some_info can be any python object.
        #if self.params.has_key(some_key):
        #    some_info = self.params[some_key]

        # Clear all the earlier stored info.
        #self.params.clear()

        # If your agent(s) have reached their objective, you can
        # stop the simulator as below.
        #self.stop()

        # Call your helper method
        #self.helper_method(1, 2)

        # For loop in python
        #for i in range(10):
        #    print i

        # Send wall positions to other agents
        self.update_and_send_wall_positions()
        # Get wall positions from other agents
        self.get_wall_positions_from_others()

        # Get target positions
        target_pos = self.get_position('target')
        own_pos = self.get_position()

        if self.target_surrounded():
            self.stop()

        if target_pos in self.get_neighbours(own_pos):
            return

        # If the distance is long, then make it so that the search doubles the heuristic
        # value of each node. This makes astar function more lika a depth first search. This
        # change makes the algorithm a lot faster with greater distances (although it is not optimal,
        # but good enough for long distances.
        if self.euclid_distance > 20:
            list_of_moves = self.astar(target_pos, double_heuristic = True)
        else:
            list_of_moves = self.astar(target_pos)

        if not list_of_moves:
            print 'Astar returned false'
            return
        next_pos = list_of_moves.pop()

        direction = ''
        if next_pos == self.pos_up():
            direction = 'up'
        if next_pos == self.pos_down():
            direction = 'down'
        if next_pos == self.pos_left():
            direction = 'left'
        if next_pos == self.pos_right():
            direction = 'right'

        self.move(direction)
        

    # All extra methods should be inside the class.
    # All class methods have self as their first parameter.
    # self is a reference of the instance of the class.
    def helper_method(self, param0, param1):

        # Do nothing
        pass

    def target_surrounded(self):
        target_pos = self.get_position('target')
        neighbour_positions = self.get_neighbours(target_pos)
        chasers = self.get_agent_names()
        chaser_positions = [self.get_position(c) for c in chasers]
        chaser_positions.append(self.get_position())

        for pos in neighbour_positions:
            if pos not in chaser_positions and pos not in self.wall_positions:
                return False
        return True

    def astar(self, target, double_heuristic = False):
        start_pos = self.get_position()

        openlist = [start_pos]
        closedmap = {} 
        parent_node = {}
        path_weight = {}
        heuristic_weight = {}
        sum_weight = {}

        path_weight[start_pos] = 0
        heuristic_weight[start_pos] = self.euclid_distance(target)
        sum_weight[start_pos] = 0

        while len(openlist) > 0:
            openlist.sort(key = lambda x: sum_weight[x], reverse = True)
            node = openlist.pop()

            if node == target:
                return self.backtrack_route(node, parent_node)


            closedmap[node] = True

            for neighbour in self.get_neighbours(node):
                if closedmap.has_key(neighbour):
                    continue
                calc_score = path_weight[node] + 1

                if neighbour not in openlist:
                    insert_stats = True
                    openlist.append(neighbour)
                elif calc_score < path_weight[neighbour]:
                    insert_stats = True
                else:
                    insert_stats = False

                if insert_stats:
                    parent_node[neighbour] = node
                    path_weight[neighbour] = calc_score
                    heuristic_weight[neighbour] = self.euclid_distance(target, neighbour)
                    if double_heuristic:
                        heuristic_weight[neighbour] *= 2
                    sum_weight[neighbour] = path_weight[neighbour] + heuristic_weight[neighbour]
        return False

    def backtrack_route(self, node, parent_node):
        retlist = []
        while parent_node.has_key(node):
            retlist.append(node)
            node = parent_node[node]
        return retlist

    def get_neighbours(self, node):
        neighbours = []
        if node[0] < 0 or node[1] < 0:
            return neighbours

        if not self.wall_or_another_chaser(self.pos_right(node)):
            neighbours.append(self.pos_right(node))

        if not self.wall_or_another_chaser(self.pos_left(node)):
            neighbours.append(self.pos_left(node))

        if not self.wall_or_another_chaser(self.pos_up(node)):
            neighbours.append(self.pos_up(node))

        if not self.wall_or_another_chaser(self.pos_down(node)):
            neighbours.append(self.pos_down(node))
            
        return neighbours
        
    def wall_or_another_chaser(self, node):
        chaser_positions = [self.get_position(x) for x in self.get_agent_names() if x != 'target']
        if node in chaser_positions:
            return True
        if node in self.wall_positions:
            return True
        return False

    def get_wall_positions_from_others(self):
        msgs = self.listen()
        chasers = self.get_agent_names()
        wall_pos = []

        for c in chasers:
            if msgs.has_key(c):
                if msgs[c].has_key('wall_positions'):
                    for pos in msgs[c]['wall_positions']:
                        self.wall_positions[pos] = True

    def update_and_send_wall_positions(self):
        sd = self.get_sensor_data()
        wall_pos = []
        for i, s in enumerate(sd):
            if s == -1:
                coords = self.get_coords_of_sensor(i)
                wall_pos.append(coords)
                self.wall_positions[coords] = True

        chasers = self.get_agent_names()

        for c in chasers:
            self.talk(c, {'wall_positions': wall_pos})

    def get_coords_of_sensor(self, index):
        pos = self.get_position()

        # Return -1 if index is not in range 0 to 7
        if index < 0 and index > 10:
            return -1

        if index == 0:
            return (pos[0] - 1, pos[1] + 1)
        elif index == 1:
            return (pos[0], pos[1] + 1)
        elif index == 2:
            return (pos[0] + 1, pos[1] + 1)
        elif index == 3:
            return (pos[0] + 1, pos[1])
        elif index == 4:
            return (pos[0] + 1, pos[1] - 1)
        elif index == 5:
            return (pos[0], pos[1] - 1)
        elif index == 6:
            return (pos[0] - 1, pos[1] - 1)
        else:
            return (pos[0] - 1, pos[1])

    def pos_left(self, own_pos = None):
        if not own_pos:
            own_pos = self.get_position()
        return (own_pos[0] - 1, own_pos[1])

    def pos_right(self, own_pos = None):
        if not own_pos:
            own_pos = self.get_position()
        return (own_pos[0] + 1, own_pos[1])

    def pos_up(self, own_pos = None):
        if not own_pos:
            own_pos = self.get_position()
        return (own_pos[0], own_pos[1] + 1)

    def pos_down(self, own_pos = None):
        if not own_pos:
            own_pos = self.get_position()
        return (own_pos[0], own_pos[1] - 1)

    def euclid_distance(self, target_pos, chaser_pos = None):
        if chaser_pos == None:
            chaser_pos = self.get_position()

        distance = math.sqrt((target_pos[0] - chaser_pos[0])**2 + 
            (target_pos[1] - chaser_pos[1])**2)

        return distance


########################################################################
# Put all your code for the target agent into this class. You have
# to implement the execute method, but you can also add other methods
# as well. Just make sure that the method names are different from
# those of the agent class in the simu module.
class target_agent(simu.agent):

    def __init__(self, name, color):

        super(target_agent, self).__init__(name, color)
        # Add possible initialization below this line
        self.wall_positions = {}

    def update_wall_positions(self):
        sd = self.get_sensor_data()
        wall_pos = []
        for i, s in enumerate(sd):
            if s == -1:
                coords = self.get_coords_of_sensor(i)
                wall_pos.append(coords)
                self.wall_positions[coords] = True

    def get_coords_of_sensor(self, index):
        pos = self.get_position()

        # Return -1 if index is not in range 0 to 7
        if index < 0 and index > 10:
            return -1

        if index == 0:
            return (pos[0] - 1, pos[1] + 1)
        elif index == 1:
            return (pos[0], pos[1] + 1)
        elif index == 2:
            return (pos[0] + 1, pos[1] + 1)
        elif index == 3:
            return (pos[0] + 1, pos[1])
        elif index == 4:
            return (pos[0] + 1, pos[1] - 1)
        elif index == 5:
            return (pos[0], pos[1] - 1)
        elif index == 6:
            return (pos[0] - 1, pos[1] - 1)
        else:
            return (pos[0] - 1, pos[1])

    def get_chaser_positions(self):
        agent_names = self.get_agent_names()
        return [self.get_position(x) for x in agent_names if x != 'target']

    def sort_neighbours(self, neighbours):
        n_plus_points = []
        chaser_pos = self.get_chaser_positions()
        for n in neighbours:
            tmp_dict = {}
            tmp_dict[n] = 0
            if not self.wall_positions.has_key(n) and n not in chaser_pos:
                for n2 in self.get_neighbour_positions(n):
                    if self.wall_positions.has_key(n2):
                        tmp_dict[n] = tmp_dict[n] + 1
                    if n2 in chaser_pos:
                        tmp_dict[n] = tmp_dict[n] + 1
            else:
                tmp_dict[n] = 5
            n_plus_points.append((n, tmp_dict[n]))
        n_plus_points.sort(key = lambda x: x[1])
        return n_plus_points

    def get_neighbour_positions(self, pos = None):
        if not pos:
            pos = self.get_position()
        neighbours = []
        neighbours.append(self.pos_left(pos))
        neighbours.append(self.pos_right(pos))
        neighbours.append(self.pos_up(pos))
        neighbours.append(self.pos_down(pos))
        return neighbours

    def pos_left(self, own_pos = None):
        if not own_pos:
            own_pos = self.get_position()
        return (own_pos[0] - 1, own_pos[1])

    def pos_right(self, own_pos = None):
        if not own_pos:
            own_pos = self.get_position()
        return (own_pos[0] + 1, own_pos[1])

    def pos_up(self, own_pos = None):
        if not own_pos:
            own_pos = self.get_position()
        return (own_pos[0], own_pos[1] + 1)

    def pos_down(self, own_pos = None):
        if not own_pos:
            own_pos = self.get_position()
        return (own_pos[0], own_pos[1] - 1)

    def euclid_distance_to_chasers(self, pos):
        chaser_positions = self.get_chaser_positions()
        return sum([self.euclid_distance(x, pos) for x in chaser_positions])

    def get_shortest_distance(self, values):
        ret_val = values[0]
        ret_distance = self.euclid_distance_to_chasers(ret_val[0])
        for i, v in enumerate(values):
            if i == 0:
                continue
            if self.euclid_distance_to_chasers(v[0]) > ret_distance:
                ret_val = v
                ret_distance = self.euclid_distance_to_chasers(v[0])
        return ret_val

    def euclid_distance(self, target_pos, chaser_pos = None):
        if chaser_pos == None:
            chaser_pos = self.get_position()

        distance = math.sqrt((target_pos[0] - chaser_pos[0])**2 + 
            (target_pos[1] - chaser_pos[1])**2)

        return distance
            
    def execute(self):

        # Do not remove the line below or the test below that.
        sd = self.get_sensor_data()
        # Test whether there are any possible moves and if not
        # do nothing, i.e. chasers have won unless they are stupid.
        if sd[1] != 0 and sd[3] != 0 and sd[5] != 0 and sd[7] != 0:
            return
        # Do not remove the lines above.
        # Put all your code for the execute method below this line.

        self.update_wall_positions()

        num_of_chasers = len(self.get_agent_names()) - 1
        if self.euclid_distance_to_chasers(self.get_position()) > 5 * num_of_chasers:
            self.move(random.choice(['up', 'down', 'left', 'right']))
            return

        sorted_list = self.sort_neighbours(self.get_neighbour_positions())
        print sorted_list
        best_value = sorted_list[0][1]

        values_with_best_value = [x for x in sorted_list if x[1] == best_value]
        print values_with_best_value

        next_pos = self.get_shortest_distance(values_with_best_value)

        direction = ''
        if next_pos[0] == self.pos_up():
            direction = 'up'
        if next_pos[0] == self.pos_down():
            direction = 'down'
        if next_pos[0] == self.pos_left():
            direction = 'left'
        if next_pos[0] == self.pos_right():
            direction = 'right'

        print direction
        self.move(direction)
        # self.move(random.choice(['up', 'down', 'left', 'right']))
        #sd = self.get_sensor_data()

        #if sd[1] == -1 and sd[3] != -1 or sd[7] == sd[1] == -1:
            #self.move('right')
        #elif sd[3] == -1 and sd[5] != -1 or sd[1] == sd[3] == -1:
            #self.move('down')
        #elif sd[5] == -1 and sd[7] != -1 or sd[3] == sd[5] == -1:
            #self.move('left')
        #elif sd[7] == -1 and sd[1] != -1 or sd[5] == sd[7] == -1:
            #self.move('up')
        #elif sd[0] == -1:
            #self.move('up')
        #elif sd[6] == -1:
            #self.move('left')
        #elif sd[4] == -1:
            #self.move('down')
        #elif sd[2] == -1:
            #self.move('right')
        #else:
            #self.move(random.choice(('up', 'right', 'down', 'left')))



# Initialize the simulator and define the obstacles in the environment.
# The obstacles (walls) can only be horizontal or vertical.
S = simu.simu(walls = [[13, 25, 30, 25], [10, 15, 25, 15], [11, 5, 11, 16], [24, 5, 24, 16]], W = 600, H = 600)

# Add the target agent to position (39, 39)
# Do not change the name of the agent.
S.add_agent(target_agent('target', (255, 0, 0)), (39, 39))

# Add chaser agents to the bottom of the window starting from origo.
# Do not change the name of the agents. The names are chaser0, chaser1, ...
# These are the names that agents can use if/when communicating.
for i in xrange(4):
    S.add_agent(chaser_agent('chaser' + str(i), (255, 255, 255)), (i, 0))

# Run the simulation
S.run()

