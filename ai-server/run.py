"""
Author: Isamu Isozaki (isamu.website@gmail.com)
Description: Run learner server
Created:  2021-06-26T02:45:02.148Z
Modified: !date!
Modified By: Isamu Isozaki
TODO:
- If tables are not present, create and add 2 random models
"""
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
from app.app import app
import os
def run():
    app()


if __name__ == "__main__":
    run()