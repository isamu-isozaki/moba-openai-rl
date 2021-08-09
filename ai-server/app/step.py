from app.repository import create_step
import cv2
import numpy as np

def step(session, match_id, bot1_id, bot2_id, step_num, state, env, actions, video, render_size=128):
    for i in range(env.sides-1):
        env.step(actions[i])
    obs, rewards, done, infos =  env.step(actions[env.sides-1])
    if done:
        obs = env.reset()
    render = env.render()
    renders = []
    for i in range(env.sides):
        renders.append(cv2.resize(render[i].astype(np.float32), (render_size,render_size)))
    renders = np.concatenate(renders, axis=1)
    renders = renders.astype(np.uint8)
    video.write(renders)
    create_step(session, match_id, bot1_id, bot2_id, step_num, state, actions, rewards, done, infos, obs)
    return obs, rewards, done, infos
