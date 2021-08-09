"""
Author: Isamu Isozaki (isamu.website@gmail.com)
Description: description
Created:  2021-07-18T00:52:34.813Z
Modified: !date!
Modified By: modifier
"""
from stable_baselines3 import A2C, PPO
import random
action_space_grid = [2]

data_policy_grid = ['random', 'newest', 'smartest']
timestamps_grid = [int(5e5), int(1e6), int(5e6)]

policy_grid = {
    'A2C': {
        'model': [A2C],
        'policy': ['MlpPolicy'],
        'learning_rate': [0.1, 0.01, 0.001, 7e-4, 0.0001],
        'n_steps': [100, 500, 1000],
        'gamma': [0.9, 0.99, 0.999, 0.9999],
        'ent_coef': [0, 0.1, 0.2, 0.3, 0.4],
        'vf_coef': [0.5, 1, 1.5],
        'max_grad_norm': [0.5, 1, 1.5],
        'normalize_advantage': [True, False]
    },
    'PPO': {
        'model': [PPO],
        'policy': ['MlpPolicy'],
        'clip_range': [0.1, 0.2, 0.3],
        'learning_rate': [0.1, 0.01, 0.001, 7e-4, 0.0001],
        'n_steps': [100, 500, 1000],
        'gamma': [0.9, 0.99, 0.999, 0.9999],
        'ent_coef': [0, 0.1, 0.2, 0.3, 0.4],
        'vf_coef': [0.5, 1, 1.5],
        'max_grad_norm': [0.5, 1, 1.5]
    }
}
def select_random_board_size():
    # For now only support two by two
    return random.choice(action_space_grid)

def select_random_data_policy():
    return random.choice(data_policy_grid)

def select_total_timestamps():
    return random.choice(timestamps_grid)

def select_random_model():
    model = random.choice(list(policy_grid.keys()))
    output_dict = {}
    for key in policy_grid[model]:
        output_dict[key] = random.choice(policy_grid[model][key])
    return model, output_dict