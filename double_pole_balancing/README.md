# Double pole balancing
This task required the ai to learn how to balance 2 poles of length 100 and 250. The poles were positioned vertically and the cart was initially moving to the left with speed of 1. The ai could control the cart by choosing speed from range of [-3, 3] once on every 20 iterations. The task was failed if one of the poles went off vertical position by more than pi/6 radians or cart got closer than 30 to the field borders. The ai was rewarded by 1 point for each 20 iterations. The task was tried out in 2 versions: with y-gravity of 10 and 30.

The learning curve looks like this:

<img src="plots/dpb_ver3.png" alt="drawing" width="200" height="200"/>

The champion of lighter version with y-gravity of 10 has achieved score of 1001(more than 30 000 iterations).
