#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python version: 3.6

import argparse

def args_parser():
    """
    解析命令行参数，配置联邦学习和模型参数
    
    :return: 解析后的参数字典
    """
    parser = argparse.ArgumentParser()
    
    # 联邦学习相关参数
    parser.add_argument('--epochs', type=int, default=10, help="训练轮数")
    parser.add_argument('--num_users', type=int, default=100, help="用户数量: K")
    parser.add_argument('--frac', type=float, default=0.1, help="每轮参与训练的客户端比例: C")
    parser.add_argument('--local_ep', type=int, default=5, help="本地训练轮数: E")
    parser.add_argument('--local_bs', type=int, default=10, help="本地批次大小: B")
    parser.add_argument('--bs', type=int, default=128, help="测试批次大小")
    parser.add_argument('--lr', type=float, default=0.01, help="学习率")
    parser.add_argument('--momentum', type=float, default=0.5, help="SGD动量参数")
    parser.add_argument('--split', type=str, default='user', help="训练-测试集划分方式")

    # 模型相关参数
    parser.add_argument('--model', type=str, default='mlp', help='模型名称')
    parser.add_argument('--kernel_num', type=int, default=9, help='每种卷积核的数量')
    parser.add_argument('--kernel_sizes', type=str, default='3,4,5', 
                        help='卷积核大小列表')
    parser.add_argument('--norm', type=str, default='batch_norm', help="归一化方式")
    parser.add_argument('--num_filters', type=int, default=32, help="卷积滤波器数量")
    parser.add_argument('--max_pool', type=str, default='True', 
                        help="是否使用最大池化")

    # 其他参数
    parser.add_argument('--dataset', type=str, default='mnist', help="数据集名称")
    parser.add_argument('--iid', action='store_true', help='数据是否独立同分布')
    parser.add_argument('--num_classes', type=int, default=10, help="类别数量")
    parser.add_argument('--num_channels', type=int, default=3, help="图像通道数")
    parser.add_argument('--gpu', type=int, default=-1, help="GPU ID, -1表示使用CPU")
    parser.add_argument('--stopping_rounds', type=int, default=10, help='早停轮数')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    parser.add_argument('--seed', type=int, default=1, help='随机种子')
    
    args = parser.parse_args()
    return args
