import socket

# 定义服务器IP地址和端口号
HOST_TGS = '192.168.43.238'
PORT_TGS = 65433

# 定义一个socket对象
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 连接服务器
    s.connect((HOST_TGS, PORT_TGS))
    print('已连接到服务器...')

    # 发送消息
    s.sendall(b'Hello,i am V!')
    # 接收响应消息
    data = s.recv(1024)

    # 打印响应消息
    print('收到来自服务器的消息：', data.decode())