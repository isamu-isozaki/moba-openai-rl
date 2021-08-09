"""
Author: Isamu Isozaki (isamu.website@gmail.com)
Description: Tasks for celery
Created:  2021-06-27T23:41:06.755Z
Modified: 2021-06-27T23:41:21.837Z
Modified By: Isamu Isozaki
"""
from celery import Celery
import os
from pathlib import Path
import shutil
import traceback
from celery.exceptions import Ignore
from celery.utils.log import get_task_logger
import pandas as pd
from app.step import step
import numpy as np
from app.repository import get_random_bots, get_newest_bots, get_smartest_bots, update_elo, update_match_wins, create_match_table
from app.models import RandomPolicyModel
import torch
import gym
import tactic_game_gym
from app.db_models import Session
import cv2
from stable_baselines3 import A2C, PPO

def make_celery():
    """
    Make celery worker
    """
    return Celery(__name__, broker=os.getenv('REDIS'), backend=os.getenv('REDIS'))

logger = get_task_logger(__name__)
celery_app = make_celery()

@celery_app.task(bind=True)
def match(self, env_name='tactic_game-v0', model_query_policy='random', sides=2, num_steps=1000, k=27, framerate=30, render_size=128):
    """
    Celery task for a match

    Args:
        self(celery task): Celery task
        env_name (str, optional): Name of the environment. Defaults to 'tactic_game-v0'.
        model_query_policy (str, optional): Policy for getting the models to have a match. Defaults to 'random'.
        sides (int, optional): The number of sides fighting. Defaults to 2.
        num_steps (int, optional): The number of steps for each match. Defaults to 5000.
        k (int, optional): elo coefficient. Defaults to 27.
        framerate (int, optional): video frame rate. Defaults to 30.
        render_size (int, optional): render size of video. Defaults to 128.
    """
    session = Session()
    # Make env
    env = gym.make(env_name)
    
    while True:
        obs = env.reset()

        # Query models
        db_models = [None for _ in range(sides)]
        if model_query_policy == 'newest':
            db_models = get_newest_bots(session, sides)
        elif model_query_policy == 'smartest':
            db_models = get_smartest_bots(session, sides)
        else:
            # Random
            db_models = get_random_bots(session, sides)
        elos = [int(db_model.elo) for db_model in db_models]
        models = [load(model) for model in db_models]
        match = create_match_table(session, db_models[0].id, db_models[1].id, elos[0], elos[1])
        video = cv2.VideoWriter(f'/data/{match.id}.avi', 0, framerate, (render_size*sides,render_size))
        winnings = [0, 0]
        total_rewards = np.zeros(sides)

        for i in range(num_steps):
            actions = []
            for j in range(len(models)):
                action, _ = models[j].predict(obs[j])
                actions.append(np.array(action).reshape([-1]))
            obs, rewards, done, infos = step(session, match.id, db_models[0].id, db_models[1].id, i, obs, env, actions, video, render_size)
            total_rewards += rewards
            if done:
                wins=[0, 0]
                for j, info in enumerate(infos['episode']):
                    if info["win"]:
                        wins[j] = 1
                        winnings[j] += 1
                elos = update_elo(session, db_models, wins, k=k)
                # ASSUME: only 2 players for now 
            integer_rewards = [int(reward) for reward in total_rewards.tolist()]
            meta_data = {'current': i, 'total': num_steps, 'rewards': integer_rewards, 'winnings': winnings, 'elos': elos, 'models': [str(db_model.model) for db_model in db_models]}
            if env_name == 'tactic_game-v0':
                meta_data['remaining'] =infos['board']['remaining_players']
                for j in range(len(meta_data['remaining'])):
                    meta_data['remaining'][j] = int(meta_data['remaining'][j])
            self.update_state(state='PROGRESS', meta=meta_data)
        cv2.destroyAllWindows()
        video.release()
        # Add to match table
        update_match_wins(session, match, winnings[0], winnings[1])

def load(db_model, action_space_size=1, num_actions=5):
    if db_model.model == 'Random':
        return RandomPolicyModel(db_model.action_space_size, num_actions)
    return eval(db_model.model).load(db_model.file_path.replace('\\', '/'))


