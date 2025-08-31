import socket
import sys
import struct
import os
import time
import json

# 定义一个客户端套接字函数，用于与指定地址的服务器进行交互
def socket_client(aim_addr):
    try:
        # 创建一个基于 IPv4 和 TCP 协议的套接字对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接到指定地址和端口号为 6666 的服务器
        s.connect((aim_addr, 6666))
    except socket.error as msg:
        # 若连接出错，打印错误信息并退出程序
        print(msg)
        sys.exit(1)
    # 接收服务器发送的消息并打印
    print(s.recv(1024))
    while 1:
        # 获取用户输入并编码为字节流
        data = input('please input work: ').encode()
        # 将用户输入的数据发送给服务器
        s.send(data)
        # 接收服务器的响应并打印
        print('aa', s.recv(1024))
        # 若用户输入为 'exit'，则退出循环
        if data == 'exit'.encode():
            break
    # 关闭套接字连接
    s.close()

# 定义一个函数，用于计算客户端与服务器之间的时间延迟
def back_delay(aim_addr):
    try:
        # 创建一个基于 IPv4 和 TCP 协议的套接字对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接到指定地址和端口号为 6666 的服务器
        s.connect((aim_addr, 6666))
    except socket.error as msg:
        # 若连接出错，打印错误信息并退出程序
        print(msg)
        sys.exit(1)
    # 记录客户端当前时间
    client_time = time.time()
    # 接收服务器发送的消息并解码打印
    print(s.recv(1024).decode())
    # 发送 'delay' 指令给服务器
    data = 'delay'.encode()
    s.send(data)
    # 接收服务器时间并转换为浮点数
    sever_time = float(s.recv(1024).decode())
    # 计算服务器时间与客户端时间的差值
    delta = sever_time - client_time
    return delta

# 定义一个函数，用于向服务器请求交易数据并接收文件
def client_trans_require(aim_addr, trans_name, DAG_file):
    try:
        # 创建一个基于 IPv4 和 TCP 协议的套接字对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接到指定地址和端口号为 6666 的服务器
        s.connect((aim_addr, 6666))
    except socket.error as msg:
        # 若连接出错，打印错误信息并退出程序
        print(msg)
        sys.exit(1)
    # 接收服务器发送的消息并解码打印
    print(s.recv(1024).decode())
    # 发送 'require' 指令给服务器
    data = 'require'.encode()
    s.send(data)
    # 接收服务器的响应
    response = s.recv(1024)
    # 发送交易名称给服务器
    data = trans_name.encode()
    s.send(data)
    # 调用 rev_file 函数接收文件
    rev_file(s, DAG_file)
    # 关闭套接字连接
    s.close()

# 定义一个函数，用于向服务器请求tips交易数据并接收文件
def client_tips_require(aim_addr, tips_list, tips_file):
    try:
        # 创建一个基于 IPv4 和 TCP 协议的套接字对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接到指定地址和端口号为 6666 的服务器
        s.connect((aim_addr, 6666))
    except socket.error as msg:
        # 若连接出错，打印错误信息并退出程序
        print(msg)
        sys.exit(1)
    # 接收服务器发送的消息并解码打印
    print(s.recv(1024).decode())
    # 发送 'requireTips' 指令给服务器
    data = 'requireTips'.encode()
    s.send(data)
    # 接收服务器的响应
    response = s.recv(1024)
    # 发送提示列表给服务器
    data = tips_list.encode()
    s.send(data)
    # 调用 rev_file 函数接收文件
    rev_file(s, tips_file)
    # 关闭套接字连接
    s.close()

# 定义一个函数，用于向服务器上传交易信息
def trans_upload(aim_addr, trans_info):
    try:
        # 创建一个基于 IPv4 和 TCP 协议的套接字对象
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接到指定地址和端口号为 6666 的服务器
        s.connect((aim_addr, 6666))
    except socket.error as msg:
        # 若连接出错，打印错误信息并退出程序
        print(msg)
        sys.exit(1)
    # 接收服务器发送的消息并解码打印
    print(s.recv(1024).decode())
    # 发送 'transUpload' 指令给服务器
    data = 'transUpload'.encode()
    s.send(data)
    # 接收服务器的响应
    response = s.recv(1024)
    # 将交易信息转换为 JSON 格式并编码为字节流发送给服务器
    data = json.dumps(trans_info.json_output()).encode("utf-8")
    s.send(data)
    # 接收服务器的响应
    response = s.recv(1024)
    # 关闭套接字连接
    s.close()

# 定义一个函数，用于从连接中接收文件并保存到指定地址
def rev_file(conn, file_addr):
    while 1:
        # 计算文件信息结构体的大小
        fileinfo_size = struct.calcsize('128si')
        # 接收文件信息
        buf = conn.recv(fileinfo_size)
        if buf:
            # 解析文件信息，获取文件名和文件大小
            filename, filesize = struct.unpack('128si', buf)
            # 去除文件名中的空字符
            fn = filename.strip(b'\00')
            # 解码文件名
            fn = fn.decode()
            # 打印文件名和文件大小
            print('File name is {0}, filesize is {1}'.format(str(fn), filesize))
            # 已接收的文件大小初始化为 0
            recvd_size = 0
            # 以二进制写入模式打开文件
            fp = open(file_addr, 'wb')
            # 打印开始接收文件的提示信息
            print('Start receiving...')
            # 发送 'OK' 确认消息给发送方
            conn.send('OK'.encode())
            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    # 若剩余文件大小大于 1024 字节，接收 1024 字节数据
                    data = conn.recv(1024)
                    recvd_size += len(data)
                else:
                    # 若剩余文件大小小于等于 1024 字节，接收剩余数据
                    data = conn.recv(filesize - recvd_size)
                    recvd_size = filesize
                # 将接收到的数据写入文件
                fp.write(data)
            # 关闭文件
            fp.close()
            # 打印接收文件结束的提示信息
            print('End receive...')
        break

if __name__ == '__main__':
    # 若作为主程序运行，调用 socket_client 函数并传入命令行参数中的地址
    socket_client(sys.argv[1])