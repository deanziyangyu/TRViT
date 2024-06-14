For this task you are given the following inputs:
1. A description of the current exercise (`exercise_desc`). This contains:
    a. Exercise name;
    b. Description of the exersise in stages;
    c. Overall Requirement of the Exersise;
    d. Body Parameters for the patient subject to maximize for the given exercise;
    e. Body Parameters for the patient subject to maintain during the given exercise.
2. For this exercise, 4 ground truth image sequences labeled by professionals. These sequences belong to each respective score class from 0 to 3 (0='Bad', 1='Good', 2='Very Good', 3='Perfect'), and for each video 5 frames from the start to end of a exercise repetition. Refer to these sequences to determine which score the currently evaluated exercise should be given.
3. An answer sheet formatted with JSON.

Your task is: Use `exercise_desc`, and the 4 gound truth sequences, assign a exercise quality score 0 to 3 for the currently evaluated exercise reptition, output your response according to the instuctions in the answer sheet.
