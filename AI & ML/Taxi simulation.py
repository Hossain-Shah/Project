import gym
import numpy as np
env = gym.make("Taxi-v2")
env.reset()
env.render()
state = env.reset()
counter = 0
reward = None
while reward != 20:
    state, reward, done, info = env.step(env.action_space.sample())
    counter += 1
print(counter)
Q = np.zeros([env.observation_space.n, env.action_space.n])
G = 0
gamma = 0.618
for episode in range(1,1001):
    done = False
    G, reward, counter = 0,0,0
    state = env.reset()
    while done != True:
            action = np.argmax(Q[state])
            state2, reward, done, info = env.step(action)
            Q[state,action] = (reward + gamma * np.max(Q[state2]))
            G += reward
            counter += 1
            state = state2
    if episode % 50 == 0:
        print('Episode {} Total Reward: {} counter: {}'.format(episode,G,counter))