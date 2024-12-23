# Imitation-Learning-for-CSI-fingerprint
## Overview  
This repository contains the implementation of the **algorithm** described in our paper: *"Dynamic Radio Map Construction with Minimal Manual Intervention: A State Space Model-Based Approach with Imitation Learning"*. It combines **imitation learning**, **Gaussian process modeling**, and **state space modeling** to construct and update a highly accurate radio map with minimal manual intervention, enabling efficient and real-time localization.  

## Abstract  
Traditional fingerprint localization methods rely heavily on manual labor to collect data from various scenarios, which is time-consuming and inefficient. Existing path planning strategies attempt to reduce this burden but often fall short due to local optimization and high computational costs.  

To address these limitations, ILRM introduces a novel approach that integrates:  
- **Multivariate Gaussian process modeling** to fit a rough fingerprint database using only a few pilot data points.  
- **State space modeling** to calculate the variation range of pilot data, forming a CSI error band to filter and refine the rough radio map.  
- **Imitation learning** and a confidence coefficient to predict and calibrate the global CSI data distribution.  

Experimental results demonstrate that ILRM outperforms state-of-the-art algorithms in most test cases, achieving low computational complexity, reduced localization error, and significant savings in manual workload.  

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

## Results  
Key findings from our experiments include:  
- **Reduced Manual Effort**: ILRM saves **73.3%** of the manual workload compared to traditional fingerprint collection methods.  
- **High Localization Accuracy**: Outperforms state-of-the-art algorithms with consistently lower localization errors.  
- **Low Computational Complexity**: Efficiently processes large-scale data in dynamic environments.  


## License
[MIT](LICENSE) © Xiaoqiang Zhu

If you use this work for your research, you may want to cite

```
@article{zhu2024dynamic,
  title={{Dynamic Radio Map Construction with Minimal Manual Intervention: A State Space Model-Based Approach with Imitation Learning}},
  author={Zhu, Xiaoqiang and Qiu, Tie and Qu, Wenyu and Zhou, Xiaobo and Shi, Tuo and Xu, Tianyi},
  journal={IEEE Transactions on Big Data},
  pages={1--14},
  year={2024},
  doi={10.1109/TBDATA.2024.3489425}
}
```
