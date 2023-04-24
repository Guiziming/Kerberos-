import socket

# 定义服务器IP地址和端口号
HOST = '192.168.43.238'
PORT = 65432

PORT2 = 65433

PORT3 = 65434



# 定义一个socket对象,与AS通信
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
    # 连接服务器
    s1.connect((HOST, PORT))
    print('已连接到AS...')

    # 发送消息
    s1.sendall(b'hello')
    # 接收响应消息
    data1 = s1.recv(1024)

    # 打印响应消息
    print('收到来自AS的消息：', data1.decode())


# 定义一个socket对象,与TGS通信
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
    # 连接服务器
    s2.connect((HOST, PORT2))
    print('已连接到TGS...')

    # 发送消息
    s2.sendall(b'hello')
    # 接收响应消息
    data2 = s2.recv(1024)

    # 打印响应消息
    print('收到来自TGS的消息：', data2.decode())

# 定义一个socket对象,与V通信
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s3:
    # 连接服务器
    s3.connect((HOST, PORT3))
    print('已连接到V...')

    # 发送消息
    s3.sendall('获取V认证')
    # 接收响应消息
    data3 = s3.recv(1024)

    # 打印响应消息
    print('收到来自V的消息：', data3.decode())


