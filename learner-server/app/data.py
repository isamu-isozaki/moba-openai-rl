"""
Author: Isamu Isozaki (isamu.website@gmail.com)
Description: Responsible for getting data to train the models on
Created:  2021-07-17T19:27:45.765Z
Modified: 2021-07-17T20:48:49.399Z
Modified By: Isamu Isozaki 
"""
from app.repository import get_newest_steps, get_smartest_bot_steps, get_random_steps

def get_steps(n, session, data_policy='newest'):
    if data_policy == 'newest':
        return get_newest_steps(session, n)
    elif data_policy == 'smartest':
        return get_smartest_bot_steps(session, n)
    elif data_policy == 'random':
        return get_random_steps(session, n)
