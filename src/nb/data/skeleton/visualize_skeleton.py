import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
from pathlib import Path
import subprocess

body = {
    0: 'Spine Base',
    1: 'Spine Mid',
    2: 'Neck',
    3: 'Head',
    4: 'Left Shoulder',
    5: 'Left Elbow',
    6: 'Left Wrist',
    7: 'Left Hand',
    8: 'Right Shoulder',
    9: 'Right Elbow',
    10:'Right Wrist',
    11:'Right Hand',
    12:'Left Hip',
    13:'Left Knee',
    14:'Left Ankle',
    15:'Left Foot',
    16:'Right Hip',
    17:'Right Knee',
    18:'Right Ankle',
    19:'Right Foot',
    20:'Spine at Shoulder',
    21:'Left Hand Tip',
    22:'Left Thumb',
    23:'Right Hand Tip',
    24:'Right Thumb',
}

plt.clf()
my_dpi = 100
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(800/my_dpi, 640/my_dpi), dpi=my_dpi)
plt.subplots_adjust(left=0.02, right=0.98, top=0.96, bottom=0.01)

def read_csv(file_path):
    # Read CSV file into a pandas DataFrame
    matrix = pd.read_csv(file_path, index_col=0, header=0).values
    # matrix = matrix.reshape((-1,))
    # print(matrix.shape)

    # Reshape matrix to shape: (number_of_timestamps, 25_joints, 3_coordinates_per_joint)
    # matrix = matrix.reshape((-1, 25, 3))
    return matrix

def plot_view(ax, skt_ls, v_ax1, v_ax2, label='full'):
        # ignoring both thumbs
    for connection in [
        (0, 1), (1, 20), (20, 2), (2, 3), # spine
    ]:
        xx = [skt_ls[connection[0]][v_ax1], skt_ls[connection[1]][v_ax1]]
        yy = [skt_ls[connection[0]][v_ax2], skt_ls[connection[1]][v_ax2]]
        ax.plot(xx, yy, 'r-')

    for connection in [
        (20, 4), (4, 5), (5, 6), (6, 7), (7, 21), # left arm
    ]:
        xx = [skt_ls[connection[0]][v_ax1], skt_ls[connection[1]][v_ax1]]
        yy = [skt_ls[connection[0]][v_ax2], skt_ls[connection[1]][v_ax2]]
        ax.plot(xx, yy, 'b-')

    for connection in [
        (20, 8), (8, 9), (9, 10), (10, 11), (11, 23), # right arm
    ]:
        xx = [skt_ls[connection[0]][v_ax1], skt_ls[connection[1]][v_ax1]]
        yy = [skt_ls[connection[0]][v_ax2], skt_ls[connection[1]][v_ax2]]
        ax.plot(xx, yy, 'g-')
    
    for connection in [
        (0, 12), (12, 13), (13, 14), (14, 15), # left leg
    ]:
        xx = [skt_ls[connection[0]][v_ax1], skt_ls[connection[1]][v_ax1]]
        yy = [skt_ls[connection[0]][v_ax2], skt_ls[connection[1]][v_ax2]]
        ax.plot(xx, yy, 'c-')

    for connection in [
        (0, 16), (16, 17), (17, 18), (18, 19), # right leg
    ]:
        xx = [skt_ls[connection[0]][v_ax1], skt_ls[connection[1]][v_ax1]]
        yy = [skt_ls[connection[0]][v_ax2], skt_ls[connection[1]][v_ax2]]
        ax.plot(xx, yy, 'm-')
    
    # 2D plot (you can plot separate graphs for x, y and z)
    for (i, pos) in enumerate(skt_ls):
        # Plotting x and y coordinates only

        # head
        if i == 3:
            ax.scatter(pos[v_ax1], pos[v_ax2], c='b', s=[500], alpha=0.3, edgecolors="none")
        # Remove thumbs
        elif i in [22, 24]:
            ...
        else:
            ax.scatter(pos[v_ax1], pos[v_ax2], c='k', edgecolors="none")


    for i in [4, 5, 6]: # 7 removed for collision avoidance
        ax.text(skt_ls[i][v_ax1]-0.02, skt_ls[i][v_ax2]+0.02, body[i], color="blue", fontsize=10, horizontalalignment='right')

    # i == 21: # left hip
    ax.text(skt_ls[21][v_ax1]-0.02, skt_ls[21][v_ax2]-0.02, body[21], color="blue", fontsize=10, horizontalalignment='right')

    for i in [8, 9, 10]: # 11 removed for collision avoidance
        ax.text(skt_ls[i][v_ax1]+0.02, skt_ls[i][v_ax2]+0.02, body[i], color="green", fontsize=10, horizontalalignment='left')
    
    # i == 23: # left hip
    ax.text(skt_ls[23][v_ax1]+0.02, skt_ls[23][v_ax2]-0.02, body[23], color="green", fontsize=10, horizontalalignment='left')

    # i == 12: # left hip
    ax.text(skt_ls[12][v_ax1]-0.02, skt_ls[12][v_ax2]-0.04, body[12], color="cyan", fontsize=10, horizontalalignment='right')

    for i in [13, 14, 15]:
        ax.text(skt_ls[i][v_ax1]-0.02, skt_ls[i][v_ax2]+0.02, body[i], color="cyan", fontsize=10, horizontalalignment='right')
    
    # i == 16: # right hip
    ax.text(skt_ls[16][v_ax1]+0.02, skt_ls[16][v_ax2]-0.04, body[16], color="magenta", fontsize=10, horizontalalignment='left')
    
    for i in [17, 18, 19]: # right hip
        ax.text(skt_ls[i][v_ax1]+0.02, skt_ls[i][v_ax2]+0.02, body[i], color="magenta", fontsize=10, horizontalalignment='left')
    
    if label=='full':
        for i in [0, 1, 2, 3, 20]: # spine base
            ax.text(skt_ls[i][v_ax1], skt_ls[i][v_ax2]+0.04, body[i], color="red", fontsize=10, horizontalalignment='center')



def plot_skeleton(skeleton_positions, rep_name, num):
    # Assuming skeleton_positions is a list of numpy arrays representing (x, y, z) coordinates

    assert len(skeleton_positions) > 0, 'No skeleton data found'

    # index_Spine_Base = 0
    # index_Spine_Mid = 4
    # index_Neck = 8
    # index_Head = 12  # no orientation
    # index_Shoulder_Left = 16
    # index_Elbow_Left = 20
    # index_Wrist_Left = 24
    # index_Hand_Left = 28
    # index_Shoulder_Right = 32
    # index_Elbow_Right = 36
    # index_Wrist_Right = 40
    # index_Hand_Right = 44
    # index_Hip_Left = 48
    # index_Knee_Left = 52
    # index_Ankle_Left = 56
    # index_Foot_Left = 60  # no orientation
    # index_Hip_Right = 64
    # index_Knee_Right = 68
    # index_Ankle_Right = 72
    # index_Foot_Right = 76  # no orientation
    # index_Spine_Shoulder = 80
    # index_Tip_Left = 84  # no orientation
    # index_Thumb_Left = 88  # no orientation
    # index_Tip_Right = 92  # no orientation
    # index_Thumb_Right = 96  # no orientation


    # Set spine to grey
    ax1.spines['bottom'].set_color('#dddddd')
    ax1.spines['top'].set_color('#dddddd') 
    ax1.spines['right'].set_color('#dddddd')
    ax1.spines['left'].set_color('#dddddd')

    ax2.spines['bottom'].set_color('#dddddd')
    ax2.spines['top'].set_color('#dddddd') 
    ax2.spines['right'].set_color('#dddddd')
    ax2.spines['left'].set_color('#dddddd')

    ax1.set_aspect('equal')
    ax2.set_aspect('equal')
    # ax1.axis('off')
    # ax2.axis('off')

    ax1.set_xticks([])
    ax1.set_yticks([])
    ax2.set_xticks([])
    ax2.set_yticks([])

    ax1.set_xticklabels([])
    ax1.set_yticklabels([])
    ax2.set_xticklabels([])
    ax2.set_yticklabels([])

    ax1.set_title('Frontal View')
    ax2.set_title('Sagittal View')

    skt_ls = skeleton_positions.tolist()

    plot_view(ax=ax1, skt_ls=skt_ls, v_ax1=0, v_ax2=1, label='full')
    plot_view(ax=ax2, skt_ls=skt_ls, v_ax1=2, v_ax2=1, label='part')


    plt.savefig(f'./store/{rep_name}/{num}.png')
    ax1.clear()
    ax2.clear()

def make_video(rep):
    subprocess.call([
        'ffmpeg', '-framerate', '4', '-pattern_type', 'glob', '-i', f'./store/{rep}/*.png',
          '-r', '30', '-pix_fmt', 'yuv420p',
        f'./store/{rep}/{rep}.mp4'
    ])

def make_gif(rep):
    subprocess.call([
    'ffmpeg', '-i', f'./store/{rep}/{rep}.mp4',
        '-vf', 'fps=4,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse',
        '-loop', '0', f'./store/{rep}/{rep}.gif'
    ])

def main(rep):
    file_paths = glob.glob(f'./store/{rep}/*.csv')

    # Plot each frame
    for file_path in file_paths:
        joint_data_1 = read_csv(file_path)
        plot_skeleton(joint_data_1, rep, Path(file_path).stem)

if __name__ == '__main__':
    dir_paths = glob.glob('./store/*')
    for dir_path in dir_paths:
        rep_name = Path(dir_path).name
        main(rep_name)
        make_video(rep_name)
        make_gif(rep_name)
