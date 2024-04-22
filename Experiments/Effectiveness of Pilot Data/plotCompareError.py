import numpy as np
from scipy.io import loadmat
import matplotlib.pyplot as plt

def main():
    figure, ax = plt.subplots()
    stepLength = [ '10%', '20%', '30%', '40%', '50%']

    # LabError = [ 3.602911945, 3.770844963, 4.148722168, 3.92524759, 3.814280433]
    # LabStd = [ 1.911134429, 1.790430524, 1.801132333, 1.560914034, 1.713434211]
    # ILM_CFBCS_Error = [4.405909196, 4.473565231, 4.465561236, 4.384365733, 4.454022643]
    # ILM_CFBCS_Std = [1.598988059, 1.585393179, 1.592551906, 1.566533179, 1.669642864]
    # GA_IPP_Error = [4.20744, 4.372429694, 4.302842572, 4.53046599, 4.349950232]
    # GA_IPP_Std = [1.88674, 2.241612661, 1.773348401, 1.927077557, 2.036685844]
    # A3C_IPP_Error = [4.19144, 4.207713298, 4.386948909, 4.265934082, 4.551802152]
    # A3C_IPP_Std = [1.95162, 2.025731054, 2.042667807, 1.943923264, 2.137500801]

    MeetingError = [2.983876835, 3.193750054, 3.116716737, 2.929061882, 2.918277863]
    MeetingStd = [1.258760912, 1.630570635, 1.391286016, 1.648088739, 1.585955331]
    ILM_CFBCS_Error = [3.013035429, 3.031050172, 2.972893436, 2.959183675, 2.903112364]
    ILM_CFBCS_Std = [1.083406062, 1.198538907, 1.229369836, 1.087027335, 1.189681646]
    GA_IPP_Error = [3.17754203, 2.985528203, 2.917559635, 3.193142927, 3.352931412]
    GA_IPP_Std = [1.402150723, 1.632734318, 1.70524068, 1.614013087, 1.743402118]
    A3C_IPP_Error = [3.11982, 2.987948805, 3.16458594, 3.431362982, 3.281716516]
    A3C_IPP_Std = [1.13717, 1.42960202, 1.565182362, 1.45744574, 2.040376609]

    plt.errorbar(stepLength, MeetingError, MeetingStd, fmt='-o', ecolor='r', color='r', elinewidth=1, capsize=3, label='Proposed Scheme')
    plt.errorbar(stepLength, ILM_CFBCS_Error, ILM_CFBCS_Std, fmt='-v', ecolor='b', color='b', elinewidth=1, capsize=3, label='ILM-CFBCS')
    plt.errorbar(stepLength, GA_IPP_Error, GA_IPP_Std, fmt='-x', ecolor='green', color='green', elinewidth=1, capsize=3, label='GA-IPP')
    plt.errorbar(stepLength, A3C_IPP_Error, A3C_IPP_Std, fmt='-p', ecolor='c', color='c', elinewidth=1, capsize=3, label='A3C-IPP')
    # fmt:'o' ',' '.' 'x' '+' 'v' '^' '<' '>' 's' 'd' 'p'

    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 10,
             }
    # plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    # plt.rcParams.update({'font.size': 15})
    plt.xlabel('Percentage of Pilot data', font2, size=15)
    plt.ylabel('Localization Error (m)', font2, size=15)
    plt.grid(color="grey", linestyle=':', linewidth=0.5)
    plt.tick_params(labelsize=15)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    plt.legend(loc='lower right', prop=font2)
    plt.ylim(0, 6)
    plt.tight_layout()
    # plt.savefig('PilotCompareMeet.pdf', bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    main()