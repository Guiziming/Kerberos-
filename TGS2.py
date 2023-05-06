#TGS启动后创建两个线程，1.接收 2.发送 接收 得到连接请求后则创建一个线程，用于处理接收操作，接收后再进行处理 发送，直接给AS发送证书
import threading
import socket
from RSA import getKey
import pymysql
import tkinter.messagebox as messagebox  # 弹窗
import RSA as rsa
import des_for_rsa as des
HOST = '192.168.43.238'
# HOST= '127.0.0.1'
PORT_AS = 65432

PORT_TGS = 65433

serial_num = 1



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

#将拆后的data部分存入TGS数据库中
def save_sql(id,e,n):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='tgs')
    print("数据库连接成功")
    # 创建游标对象
    cursor = conn.cursor()

    sql = "UPDATE mtgs SET tgs_n='%s' WHERE tgs_id='%s';" %(n,id)
    # 执行SQL语句
    # sql = "INSERT INTO mtgs(tgs_id, tgs_e, tgs_n) VALUES (%s, %s, %s)" % (id,e,n)
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交到数据库执行
    except:
        conn.rollback()  # 发生错误时回滚
        messagebox.showinfo('警告！', '数据库连接失败！')


    # 关闭游标和连接
    cursor.close()
    conn.close()

def save_sql_key(id,key):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='tgs')
    print("数据库连接成功")
    # 创建游标对象
    cursor = conn.cursor()

    sql = "UPDATE mtgs SET tgs_key='%s' WHERE tgs_id='%s';" %(key,id)
    # 执行SQL语句
    # sql = "INSERT INTO mtgs(tgs_id, tgs_e, tgs_n) VALUES (%s, %s, %s)" % (id,e,n)
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交到数据库执行
    except:
        conn.rollback()  # 发生错误时回滚
        messagebox.showinfo('警告！', 'tgs数据库连接失败！')


    # 关闭游标和连接
    cursor.close()
    conn.close()


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

#拆ACK
def unpacket_ack(cont_data):
    my_port,poserver_portrt,num,type_message,fin,pipei,rongyu=cont_data.decode().split("|")
    return pipei

def process_v_message_2000(cont_data,e,n,conn):
    pipei=unpacket_ack(cont_data)
    print("pipei: ",pipei)
    if pipei=='1001':
        process_v_message_2002(e,n,conn)
    else:
        print("可能错了")

#传递证书的报文
def process_v_message_2001(cont_data,conn):
    # print("已接收到消息类型为2001的数据段,是传递证书的报文")
    print("拆除掉报头部分的内容: ",cont_data)
    #得到id、e、n
    id,e,n=unpacket_lisence(cont_data)
    print("id:",id,"e:",e,"n",n)
    #将id、e、n存入数据库中
    save_sql(id,e,n)
    #需要发送V自己的证书
    n_tgs,e_tgs,d_tgs=rsa.getKey()
    data=packet_lisence(b'1002',str(e_tgs).encode(),str(n_tgs).encode())
    # message=packet_head(b'65432',str(serial_num).encode(),b'2001',b'0',b'00000000',b'sxwnbb')
    message=packet_head(b'65433',b'2',b'2001',b'0',b'0000',b'00000000',data)
    conn.sendall(message)
    print("已成功发送TGS证书给V!")
    ack_message=conn.recv(1024)
    print("成功接收V传递来的ack")
    print("ACK:",ack_message)
    process_v_message_2000(ack_message,e,n,conn)

    flag='recv_2001'
    return flag

def process_v_message_2002(e,n,conn):
    print("TGS开始给V发送key")
    # 传输2002号报文给V（发key）
    tmp_key=des.get_key()
    print("创建的DES key为: ",tmp_key)
    save_sql_key('1003',tmp_key)
    key=tmp_key.encode()
    print("所使用的TGS公钥为: ","e",e,"n",n)
    e=int(e)
    n=int(n)
    print("看看变了没",e,n)
    key=rsa.rsa_encrypt(key,e,n)
    print("加密后key的类型和值:",type(key),key)
    key=rsa.change_to_bytes(key)
    #包装含有key的message
    key_message=packet_head(b'65433',b'3',b'2002',b'1',b'0000',b'00000000',key)
    print("TGS的key:",key) 
    #发送key
    conn.sendall(key_message)

# 使用字典存储每个值对应的处理函数
process_dict = {
    "2001": process_v_message_2001,
    "2002": process_v_message_2002,
}

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
                print('已连接到：', addr)
                message = conn.recv(1024)
                # 打印接收到的消息
                print(message)
                type_message,pipei,cont_data=unpacket(message)
                # print(type(type_message))
                # print("消息类型为:",type_message)
                # print("数据内容为:",cont_data)
                # print('收到来自客户端的消息：', data.decode())
                # print(data)
                # print('data: ',type(data),'data.decode',type(data.decode()))
                # 发送响应消息
                # 调用对应值的处理函数
                # solve(type_message,cont_data)
                if type_message in process_dict:
                    flag=process_dict[type_message](cont_data,conn)
                    print("test",flag)
                    #result = sm.execute(flag)
                    #print(sm.state)  # 输出get_license

                else:
                    # 处理其他情况
                    print("可能有错误")

        # 循环等待客户端连接
        while True:
            # 接收客户端连接请求
            conn, addr = sss.accept()
            # 创建一个新的线程来处理客户端请求
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()

#处理接收到的AS的证书
def process_AS_message_2001(cont_data,s):
    global serial_num
    # print("已接收到消息类型为2001的数据段,是传递证书的报文")
    print("拆除掉报头部分的内容: ",cont_data)
    #得到id、e、n
    # id,e,n=unpacket_lisence(cont_data)
    #将id、e、n存入数据库中
    # save_sql(cont_data)
    id,e,n=unpacket_lisence(cont_data)
    print("id:",id,"e:",e,"n",n)
    #将id、e、n存入数据库中
    save_sql(id,e,n)
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
    print("所使用的TGS私钥d,n为: ",d_tgs,n_tgs)
    key=rsa.rsa_decrypt(secret_key,d_tgs,n_tgs)
    print("我得到的DES key为: ",key)
    
    save_sql_key(id,key.decode())
    flag='recv_2001'
    return flag

def process_AS_message_2002():
    pass

# 使用字典存储每个值对应的处理函数
process_dict = {
    "2001": process_v_message_2001,
    "2002": process_v_message_2002,
}
# 使用字典存储每个值对应的处理函数
process_dict1 = {
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
        global serial_num,n_tgs,e_tgs,d_tgs
        # serial_num_byte=serial_num.to_bytes(4, byteorder='big')   
        n_tgs,e_tgs,d_tgs=getKey()
        print("e_tgs:",e_tgs,"n_tgs",n_tgs,"d_tgs",d_tgs)
        data=packet_lisence(b'1002',str(e_tgs).encode(),str(n_tgs).encode())
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
                process_dict1[type_message_rcv](cont_data_rcv,s)
        else:
            # 处理其他情况
            print("可能有错误")
        

# 创建监听线程
listen_thread = threading.Thread(target=receive_thread)
msend_thread = threading.Thread(target=send_thread)
listen_thread.start()
msend_thread.start()

