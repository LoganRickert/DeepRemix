import gym


env = gym.make('CartPole-v0')
for episode in range(20):
    observation = env.reset()
    for step in range(100):
        env.render()
        print observation
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print "Episode finished after {} timesteps".format(step + 1)
            break
