"""
Author: Isamu Isozaki (isamu.website@gmail.com)
Description: Tasks for celery
Created:  2021-06-27T21:18:45.789Z
Modified: 2021-06-27T22:08:40.192Z
Modified By: Isamu Isozaki
"""
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

from app.tasks import celery_app