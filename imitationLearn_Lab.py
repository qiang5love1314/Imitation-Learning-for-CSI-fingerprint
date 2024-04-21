#coding=UTF-8
import os
import numpy as np
from scipy.io import loadmat, savemat
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.cross_decomposition import PLSRegression
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import WhiteKernel,ExpSineSquared,RBF
import GPy
from probrnn import models
import modules
import argparse
import torch
import utils
from torch.utils.data import DataLoader
import time
stateFile = "state-200_NN200.mat"
rewardFile = "reward-200_NN200.mat"

def getOriginalCSI():
    xLabel = getXlabel()
    yLabel = getYlabel()
    count = 0
    originalCSI = np.zeros((317, 3 * 30 * 1500), dtype=np.float)
    newName = []
    label = np.empty((0, 2), dtype=np.int)

    for i in range(21):
        for j in range(23):
            filePath = "/Users/zhuxiaoqiang/Downloads/我的定位数据集/47SwapData/coordinate" + xLabel[i] + yLabel[j] + ".mat"
            name = xLabel[i] + yLabel[j]
            if (os.path.isfile(filePath)):
                c = loadmat(filePath)
                CSI = np.reshape(c['myData'], (1, 3 * 30 * 1500))
                originalCSI[count, :] = CSI
                newName.append(name)
                label = np.append(label, [[int(xLabel[i]), int(yLabel[j])]], axis=0)
                count += 1
    return originalCSI, label, count

def getXlabel():
    xLabel = []
    for i in range(21):
        str = '%d' % (i + 1)
        xLabel.append(str)
    return xLabel

def getYlabel():
    yLabel = []
    for j in range(23):
        if (j < 9):
            num = 0
            str = '%d%d' % (num, j + 1)
            yLabel.append(str)
        else:
            yLabel.append('%d' % (j + 1))
    return yLabel

def generatePilot():
    originalCSI, label, count = getOriginalCSI()
    originalData = np.array(originalCSI[:, 0:3 * 30 * 900:5400], dtype='float')  # 317*15
    originalData = SimpleImputer(strategy='mean').fit_transform(originalData)
    rng = np.random.RandomState(20)
    randomLabel = rng.randint(1,317, size=32)   #32 63 95 126 158
    labelIndex = np.sort(randomLabel)
    listCSI = originalData[labelIndex,:]
    return label[labelIndex], listCSI

def findIndex(label, pathPlan):
    index = []
    for i in range(len(pathPlan)):
        index1 = np.where(label[:, 0] == pathPlan[i][0])
        index2 = np.where(label[:, 1] == pathPlan[i][1])
        similar = list(set(index1[0]).intersection(set(index2[0])))
        index.append(similar)
    index = [x for x in index if x]  # 删除空元素
    return index

def filterProcess(mulGauProPrediction, n_iter):
    from pykalman import KalmanFilter
    from scipy import signal
    bufferCSI = np.zeros((len(mulGauProPrediction), len(mulGauProPrediction[0])), dtype=np.float)
    b, a = signal.butter(2, 3 * 2 / 50, 'lowpass')
    for i in range(len(mulGauProPrediction)):
        kf = KalmanFilter(transition_matrices=[1], observation_matrices=[1])
        measurements = mulGauProPrediction[i]
        kf = kf.em(measurements, n_iter=n_iter)
        (filtered_state_means, filtered_state_covariances) = kf.filter(measurements)
        swap = filtered_state_means[:, 0]
        finalResult = signal.filtfilt(b, a, swap)
        bufferCSI[i, :] = finalResult
    return bufferCSI

def isOdd(n):
    if int(n)%2==1:
        return int(n)
    else:
        return int(n)-1

def find_close_fast(arr, e):
    low = 0
    high = len(arr) - 1
    idx = -1
    rng = np.random.RandomState(20)
    randomInt = rng.randint(len(errorBand[0]))

    while low <= high:
        mid = int((low + high) / 2)
        if e[randomInt,0] == arr[mid] or mid == low:
            idx = mid
            break
        elif e[randomInt,0] > arr[mid]:
            low = mid
        elif e[randomInt,0] < arr[mid]:
            high = mid
    if idx + 1 < len(arr) and abs(e[randomInt,0] - arr[idx]) > abs(e[randomInt,0] - arr[idx + 1]):
        idx += 1

    return arr[idx]

def tensorData(professionalData, device):
    lengths = torch.tensor(list(map(len, professionalData)))
    lengths = lengths.to(device)

    data = []
    for i in range(len(professionalData)):
        TensorResult = torch.tensor(abs(professionalData[i]), dtype=torch.int64)
        data.append(TensorResult)
    inputs = torch.nn.utils.rnn.pad_sequence(data, batch_first=True)
    inputs = inputs.to(device)
    return inputs, lengths

def completionData(rec, pilotCSI):
    recArray = np.zeros((len(rec), len(rec[0] - 1)), dtype=np.int)
    for i in range(len(rec)):
        transfer = np.array(rec[i])
        recArray[i, :] = transfer
    recArray = np.column_stack((recArray, pilotCSI[:, -1]))
    return recArray

def parameterSet():
    parser = argparse.ArgumentParser()
    parser.add_argument('--iterations', type=int, default=100)
    parser.add_argument('--learning_rate', type=float, default=1e-2)
    parser.add_argument('--input_dim', type=int, default=32)
    parser.add_argument('--hidden_dim', type=int, default=64)
    parser.add_argument('--latent_dim', type=int, default=64)
    parser.add_argument('--num_segments', type=int, default=15)
    parser.add_argument('--no-cuda', action='store_true', default=False)
    parser.add_argument('--latent_dist', type=str, default='concrete') # it also can be gaussian
    args = parser.parse_args()
    return args

def findPossiblePath(stateFile):
    possiblePath = []
    stateLabel = []
    state = loadmat(r"/Users/zhuxiaoqiang/Desktop/IEEE Trans/Fifth code/"+ stateFile)
    stateList = np.reshape(state['array'], (100, 200, 2))
    for i in range(100):
        a = np.array(stateList[i]).tolist()
        list.append(a, [1,1])
        new_list = [list(t) for t in set(tuple(xx) for xx in a)]
        new_list.sort()
        if [1,1] and [21,23] in new_list:
            possiblePath.append(new_list)
            stateLabel.append(i)
    return possiblePath, stateLabel

def OptimalPath(rewardFile):
    possiblePath, stateLabel = findPossiblePath(stateFile)
    reward = loadmat(r"/Users/zhuxiaoqiang/Desktop/IEEE Trans/Fifth code/" + rewardFile)
    rewardList = reward['array'][0]
    numOfpath = len(stateLabel)
    valueOfReward = []
    for i in range(numOfpath):
        valueOfReward.append(rewardList[stateLabel[i]])
    max_index = np.argmax(np.array(valueOfReward))
    OptimalPath = possiblePath[int(max_index)]
    return OptimalPath, np.max(valueOfReward)

def accuracyPre(predictions, labels):
    return  np.mean(np.sqrt(np.sum((predictions-labels)**2,1))) * 50 / 100

def accuracyStd(predictions , testLabel):
    error = np.asarray(predictions - testLabel)
    sample = np.sqrt(error[:, 0] ** 2 + error[:, 1] ** 2) * 50 / 100
    return np.std(sample)

def saveTestErrorMat(predictions, testLabel, fileName):
    error = np.asarray(predictions - testLabel)
    sample = np.sqrt(error[:, 0] ** 2 + error[:, 1] ** 2) * 50 / 100
    savemat(fileName+'.mat', {'array': sample})

if __name__ == '__main__':

    "生成飞行数据"
    originalCSI, label, count = getOriginalCSI()
    pilotLabel, pilotCSI = generatePilot()
    # print(pilotLabel)
    "多元高斯回归过程"
    mean = np.mean(pilotLabel, axis=1)
    covMatrix = np.cov(pilotCSI)
    # OneDimension = np.diag(covMatrix)
    kernelRBF = GPy.kern.RBF(input_dim=2, variance=1)
    omiga = kernelRBF.K(pilotLabel, pilotLabel)
    kernelPilot = covMatrix * omiga
    np.random.seed(0)
    mulGauProPrediction = np.random.multivariate_normal(mean, kernelPilot, size=len(label))
    # model = GPy.models.GPRegression(pilotLabel, pilotCSI, kernel=kernelRBF)
    # model.optimize()
    # predictionList = model.predict(label)[0]
    # print(predictionList)
    # print(mulGauProPrediction)

    # trainData, testData, trainLabel, testLabel = train_test_split(originalCSI, label, test_size=0.2, random_state=20)

    # '-------最小二乘可做对比实验--------'
    # plsModel = PLSRegression(n_components=2).fit(trainData, trainLabel)
    # plsPrediction = plsModel.predict(testData)
    # print(plsPrediction)

    "滤波平滑处理"
    bufferCSI = filterProcess(mulGauProPrediction, n_iter=2)

    "state space model修正飞行数据"
    import statsmodels.api as sm
    meanError = np.mean(pilotCSI, axis=0)  #列平均
    newModel = sm.tsa.SARIMAX(meanError, order=(1,0,0), trend='c')
    results = newModel.fit(disp=False)
    predict_sari = results.get_prediction()

    "误差变量即CSI变动范围，3 Antenna * 5 Packet"
    errorBand = predict_sari.conf_int()

    "对多元高斯回归预测结果进行修正"
    # from statsmodels.tsa.vector_ar.vecm import VECM
    # VECMModel = VECM(endog=np.transpose(bufferCSI)[0:15], exog_coint=errorBand) #, exog_coint=errorBand
    # res = VECMModel.fit()
    # X_pred = res.predict(exog_coint_fc=errorBand)
    # plt.plot(np.transpose(X_pred))
    # plt.show()

    "由errorBand的最小值对备选序列进行约束处理"
    from scipy.signal import savgol_filter
    filterMatrix = bufferCSI
    for i in range(len(bufferCSI)):
        sliding_window = isOdd(find_close_fast(bufferCSI[i], errorBand))    #寻找每个序列与ErrorBand最接近的元素作为滑动窗口
        tmp_result = savgol_filter(bufferCSI[i], sliding_window, 2)
        filterMatrix[i,:] = tmp_result
    # plt.plot(filterMatrix)
    # plt.show()

    "A3C路径规划"
    pathPlan, maxReward = OptimalPath(rewardFile)
    # print(pathPlan)
    "模仿学习模块"
    args = parameterSet()
    args.cuda = not args.no_cuda and torch.cuda.is_available()
    device = torch.device('cuda' if args.cuda else 'cpu')
    imitationModel = modules.CompILE(
                    input_dim=args.input_dim + 1,
                    hidden_dim=args.hidden_dim,
                    latent_dim=args.latent_dim,
                    max_num_segments=args.num_segments,
                    latent_dist='gaussian').to(device)
    optimizer = torch.optim.Adam(imitationModel.parameters(), lr=args.learning_rate)

    print('Imitation Training...')

    "模仿行为的真实数据"
    index_A3CPredict = np.array(findIndex(label, pathPlan)).flatten()
    index = np.array(findIndex(label, pilotLabel)).flatten()
    index_GaussianAndA3C = np.sort(list(set(np.append(index_A3CPredict,index,axis=0))))
    pilotCSI = originalCSI[index_GaussianAndA3C, 0:3 * 30 * 900 : 5400]

    inputs, lengths = tensorData(pilotCSI, device)

    "学习处理的预测数据"
    processCSI, length_processCSI = tensorData(filterMatrix, device)

    "由真实飞行数据训练模型，再去模仿预测其余CSI数据分布"
    for step in range(args.iterations):
        batch_loss = 0
        batch_acc = 0
        optimizer.zero_grad()

        imitationModel.train()
        outputs = imitationModel.forward(inputs, lengths)
        loss, nll, kl_z, kl_b = utils.get_losses(inputs, outputs, args)

        loss.backward()
        optimizer.step()

        if step % 5 == 0:
            imitationModel.eval()
            outputs = imitationModel.forward(inputs, lengths)
            acc, rec = utils.get_reconstruction_accuracy(inputs, outputs, args)

            batch_acc += acc.item()
            batch_loss += nll.item()
            print('step: {}, nll_train: {:.6f}, rec_acc_eval: {:.3f}'.format(step, batch_loss, batch_acc))
            # print('original sample: {}'.format(inputs[-1, :lengths[-1] - 1]))
            # print('reconstruction: {}'.format(rec[-1]))
            coefficient = batch_acc #置信度

    "补齐数组添加列元素，由飞行数据决定"
    recArray = completionData(rec, pilotCSI)

    "预测全局CSI数据分布"
    NewOutputs = imitationModel.forward(processCSI, length_processCSI)
    NewAcc, NewRec = utils.get_reconstruction_accuracy(processCSI, NewOutputs, args)
    globalArray = completionData(NewRec, filterMatrix)[:,0:15]

    "真实数据替换部分预测数据"
    globalArray[index_GaussianAndA3C,:] = pilotCSI

    "使用置信度权衡预测结果，置信度数值由模仿学习的准确度决定"
    delta = 0.2
    thirdFinger= (coefficient - delta) * globalArray + (1 - coefficient + delta) * filterMatrix[:,0:15]
    # print(thirdFinger)

    "Effectiveness without imitation learning, just using GPR and path planning"
    withoutImitation = filterMatrix[:, 0:15]
    withoutImitation[index_GaussianAndA3C, :] = originalCSI[index_GaussianAndA3C, 0:3 * 30 * 900 : 5400]

    "定位性能测试"
    traindata1, testdata1, trainlabel1, testlabel1 = train_test_split(thirdFinger, label, test_size=0.2, random_state=3)
    from sklearn.neighbors import KNeighborsRegressor
    KNN = KNeighborsRegressor(n_neighbors=12).fit(traindata1, trainlabel1)
    time_start = time.time()
    prediction = KNN.predict(testdata1)
    Training_time = time.time() - time_start

    print(accuracyPre(prediction, testlabel1), 'm')
    print(accuracyStd(prediction, testlabel1), 'm')
    print(Training_time, 's')
    # saveTestErrorMat(prediction, testlabel1, 'Predict-Lab-Error')
