'''
Functionalities:
Run semi-random deployed models from learner-server in ai-data/models(decide how to do match making)
Save state, action, reward, next state in ai-data/matches/num with the game_timestep at .01 or lower
In the db, have 
1. Bot table which stores the saved models, their elo, and type of algorithm
2. Match table which stores fight results between bots and folder name
3. Step table containing file path to Match parent id, step number, and file path to the state, action, reward, next state file

Future:
Make it so that I can play against bots based on their elo
'''