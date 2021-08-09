"""
Author: Isamu Isozaki (isamu.website@gmail.com)
Description: description
Created:  2021-07-17T19:16:31.253Z
Modified: !date!
Modified By: modifier
"""

from app.db_models import Bot, Match, Step, base, engine
import numpy as np
import pickle
import os.path
import math
LOAD_LIMIT = 50000
def get_step_counts(session):
    return session.query(Step).count()

def get_newest_steps(session, n=5000):
    return list(session.query(Step).limit(n))

def get_smartest_bot_steps(session, n=5000):
    recent_steps = session.query(Step).limit(LOAD_LIMIT)
    sorted_steps = sorted(recent_steps, key=lambda step: -step.bot.elo)
    return list(sorted_steps[:n])

def get_random_steps(session, n=5000):
    rows = get_step_counts(session)
    rows_used = min(rows, LOAD_LIMIT)
    step_ids = (np.random.permutation(rows_used)[:n]+rows-rows_used+1).tolist()
    steps = session.query(Step).filter(Step.id.in_(step_ids)).all()
    return list(steps)

def create_bot(session, model, total_timestamps, action_space_size, log_folder, data_policy, file_path, network, n_steps, learning_rate, max_grad_norm, gamma, ent_coef, params=''):
    bot = Bot(model=model, total_timestamps=total_timestamps, action_space_size=action_space_size, log_folder=log_folder, data_policy=data_policy, file_path=file_path, network=network, n_steps=n_steps, learning_rate=learning_rate, max_grad_norm=max_grad_norm, gamma=gamma, ent_coef=ent_coef, params=params)
    session.add(bot)
    session.commit()

