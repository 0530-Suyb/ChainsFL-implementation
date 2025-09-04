# ChainsFL

Implementation of ChainsFL.

## Requirments

- [Hyperledge Fabric 2.1](https://hyperledger-fabric.readthedocs.io/en/release-2.1/test_network.html#before-you-begin)
- Python3
- Pytorch
- Torchvision
- [IPFS](https://docs.ipfs.io/install/command-line/#official-distributions)

**Attention**: The configs of Fabric in `./commonComponent/interRun.sh` should be modified to access the Fabric deployed above. Besides, this file should be authorized with the right of *writer/read/run*.

## Start Fabric test-network

单分区双组织双peer，另外部署合约（需要有set和get两个函数），此外启动的cli容器要提前配置好访问peer0.org1的环境变量。

另外注意，有的fabric test-network里把密钥相关文件夹命名为crypto，有的则为organizations

I have used fabric 2.2.14 to test it

## IPFS

start IPFS `ipfs daemon`

## Deployment of DAG

The DAG could be deployed on a personal computer or the cloud server.

Copy all the files of this repository to the PC or cloud server, and then run following commands in the root path of this repository.

```
cd dagMainChain
python serverRun.py --epochs 1 --frac 0.1 --gpu -1 --model cnn --num_channels 1
# keep arguments the same with the command of FL task
# 此处提供的参数用于启动DAG主链后往链上提交请求训练的模型，也就是创世区块里的初始模型
```

## Run one shard

The shard also could be deployed on a personal computer or the cloud server.

Copy all the files of this repository to the deployment location, and modify `line 466` of `dagMainChain/clientRun.py` for the real address of the DAG server deployed above. Then run following commands in the root path of this repository.

```
# run the DAG client
cd dagMainChain
python clientRun.py --epochs 1 --frac 0.1 --gpu -1 --model cnn --num_channels 1

# run the FL task
cd federatedLearning
python main_fed_local.py --epochs 1 --frac 0.1 --gpu -1 --model cnn --num_channels 1

# 注意，按顺序执行，clientRun.py运行约5s，发现commonComponent/dict_users.pkl生成后再启动main_fed_local.py，这里模拟SLN选定参与联邦学习的设备后，SFN确定自己是否需要参与学习
```

The details of these parameters could be found in file `federatedLearning/utils/options.py`.
It should be noted that the `--epochs` configured in command with `clientRun.py` represents the number of rounds run in each shard.
And the `--epochs` configured in command with `main_fed_local.py` represents the number of epochs run on each local device.

运行main_fed_local.py后，如果没有自己终止程序，会一直训练下去永不停歇，除非程序崩溃。所以如果能够经历多轮迭代后，便说明程序可行，对于模型精度的话则不是ChainFL框架本身的问题了，需要调整数据集、超参数等。

参考example/README.md，查看实际运行过程中的程序输出内容。

## Run multiple shards

Similar to the above, copy all the files of this repository and then modify the files and execute the commands presented above.

Besides, the para of `nodeNum` in `line 58` of `dagMainChain/clientRun.py` indicates the shard index which should be modified.

## Acknowledgments

Acknowledgments give to [shaoxiongji](https://github.com/shaoxiongji/federated-learning) and [AshwinRJ](https://github.com/AshwinRJ/Federated-Learning-PyTorch) for the basic codes of the FL module.
