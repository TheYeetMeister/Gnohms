---
layout: default
title: Status
---
## Evaluation
We conducted extensive training on our PPO (Proximal Policy Optimization) model, accumulating over 1 million training steps. During this process, we recorded key metrics to evaluate the model's performance. The policy gradient loss was -0.00428, and the value loss was 8.28, indicating areas where the model's predictions and policy updates can be further optimized. The learning rate was set to 0.0003 to balance the trade-off between convergence speed and training stability.

In addition to these quantitative metrics, we performed a qualitative assessment of the agent's performance in the Duckietown environment. This included evaluating how often the agent falls off the track, its ability to maintain a straight trajectory, its speed, and its overall navigation behavior. While the agent demonstrated basic lane-following capabilities, there were instances where it struggled with sharp turns or maintaining consistent speed, leading to occasional deviations from the track.

## Remaining Goals and Challenges
Moving forward, we plan to refine the training process and experiment with different reward structures to enhance the agent's decision-making abilities. This will involve optimizing the reward function to encourage smoother navigation, better handling of turns, and improved obstacle avoidance. These adjustments aim to address the current limitations and further improve the agent's performance in the Duckietown environment.

## Resources Used

For our PPO (Proximal Policy Optimization) model, we utilized a Duckietown environment provided by our teaching assistant, JB. In addition to this environment, we leveraged Stable-Baselines3 and PyTorch to develop and train our model.
