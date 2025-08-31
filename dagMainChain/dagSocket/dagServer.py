import socket
import threading
import time
import sys
import struct
import os
import shutil
from dagComps import transaction
import json

def socket_service(local_addr, dag_pool, beta):
    """
    启动DAG服务器的套接字服务，处理客户端连接和请求

    :param local_addr: 服务器本地地址
    :param dag_pool: DAG实例，用于处理交易
    :param beta: 保持的最小tips交易数量
    """
    try:
        # 创建TCP套接字并设置端口复用
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 注意此次一定是以元组形式传入
        s.bind(("", 6666))  # 绑定到所有网络接口的6666端口
        s.listen(5)       # 开始监听，最多允许5个连接排队
        print('DAG_socket starts...')
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    
    # 无限循环，接受客户端连接
    while 1:
        conn, addr = s.accept()  # 接受客户端连接
        # 为每个客户端创建一个新的线程处理请求
        t = threading.Thread(target=deal_data, args=(conn, addr, dag_pool, beta))
        t.start()

def send_file(conn, file_addr):
    """
    向客户端发送文件

    :param conn: 与客户端的连接套接字
    :param file_addr: 要发送的文件路径
    """
    if os.path.isfile(file_addr):
        # 打包文件名和文件大小
        fileinfo_size = struct.calcsize('128si')
        fhead = struct.pack('128si', os.path.basename(file_addr).encode('utf-8'), os.stat(file_addr).st_size)
        conn.send(fhead)
        fp = open(file_addr, 'rb')
        response = conn.recv(1024)  # 等待客户端确认
        
        # 分块发送文件内容
        while 1:
            data = fp.read(1024)
            if not data:
                print('{0} file send over...'.format(os.path.basename(file_addr)))
                break
            conn.send(data)

def deal_data(conn, addr, dag_pool, beta):
    """
    处理客户端请求的线程函数

    :param conn: 与客户端的连接套接字
    :param addr: 客户端地址
    :param dag_pool: DAG实例
    :param beta: 保持的最小tips交易数量
    """
    print('Accept new connection from {0}'.format(addr))
    conn.send("You've connected, wait for command...".encode())
    
    while 1:
        data = conn.recv(1024)  # 接收客户端数据
        msg = data.decode()
        
        # 处理不同类型的客户端请求
        if msg == 'exit' or msg == 'require' or msg == 'requireTips' or msg == 'transUpload' or msg == 'delay':
            print('{0} client send data is {1}'.format(addr, msg))
        
        time.sleep(1)
        
        # 客户端退出连接
        if msg == 'exit' or not data:
            print('{0} connection close'.format(addr))
            conn.send('Connection closed!'.encode())
            break
        
        # 根据消息类型处理请求
        if msg == 'require':
            # 客户端请求特定交易数据
            conn.send('ok'.encode())
            data_t = conn.recv(1024)
            msg_t = data_t.decode()
            require_trans_file = './dagSS/dagPool/'+msg_t+'.json'
            send_file(conn, require_trans_file)
        elif msg == 'requireTips':
            # 客户端请求tips交易列表
            conn.send('ok'.encode())
            data_t = conn.recv(1024)
            msg_t = data_t.decode()
            require_tips_file = './dagSS/'+msg_t+'.json'
            send_file(conn, require_tips_file)
        elif msg == 'transUpload':
            # 客户端上传新交易
            conn.send('ok'.encode())
            data_t = conn.recv(1024)
            conn.send('ok'.encode())
            msg_t = json.loads(data_t.decode("utf-8"))
            new_trans = transaction.Transaction(**msg_t)  # 创建交易对象
            transaction.save_transaction(new_trans, './dagSS/dagPool/')  # 保存交易
            dag_pool.DAG_publish(new_trans, beta)  # 发布交易到DAG网络
            transName = 'node{}_'.format(new_trans.src_node) + str(new_trans.timestamp)
            print('*******************************************')
            print('The new trans *'+transName+'* had been published!')
            print('*******************************************')
        elif msg == 'delay':
            # 客户端请求当前时间戳
            conn.send(str(time.time()).encode())
    
    conn.close()  # 关闭连接