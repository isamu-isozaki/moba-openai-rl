# Learner Server

## Functionalities:

Train models with data in /data/matches and deploy to /data/models under the respective algorithms
Compare:
    - Training with probability prioritizing the higher elo models
    - Training random matches
The data in /data/matches will replace the collect_rollout function by sampling random actions to put in buffer(for now)
In the db add an entry to the bot table

### DB Functionalities
    - Query n most recent/random data from the Steps table 
    - Query n most high elo match files from the Steps table using also Bots and Matches table
    - Add Bot entry to Bots table with 1000 elo

## Steps to implement
1. Make DB structure
    - Bot table
    - Match table
    - Step table

    X defined in app/model.py
2. Define perliminary file structure/files
    X Currently, made structure of 
    - app/app.py choosing m models/a model to train with parameters from GridSearch
    - app/grid.py choosing what parameters to train the next model/models
    - app/data.py reponsible for getting the data for the models to train on
    - app/train.py train a model given data from data.py and parameters from grid.py
    - app/deploy.py deploy trained model to ai-server
3. Wait until 10000 random file names are in Step Table using time.sleep
4. Query 10000 random file names from Step table
5. Implement collect_rollout_from_files and add the 10000 random files
    - Implement method to read the state, action, reward from each file
6. Try training with one model and see if it trains
7. Test deploying+Save to db
8. Train models with as many parameters as possible at once
9. Test deploying+Save to db
10. Keep circulating models for ever and keep repeating step 2