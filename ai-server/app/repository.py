from app.db_models import Bot, Match, Step, base, engine
import numpy as np
import pickle
import os.path
import math

def init_db():
    base.metadata.drop_all(engine)
    base.metadata.create_all(engine)

def init_bots(session):
    bot_count = get_bot_counts(session)
    if bot_count == 0:
        create_random_bots(session)

def get_bot_counts(session):
    return session.query(Bot).count()

def get_random_bots(session, n=2):
    rows = get_bot_counts(session)
    bot_ids = (np.random.permutation(rows)[:n]+1).tolist()
    bots = session.query(Bot).filter(Bot.id.in_(bot_ids)).all()
    return bots

def get_newest_bots(session, n=2):
    return session.query(Bot).limit(n)

def get_smartest_bots(session, n=2):
    return session.query(Bot).order_by(Bot.elo.desc()).limit(n)

def get_bots_from_ids(session, ids):
    return session.query(Bot).filter(Bot.id.in_(ids)).all()

def elo_prob(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

def update_elo(session, db_models, wins, k=27):
    bot_ids = [db_model.id for db_model in db_models]
    db_models = get_bots_from_ids(session, bot_ids)
    elos = [db_model.elo for db_model in db_models]
    preds = [0, 0]
    # Probability of player 0 winning
    preds[0] = elo_prob(elos[1], elos[0])
    preds[1] = elo_prob(elos[0], elos[1])
    # Update elo rating
    for i, win in enumerate(wins):
        if win == 1:
            elos[i] = elos[i]+k*(1-preds[i])
        else:
            elos[i] = elos[i]-k*preds[i]
        db_models[i].elo = elos[i]

    session.commit()
    elos = [int(elo) for elo in elos]
    return elos

def update_match_wins(session, match, bot_1_wins, bot_2_wins):
    match.bot_1_wins = bot_1_wins
    match.bot_2_wins =  bot_2_wins
    session.commit()

def create_random_bots(session, action_space_size=1):
    bot1 = Bot(model='Random', action_space_size=action_space_size)
    session.add(bot1)
    bot2 = Bot(model='Random', action_space_size=action_space_size)
    session.add(bot2)
    session.commit()

def create_match_table(session, bot_id1, bot_id2, elo1, elo2):
    elo1 = int(elo1)
    elo2 = int(elo2)
    match = Match(bot_id1=bot_id1, bot_id2=bot_id2, max_elo=max(elo1, elo2), min_elo=min(elo1, elo2), elo_sum=elo1+elo2)
    session.add(match)
    session.flush()
    folder_name = f'/data/{match.id}'
    try:
        os.mkdir(folder_name)
        os.mkdir(folder_name+'/0')
        os.mkdir(folder_name+'/1')
    except:
        None
    match.folder_name = folder_name
    session.commit()
    return match

def create_step(session, match_id, bot1_id, bot2_id, step_num, state, action, reward, done, info, obs):
    bot_1_file_path = f'/data/{match_id}/0/{step_num}'
    bot_2_file_path = f'/data/{match_id}/1/{step_num}'

    assert not os.path.isfile(bot_1_file_path)
    assert not os.path.isfile(bot_2_file_path)

    bot_1_step = Step(step_num=step_num, match_id=match_id, file_path=bot_1_file_path, bot_id=bot1_id)
    session.add(bot_1_step)
    bot_2_step = Step(step_num=step_num, match_id=match_id, file_path=bot_2_file_path, bot_id=bot2_id)
    session.add(bot_2_step)
    session.commit()

    with open(bot_1_file_path, 'wb') as fout:
        pickle.dump((np.array([state[0]]), np.array([action[0]]), reward[0], done, info, np.array([obs[0]])), fout)
    with open(bot_2_file_path, 'wb') as fout:
        pickle.dump((np.array([state[1]]), np.array([action[1]]), reward[1], done, info, np.array([obs[1]])), fout)
