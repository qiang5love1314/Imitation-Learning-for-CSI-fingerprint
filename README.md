# Imitation-Learning-for-CSI-fingerprint
 
This repository contains the code for a submitted paper to the IEEE journal, and the codes are only available to the editors and reviewers.

# Dependencies
Before using this code, you need to install the following dependencies:
```
pip install -r requirements.txt
```

# Usage
To use the dataset, look at [CSI-dataset](https://github.com/qiang5love1314/CSI-dataset). In this paper, we used the CSI data of the lab and meeting room. Moreover, we provide two additional fingerprint database data sets for the new environments (mini lab and conference room) to show the portability of the proposed algorithm.

## Example

The main files are the [imitationLearn_Lab.py](https://github.com/qiang5love1314/Imitation-Learning-for-CSI-fingerprint/blob/main/imitationLearn_Lab.py) and [imitationLearn_Meet.py](https://github.com/qiang5love1314/Imitation-Learning-for-CSI-fingerprint/blob/main/imitationLearn_Meet.py).

In addition, the paper also utilizes our previous work [Path Planning for Adaptive CSI Map Construction With A3C in Dynamic Environments](https://ieeexplore.ieee.org/abstract/document/9629332) for obtaining the optimal path, and you can refer to the [code](https://github.com/qiang5love1314/Path-planning-based-on-A3C) for more details.

Here is a GIF to show the process of dynamically searching for the optimal path.
<p align="center">
<img src="https://github.com/qiang5love1314/Imitation-Learning-for-CSI-fingerprint/blob/main/searchPath.GIF", width="300" height="300">
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="https://github.com/qiang5love1314/Imitation-Learning-for-CSI-fingerprint/blob/main/lab.jpg", width="350" height="300">
</p>
<p align="left">Figure 1: Searching the optimal path. &nbsp;&nbsp; Figure 2: The corresponding result.</p>

## Arguments
```
iterations: Number of training iterations (default is 100).
learning_rate: Learning rate for the optimizer (default is 1e-2).
input_dim: Dimension of the input data (default is 32).
hidden_dim: Dimension of the hidden layers in the model (default is 64).
latent_dim: Dimension of the latent space in the model (default is 32).
num_segments: Number of segments to divide the time series into (default is 10).
step_length: Number of the maximum exploration step length (default is 100).
n_neighbors: Number of neighbors for KNN (default is 5).
```

## License
[MIT](LICENSE) © Xiaoqiang Zhu
