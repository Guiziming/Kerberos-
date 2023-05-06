#AS接收数据，接收C或TGS的数据，接受过后拆分后判断数据类型之后再处理
import threading
import socket
import pymysql
import tkinter.messagebox as messagebox  # 弹窗
import RSA as rsa
import des_for_rsa as des
import datetime
# 定义服务器IP地址和端口号
HOST_AS = '192.168.43.238'
# HOST_AS = '127.0.0.1'
PORT_AS = 65432
lifetime='43200'


class StateMachine:
    def __init__(self):
        self.state = 'listen'
        self.transitions = {
            'listen': {'recv_2001': 'get_license', 'recv_2003': 'recv_vertify_req'},
            'get_license': {'vertify_uerful': 'send_my_license','vertify_useless':'send_error'},
            'send_my_license': {'recv_2000': 'send_key'},
            'send_key':{'end_thread':'listen'},
            'recv_vertify_req':{'vertify_C':'send_ticket','vertify_c_useless':'send_error'},
            'send_ticket':{'end_thread':'listen'},
            "send_error":{'end_thread':'listen'}
        }


    def execute(self, operation):
        if operation in self.transitions[self.state]:
            self.state = self.transitions[self.state][operation]
            return True
        else:
            print('状态错误')
            return False

# 初始化状态机
sm = StateMachine()

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

#打包报头部分
def packet_head(port, num, type_message, fin, pipei,rongyu, data):
    my_port = port
    # print(my_port)
    server_port =port
    # print(server_port)
    serial_num = num
    # print(serial_num)
    type_mes = type_message
    # print(type_mes)
    FIN = fin
    pipei_num=pipei
    baoliu = rongyu
    baotou = my_port + b'|' + server_port + b'|' + serial_num + b'|' + type_mes + b'|' + FIN + b'|' +pipei_num+b'|'+ baoliu
    a_packet = baotou + b'|' + data
    print(a_packet)
    return a_packet

#打包data部分
def packet_lisence(id,e,n):
    return id + b',' + e + b',' +n

def find_id(id):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='as')
    print("数据库连接成功")
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    sql = "SELECT COUNT(*) FROM mas WHERE as_id = '%s';"%(id)
    
    cursor.execute(sql)  # 执行sql语句
    result = cursor.fetchone()[0]
    print('判断id:',result,type(result))
    # try:
    #     cursor.execute(sql)  # 执行sql语句
    #     conn.commit()  # 提交到数据库执行

    # except:
    #     conn.rollback()  # 发生错误时回滚
    #     messagebox.showinfo('警告！', 'ID数据库连接失败！')


    # 关闭游标和连接
    cursor.close()
    conn.close()
    if result==0:
        return 0
    else:
        return 1


#将拆后的data部分存入AS数据库中
def save_sql(id,e,n):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='as')
    print("数据库连接成功")
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交到数据库执行
        
    except:
        conn.rollback()  # 发生错误时回滚
        messagebox.showinfo('警告！', 'DATA数据库连接失败！')


    # 关闭游标和连接
    cursor.close()
    conn.close()
    

#获取AS数据库中与C通信的密钥
def get_key_sql(id):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='as')
    print("数据库连接成功")
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    # sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
    sql = "SELECT as_key FROM mas WHERE as_id ='%s';" %(id)
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
    print('数据库中的key:',result,type(result))
    return result

def save_sql_key(key,id):
     # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='as')
    print("数据库连接成功")
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    sql = "UPDATE mas SET as_key='%s' WHERE as_id='%s';" %(key,id)
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交到数据库执行
    except:
        conn.rollback()  # 发生错误时回滚
        messagebox.showinfo('警告！', '数据库连接失败！')


    # 关闭游标和连接
    cursor.close()
    conn.close()

#拆ACK
def unpacket_ack(cont_data):
    my_port,poserver_portrt,num,type_message,fin,pipei,rongyu=cont_data.decode().split("|")
    return pipei


#拆data部分
def unpacket_lisence(cont_data):
    id,e,n = cont_data.split(",")
    return id,e,n
    # return id,e,n

def change_to_uint(str):
    result = int.from_bytes(str, 'big')
    return result
#Kerberos处理2003内容
def unpacket_2003(data):
    print('data:::::;',data)
    IDc,IDtgs,TS1=data.encode().split(b",")
    ts1=change_to_uint(TS1)
    now_time=get_time()
    if now_time-ts1<=10:
        return IDc.decode(),IDtgs.decode()
    else:
        return 'error','error'
    
#最大的拆包，将报头和数据部分分开
def unpacket(packet):
    port,my_port, num, type_message, fin,pipei, rongyu, data = packet.decode().split("|")
    print("来源端口", port,"类型",type(port))
    print("序列号", num)
    print("信息类型", type_message)
    print("结束标识", fin)
    print("数据", data)
    return type_message,data

def unpacket_key_head(packet):
    port, my_port, num, type_message, fin, pipei, rongyu, data=packet.split(b'|')
    print("这个的data是: ",data)
    print("信息类型", type_message)
    print("类型为:",type(data))
    return type_message,data

#生成ticket,传入参数是str类型
def get_ticket_tgs(key,IDc,IDtgs,TS2,key_c):
    ADc='aaaa'
    message=key+'|'+IDc+'|'+ADc+'|'+IDtgs+'|'+TS2+'|'+lifetime
    print(message,type(message))
    print(key_c,type(key_c))
    ticket_tgs=des.encryption(message,key_c)
    print(ticket_tgs,type(ticket_tgs))
    return ticket_tgs

# 生成2004报文数据段，传入参数IDtgs是byte类型,key和TS2和ticket是str
def get_data_to_c(key,IDtgs,TS2,ticket):
    data_to_c=key.encode()+b','+IDtgs.encode()+b','+TS2.encode()+b','+lifetime.encode()+b','+ticket.encode()
    return data_to_c

def process_message_2000(cont_data,e,n,id):
    pipei=unpacket_ack(cont_data)
    print("pipei: ",pipei)
    if pipei=='1001':
        process_message_2002(e,n,id)
    else:
        print("可能错了")

#传递证书的报文
def process_message_2001(cont_data):
    # print("已接收到消息类型为2001的数据段,是传递证书的报文")
    print("拆除掉报头部分的内容: ",cont_data)
    #得到id、e、n
    id,e,n=unpacket_lisence(cont_data)
    print("id:",id,"e:",e,"n",n)
    #将id、e、n存入数据库中
    save_sql(id,e,n)
    #需要发送AS自己的证书
    n_as,e_as,d_as=rsa.getKey()
    data=packet_lisence(b'1001',str(e_as).encode(),str(n_as).encode())
    # message=packet_head(b'65432',str(serial_num).encode(),b'2001',b'0',b'00000000',b'sxwnbb')
    message=packet_head(b'65432',b'2',b'2001',b'0',b'0000',b'00000000',data)
    conn.sendall(message)
    print("已成功发送AS证书!")
    ack_message=conn.recv(1024)
    print("成功接收传递来的ack")
    print("ACK:",ack_message)
    process_message_2000(ack_message,e,n,id)

    flag='recv_2001'
    return flag
    

def process_message_2002(e,n,id):
    print("AS开始给TGS发送key")
    # 传输2002号报文给tgs（发key）
    tmp_key=des.get_key()
    print("创建的DES key为: ",tmp_key)
    save_sql_key(tmp_key,id)
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
    print("as的key:",key)
    #发送key
    conn.sendall(key_message)

def process_message_2003(cont_data):
    print("kerberos过程拆除掉报头部分的内容:",cont_data)
    idc,idtgs=unpacket_2003(cont_data)
    if idc == 'error':
        mack=packet_ack(b'65432',b'3',b'2000',b'0',b'0000',b'ts1to')
        conn.sendall(mack)
    else:
        flag=find_id(idc)
        if flag==1:
            Key_c_to_tgs=des.get_key()
            print('idc类型',idc,type(idc))
            keyc=get_key_sql(idc)
            IDc='1004'
            IDtgs="1002"
            ts = get_time()
            TS2 = str(ts)
            ticket_tgs=get_ticket_tgs(Key_c_to_tgs,IDc,IDtgs,TS2,keyc)
            print('key_c_to_tgs',type(Key_c_to_tgs))
            print('IDtgs',type(IDtgs),'TS2',type(TS2),'ticket_tgs',type(ticket_tgs))
            data_c=get_data_to_c(Key_c_to_tgs,IDtgs,TS2,ticket_tgs)
            data_c=data_c.decode()
            # print("！！！加密前：",data_c)
            data_to_c=des.encryption(data_c,keyc).encode()
            # print("！！！加密后：",data_to_c)
            # data_to_c2=des.decrypt(data_to_c,keyc).encode()
            # print("！！！解密后：",data_to_c2)
            # print('加密用的key',keyc)
            message_2004=packet_head(b'65433',b'1000',b'2004',b'0',b'0000',b'00000000',data_to_c)
            conn.sendall(message_2004)
            print("AS过程完成")
        else:
            mack2=packet_ack(b'65432',b'3',b'2000',b'0',b'0000',b'vertify')
            conn.sendall(mack2)
            error_c=conn.recv(1024)
            print("ticket[tgs] timeout!")
            



# 使用字典存储每个值对应的处理函数
process_dict = {
    "2001": process_message_2001,
    "2002": process_message_2002,
    "2003": process_message_2003,
}


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
            message = conn.recv(1024)
            # 打印接收到的消息
            print(message)
            type_message,cont_data=unpacket(message)
            #type_message,cont_data=unpacket_key_head(message)
            # cont_data=cont_data.decode()
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
                flag=process_dict[type_message](cont_data)
                print("test",flag)
                result = sm.execute(flag)
                print(sm.state)  # 输出get_license

            else:
                # 处理其他情况
                print("可能有错误")
            # conn.sendall(b'Received: ' + message)
            # while True:
            #     # 接收客户端发送的消息
            #     data = conn.recv(1024)
            #     if not data:
            #         break
            #     # 打印接收到的消息
            #     print(data)
            #     cont_data=unpacket(data)
            #     print("数据内容为:",cont_data)
            #     # print('收到来自客户端的消息：', data.decode())
            #     # print(data)
            #     # print('data: ',type(data),'data.decode',type(data.decode()))
            #     # 发送响应消息
            #     conn.sendall(b'Received: ' + data)

    # 循环等待客户端连接
    while True:
        # 接收客户端连接请求
        conn, addr = s.accept()
        # 创建一个新的线程来处理客户端请求
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start()
