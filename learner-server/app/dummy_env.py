"""
Author: Isamu Isozaki (isamu.website@gmail.com)
Description: description
Created:  2021-08-07T22:37:46.978Z
Modified: !date!
Modified By: modifier
"""

import gym

class DummyEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self, action_space, observation_space):
    super(DummyEnv, self).__init__()
    self.action_space = action_space
    self.observation_space = observation_space

  def step(self, action):
    None
  def reset(self):
    None
  def render(self, mode='human', close=False):
    None