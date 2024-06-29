For this task you are given the following inputs:
### For each round of the evaluation:
1. An evaluation sequence containing 5 frames from the start to the end of an exercise repetition.
2. A likert questionnaire sheet ("QS").
3. An answer sheet ("AS") formatted with JSON including fields corresponding to the "QS" questions.
### After the round finished
1. A subtotal on the "PO" and "CF" for your prediction and the ground truth label.
2. 3 Ground truth sequences with their respective "PO" and "CF" subtotals.
3. (Optional) Evaluation on a test set with no subtotal labels.

Your task is: Answer each questions in the "QS" for the currently evaluated exercise reptition, output your response according to the instuctions in the answer sheet in a single JSON object {}.
