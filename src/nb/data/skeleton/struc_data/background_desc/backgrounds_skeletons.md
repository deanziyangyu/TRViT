1. Views: Each Skeleton graph has two views. The grey box on the left is a frontal view of the patient skeleton, the grey box on the right is a sagittal view of the patient skeleton.
2. Joints and text Labels: There are totally 25 joints captured by the camera, 21 of these has text labels. Every black dot indicates a joint. The head is indicated by a large pale blue dot. The text label that is closest to the dot and of the same color to the skeleton line that passes the dot is the name of the joint.
3. Skeleton lines and colors: 
The skeleton lines and joint labels texts of five portions of the body are labeled by colors respectively: the spine/torso in red, the left arm in blue, the right arm in green, the left leg in cyan, the right leg in magenta.
Note: The saggital view is missing the text labels for the spine/torso skeleton line.

Additional things to consider during evaluation, especially when facing extreme cases:
1. Because the height, limb length of the patient may not be the same as the high-score expert, consider placing more emphasis on param_to_maintain when evaluting the patient against the experts.
2. Because the source skeleton is captured by a depth camera, some fluctuation on joint positions is normal, which means in some occations joints can be at anatomcially impossible positions. These extreme cases should be selectively ignored.
3. The subject holds a bar between their hands for exercise 1 and 2, but it is not visible in the skeleton graph.