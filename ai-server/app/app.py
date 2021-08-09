from celery import Celery
from app.tasks import match
import time
from app.db_models import Session
from app.repository import init_db, init_bots

init_db()
def app(num_matches=4):
    init_db()
    session = Session()
    init_bots(session)

    matches = []
    for _ in range(num_matches):
        matches.append(match.delay())

    while True:
        time.sleep(10)
        print('-------------------------------------------')
        for match_stat in matches:
            print(match_stat.info)
        print('-------------------------------------------')
        

        