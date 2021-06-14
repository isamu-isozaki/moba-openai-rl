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
2. Define perliminary file structure/files
    X Currently, made structure of 
    - app/app.py selecting the bots and starting matches
    - app/match.py working with running the match
    - app/step.py doing the steps in the environment and saving
3. Create 2 models which output random actions with np.randint
4. Run with m parallel environments for each match using asyncio
5. Make env restart once a game ends and just continue running
6. Make them populate the DB and the file structure
7. After 2000 steps, stop the match and Query 2n models again
8. Play matches with those 2n models with m envs each. So, n*m envs are running now.


## Future:
Make it so that I can play against bots based on their elo