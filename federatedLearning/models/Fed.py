#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import copy
import torch
from torch import nn

def FedAvg(w):
    """
    实现联邦平均算法，聚合多个本地模型的权重
    
    :param w: 本地模型权重列表
    :return: 聚合后的全局模型权重
    """
    # 深拷贝第一个模型的权重作为初始聚合结果
    w_avg = copy.deepcopy(w[0])
    
    # 对每个模型参数进行加权平均
    for k in w_avg.keys():
        for i in range(1, len(w)):
            w_avg[k] += w[i][k]
        w_avg[k] = torch.div(w_avg[k], len(w))  # 除以模型数量，得到平均值
    
    return w_avg  # 返回聚合后的模型权重
