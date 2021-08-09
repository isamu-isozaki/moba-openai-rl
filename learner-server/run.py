"""
Author: Isamu Isozaki (isamu.website@gmail.com)
Description: Run learner server
Created:  2021-06-26T02:45:02.148Z
Modified: !date!
Modified By: Isamu Isozaki
TODO:
- If tables are not present, create and add 2 random models
"""
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
from app.app import app
import os
import gym
import numpy as np
def run():
    if int(os.getenv('IS_DOCKER')) == 1 and int(os.getenv('DOCKER')) == 0:
        return
    obs_board_size = 32
    obs_shape = (obs_board_size, obs_board_size, 2*3)
    get_act_size = lambda x: gym.spaces.MultiDiscrete([5 for _ in range(x*x)])
    observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=obs_shape, dtype=np.float32)
    app(get_act_size, observation_space)


if __name__ == "__main__":
    run()