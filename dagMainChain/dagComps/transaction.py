import json
import numpy as np
import time
import hashlib

class Transaction(object):
    """
    交易类，用于表示DAG网络中的交易数据
    包含交易时间戳、源节点、模型精度、模型参数哈希和批准的交易列表
    """
    def __init__(self, timestamp, src_node, model_acc, model_para, apv_trans=[]):
        """
        初始化交易对象

        :param timestamp: 交易创建时间戳
        :param src_node: 发起交易的节点ID
        :param model_acc: 模型精度值
        :param model_para: 模型参数的IPFS哈希值
        :param apv_trans: 该交易批准的其他交易名称列表
        """
        self.timestamp = timestamp    # 交易时间戳
        self.src_node = src_node      # 源节点ID
        self.model_acc = model_acc    # 模型精度
        self.model_para = model_para  # 模型参数的IPFS哈希
        self.apv_trans = apv_trans    # 批准的交易列表
        self.hashdata = self.hash()   # 交易哈希值
        self.name = 'node{}_'.format(self.src_node) + str(self.timestamp)  # 交易名称

    def hash(self):
        """
        计算交易的哈希值，用于交易的唯一标识和验证

        :return: 交易的SHA256哈希值
        """
        tohash = {
            'timestamp': self.timestamp,
            'src_node': self.src_node
        }

        str_data = json.dumps(
                            tohash,
                            default=lambda obj: obj.__dict__,
                            sort_keys=True)

        str_data_encode = str_data.encode()
        return hashlib.sha256(str_data_encode).hexdigest()

    def json_output(self):
        """
        将交易对象转换为JSON格式输出

        :return: 交易数据的字典表示
        """
        output = {
            'timestamp': self.timestamp,
            'src_node': self.src_node,
            'model_acc': self.model_acc,
            'model_para': self.model_para,
            'apv_trans': self.apv_trans
        }
        return output

    def __str__(self):
        """
        交易对象的字符串表示

        :return: 交易的JSON字符串表示
        """
        return json.dumps(
            self.json_output(),
            default=lambda obj: obj.__dict__,
            sort_keys=True)

# 交易相关辅助函数
def read_transaction(trans_file):
    """
    从文件中读取交易数据

    :param trans_file: 交易文件路径
    :return: 解析后的交易对象
    """
    with open(trans_file, 'r') as f:
        trans_para = json.load(f)
        f.close()
    return Transaction(**trans_para)

def save_transaction(trans, file_addr):
    """
    将交易保存到文件

    :param trans: 要保存的交易对象
    :param file_addr: 保存交易的目录地址
    """
    file_name = file_addr + '/node{}_'.format(trans.src_node) + str(trans.timestamp) + '.json'
    try:
        with open(file_name, 'w') as f:
            f.write(str(trans))
    except Exception as e:
        print("Couldn't save the trans " + file_name)
        print('Reason:', e)

def save_genesis(trans, file_addr):
    """
    保存创世区块到文件

    :param trans: 创世区块交易对象
    :param file_addr: 保存目录地址
    """
    file_name = file_addr + 'GenesisBlock' + '.json'
    with open(file_name, 'w') as f:
        f.write(str(trans))
        f.close()

def name_2_time(trans_name):
    """
    从交易名称中提取时间戳和源节点信息

    :param trans_name: 交易名称
    :return: (时间戳, 源节点)元组
    """
    name = str(trans_name)
    split_lst = name.split('_', 1)
    src_node = split_lst[0]
    time = float(split_lst[1])
    return time, src_node
    