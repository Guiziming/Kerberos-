import threading
import socket

# 定义服务器IP地址和端口号
HOST_AS = '192.168.43.238'
PORT_AS = 65432

#拆包
def unpacket(packet):
    port,my_port, num, type_message, fin, rongyu, data = packet.decode().split("|")
    print("来源端口", port,"类型",type(port))
    print("序列号", num)
    print("信息类型", type_message)
    print("结束标识", fin)
    print("数据", data)
    return data

# 定义一个socket对象
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 绑定服务器IP地址和端口号
    s.bind((HOST_AS, PORT_AS))
    # 开始监听
    s.listen()
    print('服务器已启动，等待连接...')

    # 定义一个客户端处理线程
    def handle_client(conn, addr):
        with conn:
            print('已连接到：', addr)
            while True:
                # 接收客户端发送的消息
                data = conn.recv(1024)
                if not data:
                    break
                # 打印接收到的消息
                cont_data=unpacket(data)
                print("数据内容为:",cont_data)
                # print('收到来自客户端的消息：', data.decode())
                # print(data)
                # print('data: ',type(data),'data.decode',type(data.decode()))
                # 发送响应消息
                conn.sendall(b'Received: ' + data)

    # 循环等待客户端连接
    while True:
        # 接收客户端连接请求
        conn, addr = s.accept()
        # 创建一个新的线程来处理客户端请求
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()
