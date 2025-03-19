---
layout: default
Title: Final Report
---

## Project Summary
The goal is to minimize number of obstacles hit by the duckie and for the duckie having the ability to traverse the terrain smoothly. We will be using DuckieTown's environments, agents, and variables to implement our Algorithm. The input of the project will be data from the cameras or sensors within the environment to traverse the terrain effectively and the output would be the action that is taken by the agent, which is displayed in first-person and will move based on model's output. This navigation system has many applications to other products like zotbots, lidar sensors, radar detection cameras, and etc. 


## Approaches
In this project, we evaluated both baseline and advanced approaches with a focus on transitioning from an old policy consisting of MLP and CNN to a new policy with MLP only. The old policy leverages the CNN for processing raw image data and MLP for decision making of all the parameters involved in the Duckietown environment like velocity, position, yaw, and etc, which was a complex architecture which has resulted in overfitting. To compare the approaches abov, we tracked training progress and performance using TensorBoard, visualizing metrics such as ep_rew_mean and trajectory of the model's learning. In the CNN of our old policy, we tested with ResNet for feature extraction, but soon realized that it was overfitting. 

## Evaluation

## References
- https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html -> PPO algorithm
- Python Libraries
-- Pytorch

## AI Tool Usage
Tensorboard was used to visualize reports of trained models and determine our next steps.
