1. # Primany Outcome ("PO") and Control Factor ("CF")
- A Rehablitation Exercise is evaluated using two main metrics: Primary Outcome ("PO") and Control Factor ("CF"). These exercise-specific metrics are quantitatively described by body segments, distances between anatomical landmarks, and relative angles between the segments.
- Primary Outcomes (PO): These are the primary goals of the exercises and are quantified by body descriptors that change to achieve the exercise goal. Typically, this involves maximizing a body parameter, such as achieving maximum knee flexion.
- Control Factors (CF): These are physical constraints that must be maintained during the exercise. These constraints often involve the fixation or alignment of a body segment (head/neck, trunk, arms, pelvis, and legs) to anatomical landmarks, such as maintaining correct trunk alignment along the sagittal plane.

2. # About the Questionnaire Sheet ("QS")
- The "QS" is a Likert questionnaire sheet used to evaluate the subject's exercise accuracy concerning the "CFs" and "POs" during a repetition, which is presented to you as a 5-frame image sequence of the subject ("evaluation sequence").
- Every question in "QS" is in likert scale from 1 to 5 (1=Never, 2=Rarely, 3=Sometimes, 4=Often, 5=Always).
- Each "QS" starts with the exercise name and description, including `exercise_stages` which will imform the "PO" metrics, and `body segment terminology` which explain the body parameters in simpler terms.
- The `PO_questions` section measures the degree of achievement on the exercise goals, corresponding to the "PO" metrics.
- The `CF_questions` section measures the degree of control on the postures of seven body segments, corresponding to the "CF" metrics.
- Both sections contain question prefixed with letters (a to z) and numbers (1 to 10):
    - The a to z lettered questions are quantitative and exercise-specific. Carefully observe the evaluation sequence before answering these questions.
    - The 1 to 10 numbered questions are qualitatively and exercise-agnostic. Summarize the patient's overall consistency and body segment accuracy based on the lettered questions. Your answer for these questions will be compared to the ground truth.

3. # Guidelines for Answering the "QS"
- Carefully answer each question in the "QS" by providing your level of agreement or disagreement with the statement based on the evaluation sequence in likert scale. Be strict and impartial in your assessment of the subject's exercise accuracy.
- Answer the `PO_questions` by analyzing the entire movement in the evaluation sequence. Refer to the `exercise_stages` in "QS" to determine if the subject achieves the exercise primary goals. Evaluate the "PO" metrics qualitatively and rigorously with logical reasoning.
- Answer the `CF_questions` by quantifying and counting the number of frames (out of 5) where maintained of the "CF" is achieved. For example: 5 = Condition maintained in ALL 5 frames; 0 = Condition maintained in NONE of the frames.
- For you first evaluation, the default answer for the lettered questions is set to 2 to prevent untruthful biasing towards the higher scores. Only answer with higher score if you really believe the subject's accuracy is sufficiently higher than the default answer.

4. # Going Past Your First (Zero-shot) evaluation
- After your initial unaided evaluation, you will receive the ground truth answers labeled by an expert human clinician and the percentage of over- or underestimation your answer will be against the ground truth.
- The annotation labels will include the subtotal of numbered questions 1 to 3 in `PO_questions`, the subtotal of numbered questions 4 to 10 in `CF_questions`, and the total combined score.
- Observe how your answers compare to the ground truth and consider improvements for future evaluations.
- You will receive 3 additional ground truth sequences with the corresponding "PO" and "CF" scores to aid your understanding.
- After reviewing this additional data, you may be asked to evaluate more sequences to further test your ability without knowing the answers in advance.

5. # Repeating the Evaluation Cycle
- Repeat steps 3 and 4 for multiple evaluation cycles.
- Compare your evaluations with the ground truths, learn from the additional sequences, and aim to improve your accuracy over time.

# Additionals
- All subjects' faces are blurred for privacy.
- Some subjects may not face the camera directly, so account for perspective shifts when answering the questions.
- If a body segment is not visible due to image cropping or blurring, determine where the segment should be based on the posture of neighboring/connecting body segments. Make a note in the `reasoning` field in your response that the body segment is not visible.
- The subject holds a bar between their hands for some exercises. Ignore the bar during the evaluation.