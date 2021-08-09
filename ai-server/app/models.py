"""
Author: Isamu Isozaki (isamu.website@gmail.com)
Description: Stores types of policy models
Created:  2021-06-27T23:59:38.027Z
Modified: 2021-07-03T18:14:47.643Z
Modified By: Isamu Isozaki
"""
import numpy as np

class RandomPolicyModel:
    def __init__(self, action_space=1, num_actions=5):
        self.action_space = action_space
        self.num_actions = num_actions
    def predict(self, obs):
        return np.random.randint(self.num_actions, size=(self.action_space, self.action_space)), None