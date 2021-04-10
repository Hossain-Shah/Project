import numpy as np
import pylab as plt
import networkx as nx
# mapping denote the corresponding edges between nodes
points_list = [(0, 1), (1, 5), (4, 5), (5, 4), (1, 2), (2, 3), (2, 5)]
goal = 3
G = nx.Graph()
G.add_edges_from(points_list)
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)
plt.show()
# R matrix
R = np.matrix([[-1, -1, -1, -1, 0, -1],
               [-1, -1, -1, 0, -1, 100],
               [-1, -1, -1, 0, -1, -1],
               [-1, 0, 0, -1, 0, -1],
               [-1, 0, 0, -1, -1, 100],
               [-1, 0, -1, -1, 0, 100]])
# assign zeros to paths and 200 to goal-reaching point
for point in points_list:
    print(point)
    if point[1] == goal:
        R[point] = 200
    else:
        R[point] = 0

    if point[0] == goal:
        R[point[::-1]] = 200
    else:
        # reverse of point
        R[point[::-1]] = 0
# add goal point round trip
R[goal, goal] = 200
print(R)
# Q matrix
Q = np.matrix(np.zeros([6, 6]))
# Gamma (learning parameter).
gamma = 0.8
# Initial state. (Usually to be chosen at random)
initial_state = 1


# This function returns all available actions in the state given as an argument
def available_actions(state):
    current_state_row = R[state,]
    av_act = np.where(current_state_row >= 0)[1]
    return av_act


# Get available actions in the current state
available_act = available_actions(initial_state)


# This function chooses at random which action to be performed within the range
# of all the available actions.
def sample_next_action(available_actions_range):
    next_action = int(np.random.choice(available_act, 1))
    return next_action


# Sample next action to be performed
action = sample_next_action(available_act)


# This function updates the Q matrix according to the path selected and the Q
# learning algorithm
def update(current_state, action, gamma):
    max_index = np.where(Q[action,] == np.max(Q[action,]))[1]
    if max_index.shape[0] > 1:
        max_index = int(np.random.choice(max_index, size=1))
    else:
        max_index = int(max_index)
    max_value = Q[action, max_index]
    # Q learning formula
    Q[current_state, action] = R[current_state, action] + gamma * max_value
    print('max_value', R[current_state, action] + gamma * max_value)
    if (np.max(Q) > 0):
        return (np.sum(Q / np.max(Q) * 100))
    else:
        return (0)


# Update Q matrix
update(initial_state, action, gamma)
# -------------------------------------------------------------------------------
# Training
# Train over 10 000 iterations. (Re-iterate the process above).
scores = []
for i in range(10000):
    current_state = np.random.randint(0, int(Q.shape[0]))
    available_act = available_actions(current_state)
    action = sample_next_action(available_act)
    update(current_state, action, gamma)
    scores.append(update(current_state, action, gamma))
# Normalize the "trained" Q matrix
print("Trained Q matrix:")
print(Q / np.max(Q) * 100)
current_state = 3
steps = [current_state]
while current_state != 2:
    next_step_index = np.where(Q[current_state,] == np.max(Q[current_state,]))[1]
    if next_step_index.shape[0] > 1:
        next_step_index = int(np.random.choice(next_step_index, size=1))
    else:
        next_step_index = int(next_step_index)
    steps.append(next_step_index)
    current_state = next_step_index
print("Selected path:")
print(steps)
