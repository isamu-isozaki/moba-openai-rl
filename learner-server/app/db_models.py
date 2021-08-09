from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

import os
engine = db.create_engine(
    os.getenv('DB_URI'),
    poolclass=NullPool
)
session_factory = sessionmaker(bind=engine)
Session = orm.scoped_session(session_factory)
base = declarative_base()
base.metadata.bind = engine

class Bot(base):
    # Include prev_model
    __tablename__ = 'Bot'
    id = db.Column(db.Integer,primary_key=True)
    model = db.Column(db.String(255),nullable=False)
    action_space_size = db.Column(db.Integer, default=1, nullable=False)
    log_folder = db.Column(db.String(255))
    elo = db.Column(db.Integer, default=1000)
    data_policy = db.Column(db.String(255))
    file_path = db.Column(db.String(255))
    network = db.Column(db.String(255))
    n_steps = db.Column(db.Integer)
    learning_rate = db.Column(db.Numeric)
    max_grad_norm = db.Column(db.Numeric)
    gamma = db.Column(db.Numeric)
    ent_coef = db.Column(db.Numeric)
    params = db.Column(db.String(255))
    total_timestamps = db.Column(db.Integer)
    # Other parameters not present in params
    match_bot1 = db.orm.relationship('Match', foreign_keys='Match.bot_id1', back_populates='bot1')
    match_bot2 = db.orm.relationship('Match', foreign_keys='Match.bot_id2', back_populates='bot2')
    step = db.orm.relationship('Step')



class Match(base):
    # False if bot_id1 loses True otherwise
    __tablename__ = 'Match'
    id = db.Column(db.Integer,primary_key=True)
    bot_id1 = db.Column(db.Integer, db.ForeignKey('Bot.id'), nullable=False)
    bot_id2 = db.Column(db.Integer, db.ForeignKey('Bot.id'), nullable=False)
    bot1 = db.orm.relationship('Bot', back_populates='match_bot1', uselist=False, foreign_keys=[bot_id1])
    bot2 = db.orm.relationship('Bot', back_populates='match_bot2', uselist=False, foreign_keys=[bot_id2])
    max_elo = db.Column(db.Integer, nullable=False)
    min_elo = db.Column(db.Integer, nullable=False)
    elo_sum = db.Column(db.Integer, nullable=False)
    # convert to bot_ids
    bot_1_wins = db.Column(db.Integer)
    bot_2_wins = db.Column(db.Integer)
    folder_name = db.Column(db.String(255))
    step = db.orm.relationship('Step')


class Step(base):
    __tablename__ = 'Step'
    id = db.Column(db.Integer,primary_key=True)
    step_num = db.Column(db.Integer,nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('Match.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    bot_id = db.Column(db.Integer, db.ForeignKey('Bot.id'), nullable=False)
    bot = db.orm.relationship('Bot', back_populates='step', uselist=False, foreign_keys=[bot_id])