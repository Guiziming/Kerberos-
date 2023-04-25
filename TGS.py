import threading
import socket

HOST = '192.168.43.238'
PORT_AS = 65432

PORT_TGS = 65433

def solve_receive(conn, addr):
    # 接收客户端发送的消息
   with conn:
        while True:
            # 接收客户端发送的消息
            data = conn.recv(1024)
            if not data:
                break
            # 打印接收到的消息
            print('收到来自客户端的消息：', data.decode())
            print(data)
            # print('data: ',type(data),'data.decode',type(data.decode()))
            # 发送响应消息
            conn.sendall(b'Received: ' + data)

    

def receive_thread():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sss:
        # 绑定服务器IP地址和端口号
        sss.bind((HOST, PORT_TGS))
        # 开始监听
        sss.listen()
        print('服务器已启动，等待客户端连接...')

        # 定义一个客户端处理线程
        def handle_client(conn, addr):
            with conn:
                print('已连接到客户端：', addr)
                while True:
                    # 接收客户端发送的消息
                    data = conn.recv(1024)
                    if not data:
                        break
                    # 打印接收到的消息
                    print('收到来自客户端的消息：', data.decode())
                    # print(data)
                    # print('data: ',type(data),'data.decode',type(data.decode()))
                    # 发送响应消息
                    conn.sendall(b'Received: ' + data)

        # 循环等待客户端连接
        while True:
            # 接收客户端连接请求
            conn, addr = sss.accept()
            # 创建一个新的线程来处理客户端请求
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()
        

def send_thread():
    """发送数据线程函数"""
    print('服务器已启动，准备发送...')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT_AS))
        # 从命令行读取用户输入
        message = input("hi,i am tgs")
        # 发送数据到服务器
        s.sendall(message.encode())

# 创建监听线程
listen_thread = threading.Thread(target=receive_thread)
msend_thread = threading.Thread(target=send_thread)
listen_thread.start()
msend_thread.start()

