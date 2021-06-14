from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db

base = declarative_base()
engine = db.create_engine(YOUR_DB_URI)
base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)

class Bot(base):
    __tablename__ = 'Bot'
    id = db.Column(db.Integer,primary_key=True)
    data_policy = db.Column(db.String(255),nullable=False)
    elo = db.Column(db.Integer, default=1000)
    file_path = db.Column(db.String(255),nullable=False)
    model = db.Column(db.String(255),nullable=False)
    network = db.Column(db.String(255),nullable=False)
    batch_size = db.Column(db.Integer,nullable=False)
    learning_rate = db.Column(db.Numeric,nullable=False)
    max_grad_norm = db.Column(db.Numeric,nullable=False)
    gamma = db.Column(db.Numeric,nullable=False)
    tau = db.Column(db.Numeric,nullable=False)
    action_space_side = db.Column(db.Integer,nullable=False)
    params = db.Column(db.String(255),nullable=False) 
    # Other parameters not present in params
    match = db.relationship('Match', back_populates='Bot')


class Match(base):
    # False if bot_id1 loses True otherwise
    __tablename__ = 'Match'
    id = db.Column(db.Integer,primary_key=True)
    bot_id1 = db.Column(db.Integer, db.ForeignKey('Bot.id'), nullable=False)
    bot_id2 = db.Column(db.Integer, db.ForeignKey('Bot.id'), nullable=False)
    result = db.Column(db.Boolean, default=False)
    folder_name = db.Column(db.String(255), nullable=False)
    step = db.relationship('Step', back_populates='Match')


class Step(base):
    __tablename__ = 'Step'
    id = db.Column(db.Integer,primary_key=True)
    step_num = db.Column(db.Integer,nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('Match.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)


