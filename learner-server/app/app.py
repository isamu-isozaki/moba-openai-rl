"""
Author: Isamu Isozaki (isamu.website@gmail.com)
Description: description
Created:  2021-07-17T19:15:36.660Z
Modified: !date!
Modified By: modifier
"""
import os
import time

from app.db_models import Session
import json
from app.repository import get_step_counts, create_bot
from app.grid import select_random_board_size, select_random_data_policy, select_total_timestamps, select_random_model
from app.data import get_steps
from app.dummy_env import DummyEnv
from stable_baselines3.common.utils import get_latest_run_id

def app(get_action_space, observation_space, min_num_steps=5000):
    session = Session()
    while True:
        time.sleep(10)
        num_steps = get_step_counts(session)
        if num_steps > min_num_steps:
            break
        print(f'Current steps {num_steps}/{min_num_steps}')
    parent_path = '/data'
    if int(os.getenv('IS_DOCKER')) == 0:
        parent_path = '../ai-data'
    tensorboard_log = parent_path+'/logs'
    model_dir = parent_path+'/models'

    while True:
        # Getting frid
        act_board_size = select_random_board_size()
        action_space = get_action_space(act_board_size)
        env = DummyEnv(action_space, observation_space)
        data_policy = select_random_data_policy()
        get_steps_with_policy = lambda x: get_steps(x, session, data_policy=data_policy)
        total_timestamps = select_total_timestamps()
        model_name, model_dict = select_random_model()
        
        model = model_dict['model']
        policy = model_dict['policy']
        del model_dict['model']
        del model_dict['policy']
        tb_log_name = f'{model_name}_{policy}_{data_policy}_data_{total_timestamps}'
        latest_run_id = get_latest_run_id(tensorboard_log, tb_log_name)
        log_save_path = os.path.join(tensorboard_log, f"{tb_log_name}_{latest_run_id + 1}")
        save_path = os.path.join(model_dir, f"{tb_log_name}_{latest_run_id + 1}")
        print('started training with params:')
        print(tb_log_name)
        print(model_dict)
        model = model(policy, env, verbose=1, tensorboard_log=tensorboard_log, **model_dict)
        model.learn_from_steps(total_timestamps, get_steps_with_policy, tb_log_name=tb_log_name)
        model.save(save_path)


        n_steps, learning_rate, max_grad_norm, gamma, ent_coef = model_dict['n_steps'], model_dict['learning_rate'], model_dict['max_grad_norm'], model_dict['gamma'], model_dict['ent_coef']
        del model_dict['n_steps']
        del model_dict['learning_rate']
        del model_dict['max_grad_norm']
        del model_dict['gamma']
        del model_dict['ent_coef']
        if int(os.getenv('IS_DOCKER')) == 0:
            log_save_path = log_save_path.replace('../ai-data', '/data')
            save_path = save_path.replace('../ai-data', '/data')


        create_bot(session, model_name, total_timestamps, act_board_size, log_save_path, data_policy, save_path, policy, n_steps, learning_rate, max_grad_norm, gamma, ent_coef, params=json.dumps(model_dict))