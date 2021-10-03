# Double pole balancing
This task required the ai to learn how to balance 2 poles of length 100 and 250. The poles were positioned vertically and the cart was initially moving to the left with speed of 1. The ai could control the cart by choosing speed from range of [-3, 3] once on every 20 iterations. The task was failed if one of the poles went off vertical position by more than pi/6 radians or cart got closer than 30 to the field borders. The ai was rewarded by 1 point for each 20 iterations. The task was tried out in 2 versions: with y-gravity of 10 and 30.

The learning curve of easier version with y-gravity of 10 looks like this:

<img src="https://github.com/gekas145/NEAT/blob/main/plots/dpb_ver3.png" alt="drawing" width="500" height="400"/>

The champion of easier version with y-gravity of 10 has achieved score of 1001(more than 30 000 iterations) and part of its simulation is presented below.

<img src="https://github.com/gekas145/NEAT/blob/main/recorded_simulations/dpb_ver3.gif" alt="drawing" width="500" height="400"/>

The learning curve of harder version with y-gravity of 30 looks like this:

<img src="https://github.com/gekas145/NEAT/blob/main/plots/dpb_ver4.png" alt="drawing" width="500" height="400"/>

The champion of harder version with y-gravity of 30 has achieved score of 178(more than 3500 iterations) and part of its simulation is presented below.

<img src="https://github.com/gekas145/NEAT/blob/main/recorded_simulations/dpb_ver4.gif" alt="drawing" width="500" height="400"/>