#TGS启动后创建两个线程，1.接收 2.发送 接收 得到连接请求后则创建一个线程，用于处理接收操作，接收后再进行处理 发送，直接给AS发送证书
import threading
import socket
from RSA import getKey
import pymysql
import tkinter.messagebox as messagebox  # 弹窗
import RSA as rsa
import des_for_rsa as des
import datetime
import sys
import tkinter as tk

HOST = '192.168.43.238'
# HOST= '127.0.0.1'

PORT_TGS = 65433
PORT_V = 65434

serial_num = 1

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

#将拆后的data部分存入v数据库中
def save_sql(id,e,n):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v')
    # print("数据库连接成功")
    # 创建游标对象
    cursor = conn.cursor()

    # 执行SQL语句
    # sql = "INSERT INTO mv(v_id, v_e, v_n) VALUES (%s, %s, %s)" % (id,e,n)
    sql = "UPDATE mv SET v_n='%s' WHERE v_id='%s';" %(n,id)
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
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v')
    # print("数据库连接成功")
    # 创建游标对象
    cursor = conn.cursor()

    sql = "UPDATE mv SET v_key='%s' WHERE v_id='%s';" %(key,id)
    # 执行SQL语句
    # sql = "INSERT INTO mtgs(tgs_id, tgs_e, tgs_n) VALUES (%s, %s, %s)" % (id,e,n)
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交到数据库执行
    except:
        conn.rollback()  # 发生错误时回滚
        messagebox.showinfo('警告！', 'v数据库连接失败！')

def save_sql_c(c_n,idc):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v')
    # print("数据库连接成功")
    # 创建游标对象
    cursor = conn.cursor()

    sql = "UPDATE mv SET v_n='%s' WHERE v_id='%s';" %(c_n,idc)
    # 执行SQL语句
    # sql = "INSERT INTO mtgs(tgs_id, tgs_e, tgs_n) VALUES (%s, %s, %s)" % (id,e,n)
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交到数据库执行
    except:
        conn.rollback()  # 发生错误时回滚
        messagebox.showinfo('警告！', 'v数据库连接失败！')

def save_sql_v(v_n,v_d):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v')
    # print("数据库连接成功")
    # 创建游标对象
    cursor = conn.cursor()

    sql = "UPDATE mv SET v_n='%s',v_d='%s' WHERE v_id='1003';" %(v_n,v_d)
    # 执行SQL语句
    # sql = "INSERT INTO mtgs(tgs_id, tgs_e, tgs_n) VALUES (%s, %s, %s)" % (id,e,n)
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交到数据库执行
    except:
        conn.rollback()  # 发生错误时回滚
        messagebox.showinfo('警告！', 'v数据库连接失败！')

#获取v数据库中与tgs通信的密钥
def get_key_sql(id):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v')
    # print("数据库连接成功")
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    # sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
    sql = "SELECT v_key FROM mv WHERE v_id ='%s';" %(id)
    result=''
    cursor.execute(sql)  # 执行sql语句
    result = cursor.fetchone()[0]
    # try:
    #     cursor.execute(sql)  # 执行sql语句
    #     result = cursor.fetchall()
    #     # conn.commit()  # 提交到数据库执行
    # except:
    #     conn.rollback()  # 发生错误时回滚
    #     messagebox.showinfo('警告！', 'KEY数据库连接失败！')


    # 关闭游标和连接
    cursor.close()
    conn.close()
    # print('数据库中的key:',result,type(result))
    return result

#拆data部分
def unpacket_lisence(cont_data):
    id,e,n = cont_data.split(",")
    return id,e,n
    # return id,e,n

def unpacket_key_head(packet):
    port, my_port, num, type_message, fin, pipei, rongyu, data=packet.split(b'|')
    # print("这个的data是: ",data)
    # print("类型为:",type(data))
    return data
# 拆包报头
def unpacket(packet):
    print("收到的完整数据包内容: ",packet)
    port, my_port, num, type_message, fin, pipei, rongyu, data = packet.decode().split("|")
    # print("来源端口", port, "类型", type(port))
    # print("序列号", num)
    # print("信息类型", type_message)
    # print("结束标识", fin)
    # print("匹配为",pipei)
    # print("数据", data)
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
    print("发送的完整数据包内容:",a_packet)
    return a_packet

#打包data部分
def packet_lisence(id,e,n):
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

    


#处理接收到的TGS的证书
def process_message_2001(cont_data,s):
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
    print("V生成的ACK:",mack)
    s.sendall(mack)
    print("成功发送ACK给TGS")
    serial_num=serial_num+1
    key_rcv=s.recv(1024)
    print("接受到的完整数据包内容:",key_rcv)
    secret_key=unpacket_key_head(key_rcv)
    secret_key=rsa.change_to_uint(secret_key)
    print("DES key 密文为:",secret_key)
    print("所使用的v私钥d,n为: ",d_v,n_v)
    key=rsa.rsa_decrypt(secret_key,d_v,n_v)

    print("我得到的DES key为: ",key)
    save_sql_key(id,int(key))
    flag='recv_2001'
    return flag

def process_message_2002():
    pass

def process_c_message_2007(data,s):
    global n_v,e_v
    ticket_v,authen_to_v,n_c=data.split(',') # str
    key_v=get_key_sql('1002')
    print("解密前的ticket[v]:",ticket_v)
    encry_tiket_v=des.decrypt(ticket_v,key_v) # str，可能要变
    print("解密后的ticket[v]:",encry_tiket_v)
    key_c_v,IDc,ADc,IDv,TS4,lifetime4=encry_tiket_v.split('|') # str
    save_sql_c(str(n_c),IDc)
    print("ticket[v]中C与V通信的KEY: ",key_c_v)
    now_time1=get_time()
    ts4=int(TS4)
    if now_time1-ts4>=100:
        cack=packet_ack(b'65434', b'1111', b'2000', b'0', b'0004', b'TS4TOtic')
        print("cack:",cack)
        s.sendall(cack)
    else:
        # print("k_cv",key_c_v)
        print("解密前的Authenticator:",authen_to_v)
        encry_anthen_to_v = des.decrypt(authen_to_v, key_c_v)  # str
        print("解密后的Authenticator:",encry_anthen_to_v)
        IDc_authen,ADc_authen,TS5=encry_anthen_to_v.split('|')
        now_time2 = get_time()
        ts5 = int(TS5)
        if now_time2-ts5>=100:
            cack2=packet_ack(b'65434', b'1111', b'2000', b'0', b'0005', b'TS5TOtic')
            print("cack2:",cack2)
            s.sendall(cack2)
        else:
            if ADc_authen==ADc:
                save_sql_key(IDc,key_c_v)
                # '把key_c_v存起来'
                ts6=ts5+1
                TS6=str(ts6)
                data_08=str(n_v)+','+str(e_v)+','+TS6
                print("V给C发送的Kerberos反馈内容",data_08)
                data_2008=des.encryption(data_08,key_c_v) # str
                print("加密后的V给C发送的Kerberos反馈内容",data_08)
                message_2008=packet_head(b'65434',b'1111',b'2008',b'0',b'0000',b'00000000',data_2008.encode())
                # print("message_2008:",message_2008)
                # a='发送一下'
                s.sendall(message_2008)
            else:
                print("!!!!!!!ADc_authen==ADc错了！！！！！")

# 使用字典存储每个值对应的处理函数
process_dict = {
    "2001": process_message_2001,
    "2002": process_message_2002,
}
#接收监听的处理字典
process_dict1 = {
    "2007": process_c_message_2007,
}

#发送的主线程 A发送->B接收->B发送->A接收
def send_thread():
    """发送数据线程函数"""
    print('V发送已启动,准备发送...')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT_TGS))
        root = tk.Tk()
        root.title("V所发送的内容")
        app = PrintToGUI(root)
        # 从命令行读取用户输入
        # print(type(threading.get_ident()))
        global serial_num,n_v,e_v,d_v
        # serial_num_byte=serial_num.to_bytes(4, byteorder='big') 
        print("V使用的公私钥: ")  
        n_v,e_v,d_v=getKey()
        save_sql_v(str(n_v),str(d_v))
        # print("e_v:",e_v,"n_v",n_v,"d_v",d_v)
        data=packet_lisence(b'1003',str(e_v).encode(),str(n_v).encode())
        # print("数据段：",data)
        message=packet_head(b'65433',str(serial_num).encode(),b'2001',b'0',b'0000',b'00000000',data)
        serial_num=serial_num+1
        # print(serial_num)
        # message = input("hi,i am tgs")
        # 发送数据到服务器
        s.sendall(message)
        #接收发送回来的内容，再关闭连接。
        rcv_message = s.recv(1024)
        # print("rcv_message:",rcv_message)
        type_message_rcv,pipei,cont_data_rcv=unpacket(rcv_message)
        # print("消息类型为:",type_message_rcv)
        # print("数据内容为:",cont_data_rcv)
        if type_message_rcv in process_dict:
                process_dict[type_message_rcv](cont_data_rcv,s)
        else:
            # 处理其他情况
            print("可能有错误")
        root.mainloop()

class PrintToGUI(object):
    def __init__(self, root):
        self.text = tk.Text(root)
        self.text.pack()

        # 重定向标准输出到Text小部件
        sys.stdout = self
          
    def write(self, message):
        self.text.insert(tk.END, str(message))

#接收的主线程
def receive_thread():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sss:
        # 绑定服务器IP地址和端口号
        sss.bind((HOST, PORT_V))
        # 开始监听
        sss.listen()
        print('V接收已启动,等待客户端连接...')

        # 定义一个客户端处理线程
        def handle_client(conn, addr):
            root = tk.Tk()
            root.title("V所接收到的内容")
            app = PrintToGUI(root)
            with conn:
                print('已连接到：', addr)
                message = conn.recv(1024)
                # 打印接收到的消息
                # print(message)
                type_message,pipei,cont_data=unpacket(message)
                print("接收到的消息类型: ",type_message)
                # print(type(type_message))
                # print("消息类型为:",type_message)
                # print("数据内容为:",cont_data)
                # print('收到来自客户端的消息：', data.decode())
                # print(data)
                # print('data: ',type(data),'data.decode',type(data.decode()))
                # 发送响应消息
                # 调用对应值的处理函数
                # solve(type_message,cont_data)
                if type_message in process_dict1:
                    flag=process_dict1[type_message](cont_data,conn)
                    # print("test",flag)
                    #result = sm.execute(flag)
                    #print(sm.state)  # 输出get_license

                else:
                    # 处理其他情况
                    print("消息类型可能有错误")
            root.mainloop()

        # 循环等待客户端连接
        while True:
            # 接收客户端连接请求
            conn, addr = sss.accept()
            # 创建一个新的线程来处理客户端请求
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()

# 创建监听线程
listen_thread = threading.Thread(target=receive_thread)
msend_thread = threading.Thread(target=send_thread)
listen_thread.start()
msend_thread.start()

