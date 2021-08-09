# AI Server

## Functionalities:
Run semi-random deployed models from learner-server in /data/models(decide how to do match making)
 - Add noise using https://arxiv.org/pdf/2005.05719.pdf
Save state, action, reward, next state in /data/matches/num with the game_timestep at .01 or lower
In the db, have 
1. Bot table which stores the saved models, their elo, and type of algorithm
2. Match table which stores fight results between bots, the bot ids, and folder name
3. Step table containing file path to Match parent id, step number, and file path to the state, action, reward, next state file

### DB Functionalities
- Query 2n random models(prioritize new) to battle each other from the Bot table.
- Create a Match table entry on every fight with a folder 
- Every step, save to the Step table along with a file to the match folder


## Steps to implement
1. Make DB structure
    - Bot table
    - Match table
    - Step table

    X defined in app/model.py
2. Define perliminary file structure/files+function to fun game in a vid
    X Currently, made structure of 
    - app/app.py start matches and selecting bots
    - app/match.py working with running the match 
    - app/step.py doing the steps in the environment and saving
3. Create 2 models which output random actions with np.randint X
4. Run with m parallel environments for each match using threading(celery/redis) X
5. Make env restart once a game ends and just continue running -> Already done
6. Make them populate the DB and the file structure X
7. After 5000 steps, stop the match and Query 2n models again X
8. Visualize matched

## Future:
Make it so that I can play against bots based on their elo