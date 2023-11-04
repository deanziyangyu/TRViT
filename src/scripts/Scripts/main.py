import os
import sys
import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks
from scipy.signal import butter, filtfilt
import filtering
import feat_extract
import preproc


# Directory containing the CSV files (relative path)
directory = "./Raw"

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


# Convert the DataFrame to a NumPy array
Joint_Position = Joint_Position.to_numpy()
Joint_Orientation = Joint_Orientation.to_numpy()


# Calling the filtering and preprocessing modules
filtering
preproc
