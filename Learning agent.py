import gym
env = gym.make("Taxi-v2").env
env.render()
env.reset()
env.render()
print("Action Space {}".format(env.action_space))
print("State Space {}".format(env.observation_space))
state = env.encode(3, 1, 2, 0)
print("State:", state)
env.s = state
env.render()
print(env.P[328])
env.s = 328

epochs = 0
penalties, reward = 0, 0

frames = []
done = False

while not done:
    action = env.action_space.sample()
    state, reward, done, info = env.step(action)

    if reward == -10:
        penalties += 1

    frames.append({
        'frame': env.render(mode='ansi'),
        'state': state,
        'action': action,
        'reward': reward
    }
    )

    epochs += 1

print("Timesteps taken: {}".format(epochs))
print("Penalties incurred: {}".format(penalties))


