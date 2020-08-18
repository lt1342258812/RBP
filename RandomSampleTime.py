from scapy.all import *
import random
import numpy as np


def Random_Iat_List(pcaps):
    # pcaps：文件名,end_num:结束数据包序号，random_num:提取随机iat的个数,n:取iat后n位
    n = 18
    end_num = len(pcaps)
    random_num = np.random.randint(4, 10)
    i = 1  # 初始包序号
    a = pcaps[i].time
    i += 1
    b = []
    while i < end_num:
        b.append(round(pcaps[i].time - a, n))  # b存放iat
        a = pcaps[i].time
        i += 1
    return b

def Random_Iat_Sample(IatList):
    IatList_lenth = len(IatList)
    random_time_index = np.random.randint(1, IatList_lenth)
    random_time = IatList[random_time_index]
    return random_time