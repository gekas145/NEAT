# Double pole balancing
This task required the ai to learn how to balance 2 poles of length 100 and 250. The poles were positioned vertically and the cart was initially moving to the left with speed of 1. The ai could control the cart by choosing speed from range of [-3, 3] once on every 20 iterations. The ai had scaled cart center position, angular velocities and inclination angles of poles as input. The task was failed if one of the poles went off vertical position by more than pi/6 radians or cart got closer than 30 to the field borders. The ai was rewarded by 1 point for each 20 iterations. The task was tried out in 2 versions: with y-gravity of 10(ver3) and 30(ver4).

The learning curve of ver3 looks like this:

<img src="https://github.com/gekas145/NEAT/blob/main/plots/dpb_ver3.png" alt="drawing" width="500" height="400"/>

The champion of ver3 has achieved score of 1001(more than 30 000 iterations) and part of its simulation is presented below.

<img src="https://github.com/gekas145/NEAT/blob/main/recorded_simulations/dpb_ver3.gif" alt="drawing" width="500" height="400"/>

The learning curve of ver4 looks like this:

<img src="https://github.com/gekas145/NEAT/blob/main/plots/dpb_ver4.png" alt="drawing" width="500" height="400"/>

The champion of ver4 has achieved score of 178(more than 3500 iterations) and its simulation is presented below.

<img src="https://github.com/gekas145/NEAT/blob/main/recorded_simulations/dpb_ver4.gif" alt="drawing" width="500" height="400"/>

As one can notice, champions of both versions have learned how to keep the poles balanced. To solve this task neat usually evolved nets with 0 to 1 hidden nodes.