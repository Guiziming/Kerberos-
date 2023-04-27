#AS接收数据，接收C或TGS的数据，接受过后拆分后判断数据类型之后再处理
import threading
import socket
import pymysql
import tkinter.messagebox as messagebox  # 弹窗

# 定义服务器IP地址和端口号
HOST_AS = '192.168.43.238'
PORT_AS = 65432

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


#将拆后的data部分存入AS数据库中
def save_sql(id,e,n):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='as')
    print("数据库连接成功")
    # 创建游标对象
    cursor = conn.cursor()

    # 执行SQL语句
    sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交到数据库执行
    except:
        conn.rollback()  # 发生错误时回滚
        messagebox.showinfo('警告！', '数据库连接失败！')


    # 关闭游标和连接
    cursor.close()
    conn.close()

#拆data部分
def unpacket_data(cont_data):
    id,e,n = cont_data.split(",")
    return id,e,n
    # return id,e,n

#最大的拆包，将报头和数据部分分开
def unpacket(packet):
    port,my_port, num, type_message, fin, rongyu, data = packet.decode().split("|")
    print("来源端口", port,"类型",type(port))
    print("序列号", num)
    print("信息类型", type_message)
    print("结束标识", fin)
    print("数据", data)
    return type_message,data

#传递证书的报文
def process_message_2001(cont_data):
    # print("已接收到消息类型为2001的数据段,是传递证书的报文")
    print("拆除掉报头部分的内容: ",cont_data)
    #得到id、e、n
    id,e,n=unpacket_data(cont_data)
    print("id:",id,"e:",e,"n",n)
    #将id、e、n存入数据库中
    save_sql(id,e,n)
    #需要发送自己的证书和key给TGS
    # message=packet_head(b'65432',str(serial_num).encode(),b'2001',b'0',b'00000000',b'sxwnbb')
    message=packet_head(b'65432',b'2',b'2001',b'0',b'00000000',b'sxwnbb')
    conn.sendall(message)
    #状态机输出当前状态
    result = sm.execute('recv_2001')
    print(sm.state)  # 输出get_license

def process_message_2002():
    pass

# 使用字典存储每个值对应的处理函数
process_dict = {
    "2001": process_message_2001,
    "2002": process_message_2002,
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
            # print(type(type_message))
            # print("消息类型为:",type_message)
            # print("数据内容为:",cont_data)
            # print('收到来自客户端的消息：', data.decode())
            # print(data)
            # print('data: ',type(data),'data.decode',type(data.decode()))
            # 发送响应消息
            # 调用对应值的处理函数
            if type_message in process_dict:
                process_dict[type_message](cont_data)
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