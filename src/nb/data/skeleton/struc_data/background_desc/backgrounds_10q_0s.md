1. Image sequences/videos: For this exercise, 1 evaluation sequence is provided. Each sequence contain 5 frames sampled from the start to the stop of an exercise. The frames consist one patient subject and a background; evaluate and score base on the patients' exercise performance only.
2. 4 ground truth image sequences with the same specification are optionally provided. The ground truth sequences belong to each respective score class from 0 to 3 ('Bad'/'Good'/'Very Good'/'Perfect'). Ignore this information if the groundtruth is not provided.
3. The score for the evaluation sequence is currently unknown and determined by you through analytical reasoning.
4. Exercise Performance is evaluated and scored by a questionnaire sheet containing 10 questions, with the questions themselves refering to an Exercise Description (`exercise_desc`) which will be provided later. Exercise repetitions which better adhere to the Exercise Discription criteria should  scored higher, while repetitions that do not match these criteria scored lower.
5. You are to answer each question in the questionnaire sheet with the number 1 to 5 (1=Never, 2=Rarely, 3=Sometimes, 4=Often, 5=Always), based on the situation provided by the Exercise Description.

Additional things to consider during evaluation, especially when facing extreme cases:
6. All subjects' faces has been blurred for privacy. In cases where the subject in the frame might be incomplete due to image cropping, evaluate their on the body parts in the image for 
7. The subject holds a bar between their hands for exercise 1, 2, 3, and 5. Ignore the bar during the evaluation.
