import numpy as np
import os
import pandas as pd
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks
from scipy.signal import butter, filtfilt


# Directory containing the CSV files (relative path)
directory = "Raw"

# List all files in the directory
files = os.listdir(directory)

# Filter "JointPosition" files
joint_position_files = [
    file for file in files if "JointPosition" in file and file.endswith(".csv")
]

# Filter "JointOrientation" files
joint_orientation_files = [
    file for file in files if "JointOrientation" in file and file.endswith(".csv")
]

# Initialize DataFrames for JointPosition and JointOrientation
joint_position_data = pd.DataFrame()
joint_orientation_data = pd.DataFrame()

# Loop through the filtered JointPosition CSV files
for file in joint_position_files:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)

    # Append the data from the current file to the JointPosition DataFrame
    Joint_Position = pd.concat([joint_position_data, df], ignore_index=True)

# Loop through the filtered JointOrientation CSV files
for file in joint_orientation_files:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)

    # Append the data from the current file to the JointOrientation DataFrame
    Joint_Orientation = pd.concat([joint_orientation_data, df], ignore_index=True)

# Now, `Joint_Position` contains the data from all the JointPosition CSV files,
# and `Joint_Orientation` contains the data from all the JointOrientation CSV files


# Load the necessary csv files using pandas

# Joint_Position = pd.read_csv("JointPosition011214_103748.csv")
# print(Joint_Position)

# Joint_Orientation = pd.read_csv("JointOrientation011214_103748.csv")
# print(Joint_Orientation)


# Convert the DataFrame to a NumPy array
Joint_Position = Joint_Position.to_numpy()
Joint_Orientation = Joint_Orientation.to_numpy()


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


def filtering(x):
    # Define filter parameters
    filtCutOff = 1
    sample = 30

    # Design a Butterworth low-pass filter
    b, a = butter(3, (2 * filtCutOff) / sample, "low")

    # Apply the filter to the input signal x using filtfilt
    media = filtfilt(b, a, x)

    return media


# PRIMARY OUTCOME

shoulder_extR = np.arctan2(
    Spine_Sh[:, 2] - Elbow_R[:, 2], Spine_Sh[:, 1] - Elbow_R[:, 1]
)
shoulder_extR = np.degrees(shoulder_extR)

shoulder_extL = np.arctan2(
    Spine_Sh[:, 2] - Elbow_L[:, 2], Spine_Sh[:, 1] - Elbow_L[:, 1]
)
shoulder_extL = np.degrees(shoulder_extL)

# Removing singularity
for j in range(1, len(shoulder_extR) - 1):
    if (
        shoulder_extR[j + 1] - shoulder_extR[j] < -100
        or shoulder_extR[j + 1] - shoulder_extR[j] > 100
    ):
        shoulder_extR[j + 1] = -shoulder_extR[j + 1]

for j in range(1, len(shoulder_extL) - 1):
    if (
        shoulder_extL[j + 1] - shoulder_extL[j] < -100
        or shoulder_extL[j + 1] - shoulder_extL[j] > 100
    ):
        shoulder_extL[j + 1] = -shoulder_extL[j + 1]

# Filtering P.O.
shoulder_extR = filtering(shoulder_extR)
shoulder_extL = filtering(shoulder_extL)

# Peak detection
sogliaR = np.max(shoulder_extR) / np.sqrt(2)
sogliaL = np.max(shoulder_extL) / np.sqrt(2)

nsamples = len(shoulder_extR)
samples = np.arange(1, nsamples + 1)

# Find peaks
maxR, _ = find_peaks(shoulder_extR, height=sogliaR, distance=int(nsamples / 12))
minR, _ = find_peaks(
    np.max(shoulder_extR) - shoulder_extR, height=sogliaR, distance=int(nsamples / 12)
)
minR = np.max(shoulder_extR) - minR

maxL, _ = find_peaks(shoulder_extL, height=sogliaL, distance=int(nsamples / 12))
minL, _ = find_peaks(
    np.max(shoulder_extL) - shoulder_extL, height=sogliaL, distance=int(nsamples / 12)
)
minL = np.max(shoulder_extL) - minL

# Control factor

# ANGLE ELBOW

link_bracciototL = np.sqrt(
    (Shoulder_L[:, 0] - Wrist_L[:, 0]) ** 2
    + (Shoulder_L[:, 1] - Wrist_L[:, 1]) ** 2
    + (Shoulder_L[:, 2] - Wrist_L[:, 2]) ** 2
)
link_bracciototR = np.sqrt(
    (Shoulder_R[:, 0] - Wrist_R[:, 0]) ** 2
    + (Shoulder_R[:, 1] - Wrist_R[:, 1]) ** 2
    + (Shoulder_R[:, 2] - Wrist_R[:, 2]) ** 2
)
link_braccioL = np.sqrt(
    (Shoulder_L[:, 0] - Elbow_L[:, 0]) ** 2
    + (Shoulder_L[:, 1] - Elbow_L[:, 1]) ** 2
    + (Shoulder_L[:, 2] - Elbow_L[:, 2]) ** 2
)
link_braccioR = np.sqrt(
    (Shoulder_R[:, 0] - Elbow_R[:, 0]) ** 2
    + (Shoulder_R[:, 1] - Elbow_R[:, 1]) ** 2
    + (Shoulder_R[:, 2] - Elbow_R[:, 2]) ** 2
)
link_avambraccioL = np.sqrt(
    (Elbow_L[:, 0] - Wrist_L[:, 0]) ** 2
    + (Elbow_L[:, 1] - Wrist_L[:, 1]) ** 2
    + (Elbow_L[:, 2] - Wrist_L[:, 2]) ** 2
)
link_avambraccioR = np.sqrt(
    (Elbow_R[:, 0] - Wrist_R[:, 0]) ** 2
    + (Elbow_R[:, 1] - Wrist_R[:, 1]) ** 2
    + (Elbow_R[:, 2] - Wrist_R[:, 2]) ** 2
)
angologomitoL = np.degrees(
    np.arccos(
        (link_avambraccioL**2 + link_braccioL**2 - link_bracciototL**2)
        / (2 * link_avambraccioL * link_braccioL)
    )
)
angologomitoR = np.degrees(
    np.arccos(
        (link_avambraccioR**2 + link_braccioR**2 - link_bracciototR**2)
        / (2 * link_avambraccioR * link_braccioR)
    )
)
angologomitoLt = angologomitoL[:-15]  # Cut the last 15 values
angologomitoRt = angologomitoR[:-15]  # Cut the last 15 values

# ANGLE KNEE

link_gambatotL = np.sqrt(
    (Hip_L[:, 0] - Ankle_L[:, 0]) ** 2
    + (Hip_L[:, 1] - Ankle_L[:, 1]) ** 2
    + (Hip_L[:, 2] - Ankle_L[:, 2]) ** 2
)
link_gambatotR = np.sqrt(
    (Hip_R[:, 0] - Ankle_R[:, 0]) ** 2
    + (Hip_R[:, 1] - Ankle_R[:, 1]) ** 2
    + (Hip_R[:, 2] - Ankle_R[:, 2]) ** 2
)
link_femoreR = np.sqrt(
    (Hip_R[:, 0] - Knee_R[:, 0]) ** 2
    + (Hip_R[:, 1] - Knee_R[:, 1]) ** 2
    + (Hip_R[:, 2] - Knee_R[:, 2]) ** 2
)
link_femoreL = np.sqrt(
    (Hip_L[:, 0] - Knee_L[:, 0]) ** 2
    + (Hip_L[:, 1] - Knee_L[:, 1]) ** 2
    + (Hip_L[:, 2] - Knee_L[:, 2]) ** 2
)
link_tibiaR = np.sqrt(
    (Knee_R[:, 0] - Ankle_R[:, 0]) ** 2
    + (Knee_R[:, 1] - Ankle_R[:, 1]) ** 2
    + (Knee_R[:, 2] - Ankle_R[:, 2]) ** 2
)
link_tibiaL = np.sqrt(
    (Knee_L[:, 0] - Ankle_L[:, 0]) ** 2
    + (Knee_L[:, 1] - Ankle_L[:, 1]) ** 2
    + (Knee_L[:, 2] - Ankle_L[:, 2]) ** 2
)
angologinocchioL = np.degrees(
    np.arccos(
        (link_tibiaL**2 + link_femoreL**2 - link_gambatotL**2)
        / (2 * link_tibiaL * link_femoreL)
    )
)
angologinocchioR = np.degrees(
    np.arccos(
        (link_tibiaR**2 + link_femoreR**2 - link_gambatotR**2)
        / (2 * link_tibiaR * link_femoreR)
    )
)
angologinocchioLt = angologinocchioL[:-15]  # Cut the last 15 values
angologinocchioRt = angologinocchioR[:-15]  # Cut the last 15 values

# ANGLE C

angleHipL = np.arctan2(Spine_B[:, 0] - Hip_L[:, 0], Spine_B[:, 1] - Hip_L[:, 1])
angleHipL = np.degrees(angleHipL)
angleHipR = np.arctan2(Hip_R[:, 0] - Spine_B[:, 0], Hip_R[:, 1] - Spine_B[:, 1])
angleHipR = np.degrees(angleHipR)
angleHipRt = angleHipR[:-15]  # Cut the last 15 values
angleHipLt = angleHipL[:-15]  # Cut the last 15 values

# AEREA TRONCO

link_shoulder = np.sqrt(
    (Shoulder_L[:, 0] - Shoulder_R[:, 0]) ** 2
    + (Shoulder_L[:, 1] - Shoulder_R[:, 1]) ** 2
    + (Shoulder_L[:, 2] - Shoulder_R[:, 2]) ** 2
)
link_hip = np.sqrt(
    (Hip_L[:, 0] - Hip_R[:, 0]) ** 2
    + (Hip_L[:, 1] - Hip_R[:, 1]) ** 2
    + (Hip_L[:, 2] - Hip_R[:, 2]) ** 2
)
link_shoulderhipR = np.sqrt(
    (Shoulder_R[:, 0] - Hip_R[:, 0]) ** 2
    + (Shoulder_R[:, 1] - Hip_R[:, 1]) ** 2
    + (Shoulder_R[:, 2] - Hip_R[:, 2]) ** 2
)
link_shoulderhipL = np.sqrt(
    (Shoulder_L[:, 0] - Hip_L[:, 0]) ** 2
    + (Shoulder_L[:, 1] - Hip_L[:, 1]) ** 2
    + (Shoulder_L[:, 2] - Hip_L[:, 2]) ** 2
)
link_shoulderR_hipL = np.sqrt(
    (Shoulder_R[:, 0] - Hip_L[:, 0]) ** 2
    + (Shoulder_R[:, 1] - Hip_L[:, 1]) ** 2
    + (Shoulder_R[:, 2] - Hip_L[:, 2]) ** 2
)
semiperimetroR = (link_hip + link_shoulderR_hipL + link_shoulderhipR) / 2
areaeroneR = np.sqrt(
    semiperimetroR
    * (semiperimetroR - link_hip)
    * (semiperimetroR - link_shoulderR_hipL)
    * (semiperimetroR - link_shoulderhipR)
)
semiperimetroL = (link_shoulder + link_shoulderR_hipL + link_shoulderhipL) / 2
areaeroneL = np.sqrt(
    semiperimetroL
    * (semiperimetroL - link_shoulder)
    * (semiperimetroL - link_shoulderR_hipL)
    * (semiperimetroL - link_shoulderhipL)
)
sommaaree = areaeroneR + areaeroneL  # Calculate trunk area using Heron's formula
sommaareet = sommaaree[:-15]  # Cut the last 15 values

# HAND JOINT

link_hand = np.sqrt(
    (Hand_R[:, 0] - Hand_L[:, 0]) ** 2
    + (Hand_R[:, 1] - Hand_L[:, 1]) ** 2
    + (Hand_R[:, 2] - Hand_L[:, 2]) ** 2
)
link_handt = link_hand[:-15]  # Cut the last 15 values

# LINK BETWEEN ANKLES

link_foot = np.sqrt(
    (Ankle_R[:, 0] - Ankle_L[:, 0]) ** 2
    + (Ankle_R[:, 1] - Ankle_L[:, 1]) ** 2
    + (Ankle_R[:, 2] - Ankle_L[:, 2]) ** 2
)
link_foott = link_foot[:-15]  # Cut the last 15 values

# REGULARITY

derR = np.diff(maxR)
derL = np.diff(maxL)

# Look into this code
# derR = np.diff(ind_maxR)
# derL = np.diff(ind_maxL)


# Define a list of arrays
arrays = [
    shoulder_extR,
    shoulder_extL,
    angologomitoLt,
    angologomitoRt,
    angologinocchioLt,
    angologinocchioRt,
    angleHipLt,
    angleHipRt,
    sommaareet,
    link_handt,
    link_foott,
    derR,
    derL,
]

# Define a list of corresponding column names
column_names = [
    "shoulder_extR",
    "shoulder_extL",
    "angologomitoLt",
    "angologomitoRt",
    "angologinocchioLt",
    "angologinocchioRt",
    "angleHipLt",
    "angleHipRt",
    "sommaareet",
    "link_handt",
    "link_foott",
    "derR",
    "derL",
]

# Save each array into a separate CSV file
for i in range(len(arrays)):
    data = {column_names[i]: arrays[i]}
    df = pd.DataFrame(data)
    df.to_csv(f"{column_names[i]}.csv", index=False)


import pandas as pd

# List of separate CSV files
csv_files = [
    "shoulder_extR.csv",
    "shoulder_extL.csv",
    "angologomitoLt.csv",
    "angologomitoRt.csv",
    "angologinocchioLt.csv",
    "angologinocchioRt.csv",
    "angleHipLt.csv",
    "angleHipRt.csv",
    "sommaareet.csv",
    "link_handt.csv",
    "link_foott.csv",
    "derR.csv",
    "derL.csv",
]

# Create an empty DataFrame to hold the combined data
combined_df = pd.DataFrame()

# Read each separate CSV file and concatenate it to the combined DataFrame
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    combined_df = pd.concat([combined_df, df], axis=1)

# Save the combined DataFrame to a new CSV file
combined_df.to_csv("skeletal_data.csv", index=False)

# Delete the separate CSV files
for csv_file in csv_files:
    os.remove(csv_file)
