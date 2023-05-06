#TGS启动后创建两个线程，1.接收 2.发送 接收 得到连接请求后则创建一个线程，用于处理接收操作，接收后再进行处理 发送，直接给AS发送证书
import threading
import socket
from RSA import getKey
import pymysql
import tkinter.messagebox as messagebox  # 弹窗
import RSA as rsa
import datetime
import des_for_rsa as des
HOST = '192.168.43.238'
# HOST= '127.0.0.1'

PORT_TGS = 65433
PORT_V = 65434
PORT_AS = 65432

serial_num = 1

def change_to_bytes(my_uint):
    if my_uint == 0:
        return bytes(1)
    result = my_uint.to_bytes((my_uint.bit_length() + 7) // 8, 'big')  # 8位划分，尽量少补零
    return result

# 获取时间戳
def get_time():
    start_time = datetime.datetime(2023, 5, 1, 0, 0, 0)
    now = datetime.datetime.now()
    ts = (now - start_time).seconds
    return ts

# ack打包函数，ack只需要传递包头
def packet_ack(port, num, type_message, fin,pipei,rongyu):
    my_port = port
    server_port = port
    serial_num = num
    type_mes = type_message
    FIN = fin
    pipei_num=pipei
    baoliu = rongyu
    ack = my_port + b'|' + server_port + b'|' + serial_num + b'|' + type_mes + b'|' + FIN + b'|'+pipei_num + b'|'+ baoliu
    return ack

#拆data部分
def unpacket_lisence(cont_data):
    id,e,n = cont_data.split(",")
    return id,e,n
    # return id,e,n

def unpacket_key_head(packet):
    port, my_port, num, type_message, fin, pipei, rongyu, data=packet.split(b'|')
    print("这个的data是: ",data)
    print("类型为:",type(data))
    return data

def unpacket_TS_head(packet):
    port, my_port, num, type_message, fin, pipei, rongyu, data=packet.split(b'|')
    print("这个的data是: ",data)
    print("类型为:",type(data))
    return type_message,data

# 拆包报头
def unpacket(packet):
    port, my_port, num, type_message, fin, pipei, rongyu, data = packet.decode().split("|")
    print("来源端口", port, "类型", type(port))
    print("序列号", num)
    print("信息类型", type_message)
    print("结束标识", fin)
    print("匹配为",pipei)
    print("数据", data)
    return type_message , pipei , data #返回值添加一个fin

# 打包报头部分
def packet_head(port, num, type_message, fin,pipei, rongyu, data):
    my_port = port
    server_port = port
    serial_num = num
    type_mes = type_message
    FIN = fin
    pipei_num=pipei
    baoliu = rongyu
    baotou = my_port + b'|' + server_port + b'|' + serial_num + b'|' + type_mes + b'|' + FIN +b'|'+pipei_num+ b'|' + baoliu
    a_packet = baotou + b'|' + data
    print(a_packet)
    return a_packet

#打包data部分
def packet_lisence(id,e,n):
    return id + b',' + e + b',' +n

#C->AS,Kerberos过程打包data
def packet_data_2003(IDc,IDtgs):
    ts=get_time()
    TS=str(ts)
    ts1=TS.encode()
    return IDc+b','+IDtgs+b','+ts1

#接受2004号报文（AS的ticket【tgs】
def recv_2004(data):
    global key_as,Key_c_to_tgs
    # Keyc='数据库里rsa发的key，转化为int'
    # key_as='67333333'
    print("C使用的key:",key_as,type(key_as))
    encry_data=des.decrypt(data,key_as)
    print("解密用的key:",key_as)
    print("****encry_data******",encry_data,type(encry_data))
    Key_c_to_tgs,IDtgs,TS2,Lifetime2,ticket_tgs=encry_data.split(',')
    ts2 = int(TS2)
    now_time = get_time()
    if now_time - ts2 <= 10:
        return ticket_tgs
    else:
        return 'error'
    
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
   

#处理接收到的AS的证书
def process_AS_message_2001(cont_data,s):
    global serial_num,id_as,e_as,n_as,key_as
    # print("已接收到消息类型为2001的数据段,是传递证书的报文")
    print("拆除掉报头部分的内容: ",cont_data)
    #得到id、e、n
    # id,e,n=unpacket_lisence(cont_data)
    #将id、e、n存入数据库中
    # save_sql(cont_data)
    id_as,e_as,n_as=unpacket_lisence(cont_data)
    print("as的id:",id_as,"as的e:",e_as,"as的n",n_as)
    mack=packet_ack(b'65432',str(serial_num).encode(),b'2000',b'0',b'1001',b'00000000')
    print("mack:",mack)
    s.sendall(mack)
    print("成功发送mack给AS")
    serial_num=serial_num+1
    key_rcv=s.recv(1024)
    print("接收到的key_message为:",key_rcv)
    secret_key=unpacket_key_head(key_rcv)
    secret_key=rsa.change_to_uint(secret_key)
    print("secret_key:",secret_key)
    print("所使用的c私钥d,n为: ",d_c,n_c)
    key_as=rsa.rsa_decrypt(secret_key,d_c,n_c)
    key_as=key_as.decode()
    print("我得到的DES key为: ",key_as)

    flag='recv_2001'
    return flag

def process_AS_message_2002():
    pass

# 使用字典存储每个值对应的处理函数
process_dict = {
    "2001": process_AS_message_2001,
    "2002": process_AS_message_2002,
}

#发送的主线程 A发送->B接收->B发送->A接收
def send_thread():
    """发送数据线程函数"""
    print('发送已启动，准备发送...')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT_AS))
        # 从命令行读取用户输入
        # print(type(threading.get_ident()))
        global serial_num,n_c,e_c,d_c
        # serial_num_byte=serial_num.to_bytes(4, byteorder='big')   
        n_c,e_c,d_c=getKey()
        print("e_c:",e_c,"n_c",n_c,"d_c",d_c)
        data=packet_lisence(b'1004',str(e_c).encode(),str(n_c).encode())
        print("数据段：",data)
        message=packet_head(b'65432',str(serial_num).encode(),b'2001',b'0',b'0000',b'00000000',data)
        serial_num=serial_num+1
        # print(serial_num)
        # message = input("hi,i am tgs")
        # 发送数据到服务器
        s.sendall(message)
        #接收发送回来的内容，再关闭连接。
        rcv_message = s.recv(1024)
        print("rcv_message:",rcv_message)
        type_message_rcv,pipei,cont_data_rcv=unpacket(rcv_message)
        print("消息类型为:",type_message_rcv)
        print("数据内容为:",cont_data_rcv)
        if type_message_rcv in process_dict:
                process_dict[type_message_rcv](cont_data_rcv,s)
        else:
            # 处理其他情况
            print("可能有错误")
    

def send_kerberos_thread():
    '''Kerberos发送线程函数'''
    print('kerberos发送已启动,准备发送...')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT_AS))
            #获取2003报文
            global serial_num
            num=serial_num#更换成相应序列号
            serial_num=serial_num+1
            data_2003=packet_data_2003(b'1004',b'1002')
            message_2003=packet_head(b'65433',b'3',b'2003',b'0',b'0000',b'00000000',data_2003)
            s.sendall(message_2003)
            message_2004=s.recv(1024)
            print(message_2004)
            type_message,data_2004=unpacket_TS_head(message_2004)
            ticket_tgs=recv_2004(data_2004)
            if ticket_tgs=='error':
                # a='发送超时反馈'
                mack=packet_ack(b'65432',b'4',b'2000',b'0',b'0000',b'ts2to')
                s.sendall(mack)
            else:
                print("******我与AS通信成功啦******")
                

                #创建和tgs通信的线程

            # type_message,data_2004=unpacket(message_2004)
            # ticket_tgs=recv_2004(data_2004)
            # if ticket_tgs=='error':
            #     print("发送超时反馈")
            #     a='发送超时反馈'
            # else:
            #     pass
            #     #创建和tgs通信的线程

msend_thread = threading.Thread(target=send_thread)
msend_kerberos_thread=threading.Thread(target=send_kerberos_thread)
msend_thread.start()
msend_thread.join()
msend_kerberos_thread.start()
msend_thread.join()
