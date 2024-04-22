import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

def main():
    figure, ax = plt.subplots()

    '----------Meeting Room-----------'
    stepLength = ['50', '60', '80', '90', '100']
    MyScheme = [71.47136225, 78.68464304, 99.78410973, 110.990131, 119.6762769]
    FL_MLP = [20.93867961, 42.16923247, 62.46897964, 85.2855522, 106.4258117]
    ILM_CFBCS = [32.28458502, 59.04185449, 87.4074918, 117.4512801, 141.0272177]
    GA_IPP = [35.44025893, 35.86367859, 36.15181823, 38.01079649, 38.46924296]
    A3C_IPP = [70.33484729, 79.62861346, 100.1454124, 111.9249254, 121.0303124]

    # '----------Lab-----------'
    # stepLength = ['130', '150', '180', '200']
    # MyScheme = [156.6539896, 181.8982608, 222.3739552, 253.3521922]
    # FL_MLP = [78.31608537, 114.7778259, 150.5364862, 187.0944393]
    # ILM_CFBCS = [89.99210586, 129.0205603, 168.9104342, 207.0822966]
    # GA_IPP = [106.5495205, 108.1446887, 135.1763291, 106.0618964]
    # A3C_IPP = [157.7788654, 183.4583055, 225.8689418, 253.3521922]

    plt.plot(stepLength, MyScheme, color='r', marker='o', label='Proposed Scheme')
    plt.plot(stepLength, FL_MLP, color='b', marker='v', label='FL-MLP')
    plt.plot(stepLength, ILM_CFBCS, color='green', marker='x', label='ILM-CFBCS')
    plt.plot(stepLength, GA_IPP, color='c', marker='p', label='GA-IPP')
    plt.plot(stepLength, A3C_IPP, color = 'orange', marker = '+', label = 'A3C-IPP')

    # plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    # plt.rcParams.update({'font.size': 13})
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 12,
             }
    plt.xlabel('Budget', font2, size=15)
    plt.ylabel('Total Reward', font2, size=15)
    plt.grid(color="grey", linestyle=':', linewidth=0.5)
    plt.tick_params(labelsize=15)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    plt.legend(loc='upper left', prop=font2)
    # plt.savefig('Reward_Compare_Meet.pdf', bbox_inches='tight')
    # plt.ylim(15, 130)
    plt.show()

if __name__ == '__main__':
    main()