# Pole balancing

This task required the ai to learn how to balance single pole of length 177. The pole had initial inclination angle of -0.27 radians, and the cart was initially still. The ai could control the cart by choosing moving direction(read set cart speed to -1 or 1) on every 20 iterations. The ai had scaled cart center position, angular velocity and inclination angle of pole as input. The task was failed the pole went off vertical position by more than pi/6 radians or cart got closer than 60 to the field borders. The ai was rewarded by 1 point for each 20 iterations.

<p float="left">
  <img src="https://github.com/gekas145/NEAT/blob/main/plots/pb_ver3.png" alt="drawing" width="500" height="400"/>
  <img src="https://github.com/gekas145/NEAT/blob/main/plots/pb_ver3_defeat_causes.png" alt="drawing" width="500" height="400"/>
</p>

On the right graph one can see that majority of the population has learned how to balance and was mainly loosing because of going off the field constraints. Learning of how to avoid the field edges was pretty hard as at the very beginning organisms only learn how to balance the pole and rarely get to the edges. There was a try to increase the reward if cart center remained "not far" from the field center, but it was only helpful for learning where the center is, not how to the avoid field edges.

The ultimate champion has achieved score of 1319(more than 26 000 iterations) and part of its simulation is presented below.

<img src="https://github.com/gekas145/NEAT/blob/main/recorded_simulations/pb_ver3.gif" alt="drawing" width="500" height="400"/>