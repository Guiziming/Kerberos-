#TGS启动后创建两个线程，1.接收 2.发送 接收 得到连接请求后则创建一个线程，用于处理接收操作，接收后再进行处理 发送，直接给AS发送证书
import threading
import socket
from RSA import getKey
HOST = '192.168.43.238'
PORT_AS = 65432

PORT_TGS = 65433

serial_num = 1

#最大的拆包，将报头和数据部分分开
def unpacket(packet):
    port,my_port, num, type_message, fin, rongyu, data = packet.decode().split("|")
    print("来源端口", port,"类型",type(port))
    print("序列号", num)
    print("信息类型", type_message)
    print("结束标识", fin)
    print("数据", data)
    return type_message,data

#打包报头部分
def packet_head(port, num, type_message, fin, rongyu, data):
    my_port = port
    # print(my_port)
    server_port =port
    # print(server_port)
    serial_num = num
    # print(serial_num)
    type_mes = type_message
    # print(type_mes)
    FIN = fin
    baoliu = rongyu
    baotou = my_port + b'|' + server_port + b'|' + serial_num + b'|' + type_mes + b'|' + FIN + b'|' + baoliu
    a_packet = baotou + b'|' + data
    print(a_packet)
    return a_packet

#打包data部分
def packet_data(id,e,n):
    return id + b',' + e + b',' +n

#处理接收到的数据内容
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

    
#接收的主线程
def receive_thread():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sss:
        # 绑定服务器IP地址和端口号
        sss.bind((HOST, PORT_TGS))
        # 开始监听
        sss.listen()
        print('接收已启动，等待客户端连接...')

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

#传递证书的报文
def process_message_2001(cont_data):
    # print("已接收到消息类型为2001的数据段,是传递证书的报文")
    print("拆除掉报头部分的内容: ",cont_data)
    #得到id、e、n
    # id,e,n=unpacket_data(cont_data)
    #将id、e、n存入数据库中
    # save_sql(cont_data)
    

def process_message_2002():
    pass

# 使用字典存储每个值对应的处理函数
process_dict = {
    "2001": process_message_2001,
    "2002": process_message_2002,
}

#发送的主线程 A发送->B接收->B发送->A接收
def send_thread():
    """发送数据线程函数"""
    print('发送已启动，准备发送...')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT_AS))
        # 从命令行读取用户输入
        # print(type(threading.get_ident()))
        global serial_num
        # serial_num_byte=serial_num.to_bytes(4, byteorder='big')   
        n_tgs,e_tgs,d_tgs=getKey()
        # print("e_tgs:",e_tgs,"n_tgs",n_tgs)
        data=packet_data(b'1002',str(e_tgs).encode(),str(n_tgs).encode())
        print("数据段：",data)
        message=packet_head(b'65432',str(serial_num).encode(),b'2001',b'0',b'00000000',data)
        serial_num=serial_num+1
        # print(serial_num)
        # message = input("hi,i am tgs")
        # 发送数据到服务器
        s.sendall(message)
        #接收发送回来的内容，再关闭连接。
        rcv_message = s.recv(1024)
        print(rcv_message)
        type_message_rcv,cont_data_rcv=unpacket(rcv_message)
        print("消息类型为:",type_message_rcv)
        print("数据内容为:",cont_data_rcv)
        if type_message_rcv in process_dict:
                process_dict[type_message_rcv](cont_data_rcv)
        else:
            # 处理其他情况
            print("可能有错误")

# 创建监听线程
listen_thread = threading.Thread(target=receive_thread)
msend_thread = threading.Thread(target=send_thread)
listen_thread.start()
msend_thread.start()

