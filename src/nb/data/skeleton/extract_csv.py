import pickle as pkl
import pandas as pd
import os

object = None

os.mkdir('./store/')

with open("./skelton_3D_0.pkl", "rb") as f:
    object = pkl.load(f)


for i in range(0, len(list(object.values())[1]), 10):
    score = str(int(list(object.values())[1][i]['label'][0]))
    name = f"{list(object.values())[1][i]['frame_dir']}_s={score}"
    os.mkdir(f'./store/{name}')
    for frame in range(0, len(list(object.values())[1][i]['keypoint'][0]), 5):
        df = pd.DataFrame(list(object.values())[1][i]['keypoint'][0][frame])
        frame_filled = '{:0>4}'.format(frame) # fill zeros to four digits for correct sorting
        df.to_csv(f'./store/{name}/{frame_filled}.csv')