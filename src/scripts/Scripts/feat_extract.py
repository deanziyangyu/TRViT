import os
import sys
import preproc
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks
import matplotlib.pyplot as plt  # Uncomment if you want to plot the results
import preproc
from filtering import *

# Getting access to all the joint positions in preproc.py
Hip_R = preproc.Hip_R
Knee_R = preproc.Knee_R
Ankle_R = preproc.Ankle_R
Foot_R = preproc.Foot_R
Hip_L = preproc.Hip_L
Knee_L = preproc.Knee_L
Ankle_L = preproc.Ankle_L
Foot_L = preproc.Foot_L
Spine_B = preproc.Spine_B
Spine_M = preproc.Spine_M
Head_C = preproc.Head_C
Spine_Sh = preproc.Spine_Sh
Shoulder_R = preproc.Shoulder_R
Shoulder_L = preproc.Shoulder_L
Elbow_R = preproc.Elbow_R
Wrist_R = preproc.Wrist_R
Hand_R = preproc.Hand_R
Elbow_L = preproc.Elbow_L
Wrist_L = preproc.Wrist_L
Hand_L = preproc.Hand_L


# PRIMARY OUTCOME
shoulder_extR = np.arctan2(
    Spine_Sh[:, 2] - Elbow_R[:, 2], Spine_Sh[:, 1] - Elbow_R[:, 1]
) * (180 / np.pi)
shoulder_extL = np.arctan2(
    Spine_Sh[:, 2] - Elbow_L[:, 2], Spine_Sh[:, 1] - Elbow_L[:, 1]
) * (180 / np.pi)

# Removing singularity
for j in range(1, len(shoulder_extR)):
    if (
        shoulder_extR[j] - shoulder_extR[j - 1] < -100
        or shoulder_extR[j] - shoulder_extR[j - 1] > 100
    ):
        shoulder_extR[j] = -shoulder_extR[j]

for j in range(1, len(shoulder_extL)):
    if (
        shoulder_extL[j] - shoulder_extL[j - 1] < -100
        or shoulder_extL[j] - shoulder_extL[j - 1] > 100
    ):
        shoulder_extL[j] = -shoulder_extL[j]

# Filtraggio P.O.
shoulder_extR = filtering(shoulder_extR)
shoulder_extL = filtering(shoulder_extL)


# Peak Detection
sogliaR = max(shoulder_extR) / np.sqrt(2)
sogliaL = max(shoulder_extL) / np.sqrt(2)
nsamples = len(shoulder_extR)
samples = np.arange(1, nsamples + 1)

# Find peaks
maxR, ind_maxR = find_peaks(shoulder_extR, height=sogliaR, distance=nsamples // 12)
minR, ind_minR = find_peaks(
    max(shoulder_extR) - shoulder_extR, height=sogliaR, distance=nsamples // 12
)
minR = max(shoulder_extR) - minR

maxL, ind_maxL = find_peaks(shoulder_extL, height=sogliaL, distance=nsamples // 12)
minL, ind_minL = find_peaks(
    max(shoulder_extL) - shoulder_extL, height=sogliaL, distance=nsamples // 12
)
minL = max(shoulder_extL) - minL


# Uncomment the following lines to plot the results

# Convert indices to integers
int_max_indices = ind_maxR["peak_heights"].astype(int)
int_min_indices = ind_minR["peak_heights"].astype(int)


# # Convert indices to integers after rounding
# int_max_indices = np.round(ind_maxR["peak_heights"]).astype(int)
# int_min_indices = np.round(ind_minR["peak_heights"]).astype(int)

# Plot the data
plt.plot(samples, shoulder_extR, label="underarm right angle")
plt.plot(samples[int_max_indices], maxR, "or", label="local maxima")
plt.plot(samples[int_min_indices], minR, "*g", label="local minima")

# Set labels and title
plt.title("Primary outcome detection exercise 1")
plt.xlabel("Number of samples")
plt.ylabel("Degree")
plt.legend()

# Show the plot
plt.show()


# Control factor

# ELBOW ANGLE
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

angologomitoL = np.arccos(
    (link_avambraccioL**2 + link_braccioL**2 - link_bracciototL**2)
    / (2.0 * link_avambraccioL * link_braccioL)
) * (180 / np.pi)

angologomitoR = np.arccos(
    (link_avambraccioR**2 + link_braccioR**2 - link_bracciototR**2)
    / (2.0 * link_avambraccioR * link_braccioR)
) * (180 / np.pi)

angologomitoLt = angologomitoL[
    :-15
]  # cut the last 15 values from the vector/array related to file acquisition
angologomitoRt = angologomitoR[:-15]

# KNEE ANGLE

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

angologinocchioL = np.arccos(
    (link_tibiaL**2 + link_femoreL**2 - link_gambatotL**2)
    / (2.0 * link_tibiaL * link_femoreL)
) * (180 / np.pi)

angologinocchioR = np.arccos(
    (link_tibiaR**2 + link_femoreR**2 - link_gambatotR**2)
    / (2.0 * link_tibiaR * link_femoreR)
) * (180 / np.pi)

angologinocchioLt = angologinocchioL[
    :-15
]  # cut the last 15 values from the vector/array

angologinocchioRt = angologinocchioR[
    :-15
]  # cut the last 15 values from the vector/array

# ANGLE C

angleHipL = np.arctan2(Spine_B[:, 0] - Hip_L[:, 0], Spine_B[:, 1] - Hip_L[:, 1]) * (
    180 / np.pi
)  # (HALF ANGLE C) angle reported in degrees between the left hip and lower spine

angleHipR = np.arctan2(Hip_R[:, 0] - Spine_B[:, 0], Hip_R[:, 1] - Spine_B[:, 1]) * (
    180 / np.pi
)  # (HALF ANGLE C) angle reported in degrees between the right hip and lower spine

angleHipRt = angleHipR[:-15]  # cut the last 15 values from the vector/array
angleHipLt = angleHipL[:-15]  # cut the last 15 values from the vector/array

# AEREA TRONCO

link_shoulder = np.sqrt(
    (Shoulder_L[:, 0] - Shoulder_R[:, 0]) ** 2
    + (Shoulder_L[:, 1] - Shoulder_R[:, 1]) ** 2
    + (Shoulder_L[:, 2] - Shoulder_R[:, 2]) ** 2
)  # distance between shoulders

link_hip = np.sqrt(
    (Hip_L[:, 0] - Hip_R[:, 0]) ** 2
    + (Hip_L[:, 1] - Hip_R[:, 1]) ** 2
    + (Hip_L[:, 2] - Hip_R[:, 2]) ** 2
)  # distance between hips

link_shoulderhipR = np.sqrt(
    (Shoulder_R[:, 0] - Hip_R[:, 0]) ** 2
    + (Shoulder_R[:, 1] - Hip_R[:, 1]) ** 2
    + (Shoulder_R[:, 2] - Hip_R[:, 2]) ** 2
)  # distance between right shoulder and hip

link_shoulderhipL = np.sqrt(
    (Shoulder_L[:, 0] - Hip_L[:, 0]) ** 2
    + (Shoulder_L[:, 1] - Hip_L[:, 1]) ** 2
    + (Shoulder_L[:, 2] - Hip_L[:, 2]) ** 2
)  # distance between left shoulder and hip

link_shoulderR_hipL = np.sqrt(
    (Shoulder_R[:, 0] - Hip_L[:, 0]) ** 2
    + (Shoulder_R[:, 1] - Hip_L[:, 1]) ** 2
    + (Shoulder_R[:, 2] - Hip_L[:, 2]) ** 2
)  # distanza tra spalla destra anca sinistra

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

sommaaree = (
    areaeroneR + areaeroneL
)  # calculation of the area of a truncated shape using the Heron's method

sommaareet = sommaaree[:-15]

# joint of the hands

link_hand = np.sqrt(
    (Hand_R[:, 0] - Hand_L[:, 0]) ** 2
    + (Hand_R[:, 1] - Hand_L[:, 1]) ** 2
    + (Hand_R[:, 2] - Hand_L[:, 2]) ** 2
)  # distance between hands

link_handt = link_hand[:-15]  #  cut the last 15 values from the vector/array

# LINK BETWEEN THE ANKLES

link_foot = np.sqrt(
    (Ankle_R[:, 0] - Ankle_L[:, 0]) ** 2
    + (Ankle_R[:, 1] - Ankle_L[:, 1]) ** 2
    + (Ankle_R[:, 2] - Ankle_L[:, 2]) ** 2
)  # distance between ankles

link_foott = link_foot[:-15]

# REGOLARITA'

peak_heights_R = ind_maxR["peak_heights"]
derR = np.diff(peak_heights_R)

peak_heights_L = ind_maxL["peak_heights"]
derL = np.diff(peak_heights_L)


plt.plot(derR, "r", label="interval P.O. Right")
plt.plot(derL, "b", label="interval P.O. Left")
plt.title("Derivative: Frequency/velocity Variability")
plt.xlabel("Number of interval")
plt.ylabel("Samples-difference")
plt.legend()
plt.show()

# Filtering C.F.
angologomitoLt = filtering(angologomitoLt)
angologomitoRt = filtering(angologomitoRt)
angologinocchioLt = filtering(angologinocchioLt)
angologinocchioRt = filtering(angologinocchioRt)
angleHipRt = filtering(angleHipRt)
angleHipLt = filtering(angleHipLt)
sommaareet = filtering(sommaareet)
link_handt = filtering(link_handt)
link_foott = filtering(link_foott)


# print(samples)


## TODO: look into deleting some of the codes below

# Uncomment the following lines to plot the results
# plt.plot(samples, shoulder_extR)
# plt.plot(samples[ind_maxR], maxR, "or")
# plt.plot(samples[ind_minR], minR, "*g")
# plt.title("Primary outcome detection exercise 1")
# plt.xlabel("Number of samples")
# plt.ylabel("Degree")
# plt.legend(["underarm right angle", "local maxima", "local minima"])
# plt.show()


# print(ind_maxR)
# print(maxR)


# # Define a list of arrays
# arrays = [
#     shoulder_extR,
#     shoulder_extL,
#     angologomitoLt,
#     angologomitoRt,
#     angologinocchioLt,
#     angologinocchioRt,
#     angleHipLt,
#     angleHipRt,
#     sommaareet,
#     link_handt,
#     link_foott,
#     derR,
#     derL,
# ]

# # Define a list of corresponding column names
# column_names = [
#     "shoulder_extR",
#     "shoulder_extL",
#     "angologomitoLt",
#     "angologomitoRt",
#     "angologinocchioLt",
#     "angologinocchioRt",
#     "angleHipLt",
#     "angleHipRt",
#     "sommaareet",
#     "link_handt",
#     "link_foott",
#     "derR",
#     "derL",
# ]


# # Save each array into a separate CSV file
# for i in range(len(arrays)):
#     data = {column_names[i]: arrays[i]}
#     df = pd.DataFrame(data)
#     df.to_csv(f"{column_names[i]}.csv", index=False)


# import pandas as pd

# # List of separate CSV files
# csv_files = [
#     "shoulder_extR.csv",
#     "shoulder_extL.csv",
#     "angologomitoLt.csv",
#     "angologomitoRt.csv",
#     "angologinocchioLt.csv",
#     "angologinocchioRt.csv",
#     "angleHipLt.csv",
#     "angleHipRt.csv",
#     "sommaareet.csv",
#     "link_handt.csv",
#     "link_foott.csv",
#     "derR.csv",
#     "derL.csv",
# ]

# # Create an empty DataFrame to hold the combined data
# combined_df = pd.DataFrame()

# # Read each separate CSV file and concatenate it to the combined DataFrame
# for csv_file in csv_files:
#     df = pd.read_csv(csv_file)
#     combined_df = pd.concat([combined_df, df], axis=1)

# # Save the combined DataFrame to a new CSV file
# combined_df.to_csv("skeletal_data.csv", index=False)

# # Delete the separate CSV files
# for csv_file in csv_files:
#     os.remove(csv_file)

# print(angleHipR)


# derR = np.diff(ind_maxR) #not needed
# derL = np.diff(ind_maxL) #not needed
