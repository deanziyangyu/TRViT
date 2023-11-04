import numpy as np
import os
import pandas as pd
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks
from scipy.signal import butter, filtfilt
import sys
import main

# Getting joint orientation data from main.py
Joint_Position = main.Joint_Orientation

# Define indices for joint positions
index_Spine_Base = 0  # 0-based indexing in Python
index_Spine_Mid = 4
index_Neck = 8
index_Head = 12  # no orientation
index_Shoulder_Left = 16
index_Elbow_Left = 20
index_Wrist_Left = 24
index_Hand_Left = 28
index_Shoulder_Right = 32
index_Elbow_Right = 36
index_Wrist_Right = 40
index_Hand_Right = 44
index_Hip_Left = 48
index_Knee_Left = 52
index_Ankle_Left = 56
index_Foot_Left = 60  # no orientation
index_Hip_Right = 64
index_Knee_Right = 68
index_Ankle_Right = 72
index_Foot_Right = 76  # no orientation
index_Spine_Shoulder = 80
index_Tip_Left = 84  # no orientation
index_Thumb_Left = 88  # no orientation
index_Tip_Right = 92  # no orientation
index_Thumb_Right = 96  # no orientation


# Extract joint positions from Joint_Position data
Hip_R = Joint_Position[:, index_Hip_Right : index_Hip_Right + 3]
Knee_R = Joint_Position[:, index_Knee_Right : index_Knee_Right + 3]
Ankle_R = Joint_Position[:, index_Ankle_Right : index_Ankle_Right + 3]
Foot_R = Joint_Position[:, index_Foot_Right : index_Foot_Right + 3]

Hip_L = Joint_Position[:, index_Hip_Left : index_Hip_Left + 3]
Knee_L = Joint_Position[:, index_Knee_Left : index_Knee_Left + 3]
Ankle_L = Joint_Position[:, index_Ankle_Left : index_Ankle_Left + 3]
Foot_L = Joint_Position[:, index_Foot_Left : index_Foot_Left + 3]

Spine_B = Joint_Position[:, index_Spine_Base : index_Spine_Base + 3]
Spine_M = Joint_Position[:, index_Spine_Mid : index_Spine_Mid + 3]
Head_C = Joint_Position[:, index_Head : index_Head + 3]

Spine_Sh = Joint_Position[:, index_Spine_Shoulder : index_Spine_Shoulder + 3]
Shoulder_R = Joint_Position[:, index_Shoulder_Right : index_Shoulder_Right + 3]
Shoulder_L = Joint_Position[:, index_Shoulder_Left : index_Shoulder_Left + 3]

Elbow_R = Joint_Position[:, index_Elbow_Right : index_Elbow_Right + 3]
Wrist_R = Joint_Position[:, index_Wrist_Right : index_Wrist_Right + 3]
Hand_R = Joint_Position[:, index_Hand_Right : index_Hand_Right + 3]

Elbow_L = Joint_Position[:, index_Elbow_Left : index_Elbow_Left + 3]
Wrist_L = Joint_Position[:, index_Wrist_Left : index_Wrist_Left + 3]
Hand_L = Joint_Position[:, index_Hand_Left : index_Hand_Left + 3]
