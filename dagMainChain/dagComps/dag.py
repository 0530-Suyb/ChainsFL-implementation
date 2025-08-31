import os
import time
import json
# import transaction
import random

class DAG(object):
    def __init__(self,active_lst_addr='./dagSS/active_list.json',timespan =-1):
        """
        初始化DAG类。

        :param active_lst_addr: 存储活跃交易池的JSON文件地址，默认为'./dagSS/active_list.json'
        :param timespan: 时间跨度，默认为-1
        """
        self.active_lst_addr = active_lst_addr  # 存储活跃交易池的JSON文件地址
        self.timespan = timespan  # 时间跨度
        self.active_pool = {}  # 活跃交易池，键为交易名称，值为交易时间戳
        self.tips_pool = {}  # 交易tips池，键为交易名称，值为交易时间戳

    def DAG_add(self,trans):
        """
        向DAG中添加交易到活跃交易池，并根据条件从tips池中删除已批准的交易。

        :param trans: 要添加的交易对象，需包含name、timestamp和apv_trans属性
        """
        self.active_pool[trans.name] = trans.timestamp  # 将交易添加到活跃交易池
        approve_lst = trans.apv_trans  # 获取该交易批准的交易列表
        candidateDel = []  # 待删除的候选交易列表（当前未使用）
        if len(self.tips_pool) > 3:  # 当tips池中的交易数量大于3时
            for ele in approve_lst:  # 遍历该交易批准的交易列表
                if ele in self.tips_pool:  # 如果被批准的交易在tips池中
                    del self.tips_pool[ele]  # 从tips池中删除该交易
                    
## The number of tips needs to be kept greater than 3
## The DAG_publish function is responsible for saving the newly active_pool as json file and 
    def DAG_publish(self,trans,tipsMore):
        """
        发布交易，更新活跃交易池和tips池，并将结果保存到JSON文件。
        确保tips池中的交易数量大于指定的tipsMore数量。

        :param trans: 要发布的交易对象，需包含name、timestamp和apv_trans属性
        :param tipsMore: tips池需要保持的最小交易数量
        """
        self.active_pool[trans.name] = trans.timestamp  # 将交易添加到活跃交易池
        self.tips_pool[trans.name] = trans.timestamp  # 将交易添加到tips池
        approve_lst = trans.apv_trans  # 获取该交易批准的交易列表
        
        # 如果tips池中的交易数量足够多，可以删除所有被批准的交易
        if len(self.tips_pool) >= (len(approve_lst)+tipsMore):
            for ele in approve_lst:  # 遍历该交易批准的交易列表
                if ele in self.tips_pool:  # 如果被批准的交易在tips池中
                    del self.tips_pool[ele]  # 从tips池中删除该交易
        # 如果tips池中的交易数量大于tipsMore但不足以删除所有被批准的交易
        elif (len(self.tips_pool) > tipsMore) and (len(self.tips_pool) < (len(approve_lst)+tipsMore)):
            tipsDelNum = len(self.tips_pool) - tipsMore  # 计算需要删除的交易数量
            while tipsDelNum != 0:  # 循环删除直到达到需要删除的数量
                tmpDelTip = approve_lst[random.randint(0,len(approve_lst)-1)]  # 随机选择一个待批准的交易
                if tmpDelTip in self.tips_pool:  # 如果该交易在tips池中
                    del self.tips_pool[tmpDelTip]  # 从tips池中删除该交易
                    tipsDelNum -= 1  # 需要删除的数量减1
        
        # 将活跃交易池保存到JSON文件
        with open(self.active_lst_addr,'w') as f:
            json.dump(self.active_pool,f)
            f.close()
        
        # 将tips池保存到JSON文件
        with open('./dagSS/tip_list.json','w') as f:
            json.dump(self.tips_pool,f)
            f.close()
    
    def DAG_genesisDel(self):
        """
        如果tips池中存在创世区块，则将其从tips池中删除，并更新tips池的JSON文件。
        """
        if 'GenesisBlock' in self.tips_pool.keys():  # 检查tips池中是否存在创世区块
            del self.tips_pool['GenesisBlock']  # 从tips池中删除创世区块
        
        # 将更新后的tips池保存到JSON文件
        with open('./dagSS/tip_list.json','w') as f:
            json.dump(self.tips_pool,f)
            f.close()

## !!! Note: This part is important for the realization of product logic.
    def DAG_choose(self,max_num):
        """
        从tips池中选择最多max_num个交易。

        :param max_num: 最多选择的交易数量
        :return: 选中的交易名称列表
        """
        count = 0  # 已选择的交易数量
        trans_lst = []  # 选中的交易列表
        for trans in self.tips_pool:  # 遍历tips池中的交易
            if count >= max_num:  # 如果已选择的交易数量达到上限
                break  # 停止遍历
            count += 1  # 已选择的交易数量加1
            trans_lst.append(trans)  # 将交易添加到选中列表中
        return trans_lst