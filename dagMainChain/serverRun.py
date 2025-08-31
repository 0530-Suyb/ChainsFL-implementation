# -*- coding: utf-8 -*-
# ******************************************************
# Filename     : serverRun.py
# Author       : Shuo Yuan 
# Email        : ishawnyuan@gmail.com
# Blog         : https://iyuanshuo.com
# Last modified: 2020-06-18 20:05
# Description  : 
# ******************************************************

import sys
from dagComps import transaction
from dagComps.dag import DAG
from dagSocket import dagServer
import socket
import os
import time
import shutil
import numpy as np
import time
import glob
import torch

# 导入公共组件
sys.path.append('../commonComponent')
import usefulTools

sys.path.append('../federatedLearning')
import buildModels

# The number of tips selected by the new transaction
alpha = 3
## The number of tips needs to be kept greater than 3
beta = 3

def main(arg=True):
    if os.path.exists('./dagSS') == False:
        os.mkdir('./dagSS')
    if os.path.exists('./dagSS/dagPool'):
        shutil.rmtree('./dagSS/dagPool')
    os.mkdir('./dagSS/dagPool')
    # 创建一个 DAG（有向无环图）实例，用于管理区块链交易数据
    # active_lst_addr 参数指定了活动交易列表的存储路径
    # timespan 参数设置为 60 秒，可能与交易确认或清理机制相关
    host_DAG = DAG(active_lst_addr='./dagSS/active_list.json',timespan=60)

    # Generate the genesis block for DAG
    # genesisGen = os.popen(r"bash ./invokeRun.sh genesis")
    # genesisInfo = genesisGen.read()

    # 设置创世区块的模型参数哈希值（来自 IPFS）
    # 系统提供了两种选择：MLP 模型和 CNN 模型的哈希值，默认使用 MLP 模型
    # For MLP
    genesisInfo = 'QmaBYCmzPQ2emuXpVykLDHra7t8tPiU8reFMkbHpN1rRoo'
    # For CNN
    # genesisInfo = 'QmTZqGKUEvD5F8vQyEEJLJB7rzX17tpnN2Uu4YWBRZEYQx'

    # suyb：既然IPFS上没有模型参数文件，那就自己生成并上传IPFS
    # For testing DEMO
    net_glob, args, dataset_train, dataset_test, dict_users = buildModels.modelBuild()
    net_glob.train()
    w_glob = net_glob.state_dict()
    baseParasFile = 'initialModel.pkl'
    torch.save(w_glob, baseParasFile)
    basefileHash, baseSttCode = usefulTools.ipfsAddFile(baseParasFile)
    if baseSttCode == 0:
        print('\nThe base mode parasfile ' + baseParasFile + ' has been uploaded!')
        print('And the fileHash is ' + basefileHash + '\n')
    else:
        print('Error: ' + basefileHash)
        print('\nFailed to uploaded the aggregated parasfile ' + baseParasFile + ' !\n')
    # 赋给 genesisInfo，以符合设计模式的“开闭原则”
    genesisInfo = basefileHash

    print("The genesisBlock hash value is ", genesisInfo)
    # genesisGen.close()

    # 创建一个新的交易对象作为创世区块
    # 交易时间为当前时间，源节点 ID 设为 0，模型精度设为 0.0，模型参数设为之前定义的 genesisInfo，批准的交易列表为空
    ini_trans = transaction.Transaction(time.time(), 0, 0.0, genesisInfo, [])
    # 将创世区块保存到 ./dagSS/dagPool/ 目录
    transaction.save_genesis(ini_trans, './dagSS/dagPool/')
    # 显式设置交易名称为 'GenesisBlock'
    ini_trans.name = 'GenesisBlock'
    ini_trans_file_addr = './dagSS/dagPool/'+ ini_trans.name +'.json'

    # 调用 DAG_publish 方法将创世区块发布到 DAG 网络
    # 更新活动交易池和tips交易池
    # 新交易发布时，会同时添加到活跃交易池和tips交易池
    # 当交易被其他新交易批准时，会从tips交易池中移除，但仍保留在活跃交易池中
    
    # 将交易池数据保存到 JSON 文件
    host_DAG.DAG_publish(ini_trans, beta)
    # 调用 DAG_genesisDel 方法从tips交易池中移除创世区块
    # 这是因为创世区块不应作为新交易的批准目标
    # 确保系统从正确的状态开始处理新交易
    host_DAG.DAG_genesisDel()

    while arg:
        # 进入无限循环，持续运行网络服务
        # 调用 socket_service 函数启动套接字服务器
        # 传递 DAG 实例用于交易处理
        # 传递 beta 参数（在代码开头定义为 3，表示需要保持的tips数量）
        dagServer.socket_service("127.0.0.1", host_DAG, beta)

if __name__ == '__main__':

    main(True)
    # suyb：总结一下
    # 该脚本中，令DAG链的创世区块的交易内容为需要训练的模型参数文件在IPFS上的CID码，（相当于论文中的the task request block）
    # 后续客户端会从DAG链上创世区块的信息得到IPFS上模型参数文件的CID，然后开始下载模型参数文件，进行训练。
    # DAG链在./dagSS/dagPool/目录下保存链的每笔交易，每笔交易记录了该笔交易的交易名称、时间戳、源节点ID、模型精度、模型参数文件的CID码以及批准的交易列表等信息。