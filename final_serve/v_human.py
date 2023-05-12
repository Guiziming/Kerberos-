import tkinter as tk
from tkinter import Button, messagebox
from tkinter.messagebox import showinfo, showwarning, showerror
import time
import socket
import sys
import threading
import pymysql
import queue
from collections import Counter
from random import randint
import random
import os
import tkinter as tk
import RSA as rsa
import des_for_rsa as des

# HOST = '127.0.0.1'
HOST = '192.168.43.238'  # 服务端地址
PORT = 5000        # 服务端监听的端口号

# 拆包报头
def unpacket(packet):
    port, my_port, num, type_message, fin, pipei, rongyu, data = packet.decode().split("|")
    print("收到的完整数据包内容: ",packet)
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
    print(a_packet)
    return a_packet

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

#拆ACK
def unpacket_ack(cont_data):
    my_port,poserver_portrt,num,type_message,fin,pipei,rongyu=cont_data.decode().split("|")
    return pipei

def recv_zuobiao(data):
    x, y, color, baoliu = data.split(",")
    return x, y, color

# 生成签名
# 传入参数，byte,int,int
# 传出参数，int
def get_sign(data, d, n):
    sign = rsa.rsa_encrypt(data, d, n)
    return sign


# 拆签名
# 传入参数，int
# 传出参数，byte
def recv_sign(message, e, n):
    print("message, e, n",message, e, n)
    data = rsa.rsa_decrypt(message, e, n)
    return data

#获取v数据库中与tgs通信的密钥
def get_key_sql(id):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v')
    
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
    
    return result

#获取v数据库中与tgs通信的密钥
def get_c_sql(pipei):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v')
    
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    # sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
    # sql = "SELECT v_n v_d FROM mv WHERE v_id ='1003';"
    sql="SELECT * FROM mv WHERE v_id = '%s';" %pipei
    try:
        # 执行SQL语句
        cursor.execute(sql)
            # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            c_n = row[2]
            # v_d = row[3]
            # 打印结果
            # print("admin_id=%s,admin_pass=%s" % (admin_id, admin_pass))
    except:
        print("Error: unable to fecth data")
    return c_n

def get_myself_sql():
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v')
    
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    # sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
    # sql = "SELECT v_n v_d FROM mv WHERE v_id ='1003';"
    sql="SELECT * FROM mv WHERE v_id = '1003';" 
    v_n=''
    v_d=''
    try:
        # 执行SQL语句
        cursor.execute(sql)
            # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            v_n = row[2]
            v_d = row[3]
            # 打印结果
            # print("admin_id=%s,admin_pass=%s" % (admin_id, admin_pass))
    except:
        print("Error: unable to fecth data")
    return v_n,v_d

def get_coins(username):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    # sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
    # sql = "SELECT v_n v_d FROM mv WHERE v_id ='1003';"
    sql="SELECT * FROM mvinfo WHERE vinfo_id = '%s';" %username
    coins='0'
    try:
        # 执行SQL语句
        cursor.execute(sql)
            # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            coins = row[2]
            # v_d = row[3]
            # 打印结果
            # print("admin_id=%s,admin_pass=%s" % (admin_id, admin_pass))
    except:
        print("Error: unable to fecth data")
    return coins

def get_card(username):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    # sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
    # sql = "SELECT v_n v_d FROM mv WHERE v_id ='1003';"
    sql="SELECT * FROM mvinfo WHERE vinfo_id = '%s';" %username
    card='0'
    try:
        # 执行SQL语句
        cursor.execute(sql)
            # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            card = row[4]
            # v_d = row[3]
            # 打印结果
            # print("admin_id=%s,admin_pass=%s" % (admin_id, admin_pass))
    except:
        print("Error: unable to fecth data")
    return card

def get_rank(username):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    # sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
    # sql = "SELECT v_n v_d FROM mv WHERE v_id ='1003';"
    sql="SELECT * FROM mvinfo WHERE vinfo_id = '%s';" %username
    rank='0'
    try:
        # 执行SQL语句
        cursor.execute(sql)
            # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            rank = row[3]
            # v_d = row[3]
            # 打印结果
            # print("admin_id=%s,admin_pass=%s" % (admin_id, admin_pass))
    except:
        print("Error: unable to fecth data")
    return rank


def save_user_rank(username,new_rank):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    sql = "UPDATE mvinfo SET vinfo_rank='%s' WHERE vinfo_id='%s';" %(new_rank,username)
    # sql="SELECT * FROM mv WHERE v_id = '1003';" 
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交到数据库执行
    except:
        conn.rollback()  # 发生错误时回滚
        messagebox.showinfo('警告！', '数据库连接失败！')
    # 关闭游标和连接
    cursor.close()
    conn.close()
    

def save_coins_card(usrname,coins,card):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    sql = "UPDATE mvinfo SET vinfo_coin='%s',vinfo_card='%s' WHERE vinfo_id='%s';" %(coins,card,usrname)
    # sql="SELECT * FROM mv WHERE v_id = '1003';" 
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交到数据库执行
    except:
        conn.rollback()  # 发生错误时回滚
        messagebox.showinfo('警告！', '数据库连接失败！')
    # 关闭游标和连接
    cursor.close()
    conn.close()

def save_coins_yugui(coins,username):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    sql = "UPDATE mvinfo SET vinfo_coin='%s',vinfo_yugui='1' WHERE vinfo_id='%s';" %(coins,username)
    # sql="SELECT * FROM mv WHERE v_id = '1003';" 
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交到数据库执行
    except:
        conn.rollback()  # 发生错误时回滚
        messagebox.showinfo('警告！', '数据库连接失败！')
    # 关闭游标和连接
    cursor.close()
    conn.close()

def save_coins_kitty(coins,username):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    sql = "UPDATE mvinfo SET vinfo_coin='%s',vinfo_kitty='1' WHERE vinfo_id='%s';" %(coins,username)
    # sql="SELECT * FROM mv WHERE v_id = '1003';" 
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交到数据库执行
    except:
        conn.rollback()  # 发生错误时回滚
        messagebox.showinfo('警告！', '数据库连接失败！')
    # 关闭游标和连接
    cursor.close()
    conn.close()

def save_coins_ameng(coins,username):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    
    # 创建游标对象
    cursor = conn.cursor()


    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    sql = "UPDATE mvinfo SET vinfo_coin='%s',vinfo_ameng='1' WHERE vinfo_id='%s';" %(coins,username)
    # sql="SELECT * FROM mv WHERE v_id = '1003';" 
    try:
        cursor.execute(sql)  # 执行sql语句
        conn.commit()  # 提交到数据库执行
    except:
        conn.rollback()  # 发生错误时回滚
        messagebox.showinfo('警告！', '数据库连接失败！')
    # 关闭游标和连接
    cursor.close()
    conn.close()

def get_yugui(username):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    
    # 创建游标对象
    cursor = conn.cursor()

    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    # sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
    # sql = "SELECT v_n v_d FROM mv WHERE v_id ='1003';"
    sql="SELECT * FROM mvinfo WHERE vinfo_id = '%s';" %username
    flag='0'
    try:
        # 执行SQL语句
        cursor.execute(sql)
            # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            flag = row[5]
            # v_d = row[3]
            # 打印结果
            # print("admin_id=%s,admin_pass=%s" % (admin_id, admin_pass))
    except:
        print("Error: unable to fecth data")
    return flag

def get_kitty(username):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    
    # 创建游标对象
    cursor = conn.cursor()

    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    # sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
    # sql = "SELECT v_n v_d FROM mv WHERE v_id ='1003';"
    sql="SELECT * FROM mvinfo WHERE vinfo_id = '%s';" %username
    flag='0'
    try:
        # 执行SQL语句
        cursor.execute(sql)
            # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            flag = row[6]
            # v_d = row[3]
            # 打印结果
            # print("admin_id=%s,admin_pass=%s" % (admin_id, admin_pass))
    except:
        print("Error: unable to fecth data")
    return flag

def get_user_rank(username):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    
    # 创建游标对象
    cursor = conn.cursor()

    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    # sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
    # sql = "SELECT v_n v_d FROM mv WHERE v_id ='1003';"
    sql="SELECT * FROM mvinfo WHERE vinfo_id = '%s';" %username
    flag='0'
    try:
        # 执行SQL语句
        cursor.execute(sql)
            # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            flag = row[3]
            # v_d = row[3]
            # 打印结果
            # print("admin_id=%s,admin_pass=%s" % (admin_id, admin_pass))
    except:
        print("Error: unable to fecth data")
    return flag


def get_ameng(username):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    
    # 创建游标对象
    cursor = conn.cursor()

    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    # sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
    # sql = "SELECT v_n v_d FROM mv WHERE v_id ='1003';"
    sql="SELECT * FROM mvinfo WHERE vinfo_id = '%s';" %username
    flag='0'
    try:
        # 执行SQL语句
        cursor.execute(sql)
            # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            flag = row[7]
            # v_d = row[3]
            # 打印结果
            # print("admin_id=%s,admin_pass=%s" % (admin_id, admin_pass))
    except:
        print("Error: unable to fecth data")
    return flag



def row_column_win(x,m,n,chess):
    for i in x:
        if x[i]>=5:
            xy=[]
            for j in chess:
                if j[m]==i:
                    xy.append(j[n])
            xy.sort()
            count=0
            for j in range(len(xy)-1):
                if xy[j]+1==xy[j+1]:
                    count+=1
                else:
                    count=0
            if count>=4:
                return 1

def xiejiao_win(chess):
    x,y=[],[]
    chess.sort()
    for i in chess:
        x.append(i[0])
        y.append(i[1])
    c,first,last=0,0,0
    for i in range(len(x)-1):
        if x[i+1]!=x[i]:
            if x[i]+1==x[i+1]:
                c+=1
                last=i+1
            else:
                if c<4:
                    first=i+1
                    c=0
                else:
                    last=i
                    print(last)
                    break
        else:
            last=i+1
    if c>=4:
        dis=[]
        for i in range(first,last+1):
            dis.append(x[i]-y[i])
        count=Counter(dis)
        for i in count:
            if count[i]>=5:
                return 1
        dis=[]
        x2=[i*(-1) for i in x]
        for i in range(first,last+1):
            dis.append(x2[i]-y[i])
        count=Counter(dis)
        for i in count:
            if count[i]>=5:
                return 1

def gameover(wcx,wcy,bcx,bcy,white_chess,black_chess):
    wcx_count,wcy_count,bcx_count,bcy_count=Counter(wcx),Counter(wcy),Counter(bcx),Counter(bcy)
    if row_column_win(wcx_count,0,1,white_chess)==1:
        return 0
    elif row_column_win(bcx_count,0,1,black_chess)==1:
        return 1
    elif row_column_win(wcy_count,1,0,white_chess)==1:
        return 0
    elif row_column_win(bcy_count,1,0,black_chess)==1:
        return 1
    elif xiejiao_win(white_chess)==1:
        return 0
    elif xiejiao_win(black_chess)==1:
        return 1
    else:
        return 2

def recv_zuobiao (data):
    x,y,color = data.split(",")
    return x,y,color

def recv_2019(pipei,cont_data):
    print("C的证书ID",pipei)
    key_c_v = get_key_sql(pipei)
    # print("cont_data_2019:",cont_data)
    decry_message_2019 = des.decrypt(cont_data, key_c_v)  # str
    print("解密后的2019(棋子信息)报文内容:",decry_message_2019)
    data_2019, sign_2019 = decry_message_2019.split('|')  # str
    #goods_type,username=data_2022.split(',')
    ec=65537
    n_c = get_c_sql(pipei)
    nv,dv=get_myself_sql()
    nv=int(nv)
    dv=int(dv)
    data_sign_2019 = recv_sign(int(sign_2019), ec, int(n_c)).decode()
    # print("data_sign_2019: ",data_sign_2019)
    if '2019'==data_sign_2019:
        print("验签成功！")
        return data_2019
    else:
        print("第一条信息验签错误")
        return '1'
        
def send_packet_2019(data,pipei):
    key_c_v = get_key_sql(pipei)
    nv,dv=get_myself_sql()
    nv=int(nv)
    dv=int(dv)
    sign_2019 = get_sign(b'2019', dv, nv)
    message_2019 = data + '|' + str(sign_2019)
    print("加密前的2019（双人对战）内容：",message_2019)
    encry_message_2019 = des.encryption(message_2019, key_c_v)  # str
    packet_2019 = packet_head(b'65434', b'1111', b'2019', b'0', b'1004', b'00000000', encry_message_2019.encode())
    return packet_2019


class PrintToGUI(object):
    def __init__(self, root):
        self.text = tk.Text(root)
        self.text.pack()

        # 重定向标准输出到Text小部件
        sys.stdout = self
          
    def write(self, message):
        self.text.insert(tk.END, str(message))

def handle_client_request(client_socket,addr):
    root = tk.Tk()
    root.title("V_human所接收到的内容")
    app = PrintToGUI(root)
    # 接收玩家的用户名并加入等待队列
    print("已连接到: ",addr)
    # print('已连接到：', addr)
    packet_all=client_socket.recv(1024)
    # print("packet_all",packet_all)
    type_message,pipei,data=unpacket(packet_all) #str
    username=recv_2019(pipei,data)
    # print("存放队列之前的username:",username)
    # username = client_socket.recv(1024).decode()
    wait_queue.put((username,pipei,client_socket))
    # print("我接受到的玩家: ",wait_queue)
    # 如果等待队列中有两个玩家，则开始游戏
    if wait_queue.qsize() == 2:
        # 从等待队列中取出两个玩家并开始游戏
        username_1,pipei_1,socket1 = wait_queue.get()
        username_2,pipei_2,socket2 = wait_queue.get()
        print('正在双人对战的玩家1: ',username_1,"玩家2: ",username_2)
        user_rank_1=get_user_rank(username_1)
        user_rank_2=get_user_rank(username_2)
        user_color_1='0'
        user_color_2='1'
        # 发送游戏开始的消息给两个玩家
        message1=username_1+','+user_rank_1+','+user_color_1+','+username_2+','+user_rank_2+','+user_color_2
        packet_2019_1=send_packet_2019(message1,pipei_1)
        socket1.sendall(packet_2019_1)
        message2=username_2+','+user_rank_2+','+user_color_2+','+username_1+','+user_rank_1+','+user_color_1
        packet_2019_2=send_packet_2019(message2,pipei_2)
        socket2.sendall(packet_2019_2)
        #黑白棋子初始化
        black_chess,white_chess=[],[]
        wcx,wcy,bcx,bcy=[],[],[],[]
        play_count=2 
        # 等待两个玩家依次下棋
        while True:
            packet_2019=socket1.recv(1024)
            type_message_2019,pipei_2019,message_2019=unpacket(packet_2019)
            position1=recv_2019(pipei_2019,message_2019)
            # position1 = socket1.recv(1024)
            #row1, col1 = map(int, position1.split(','))
            # print(position1,type(position1))
                        
            # black_message=position1
            #接收玩家一的消息并向玩家二发送反馈信息
            if position1=='surrender':
                print("玩家一认输")
                data="enemy_surrender"
                rank_1=get_user_rank(username_1)
                rank_1_int=int(rank_1)-50
                save_user_rank(username_1,str(rank_1_int))
                message_renshu=send_packet_2019(data,pipei_2)
                socket2.sendall(message_renshu)

                rank_2=get_user_rank(username_2)
                rank_2_int=int(rank_2)+50
                save_user_rank(username_2,str(rank_2_int))
                break
            elif position1=='i_run':
                if play_count==2:
                    print("走了一个")
                    play_count=play_count-1
                    data="enemy_surrender"
                    rank_1=get_user_rank(username_1)
                    rank_1_int=int(rank_1)-50
                    save_user_rank(username_1,str(rank_1_int))
                    message_renshu=send_packet_2019(data,pipei_2)
                    socket2.sendall(message_renshu)
                    rank_2=get_user_rank(username_2)
                    rank_2_int=int(rank_2)+50
                    save_user_rank(username_2,str(rank_2_int))
                    break
                else:
                    break
            else:
                message_qizi=send_packet_2019(position1,pipei_2)
                socket2.sendall(message_qizi)
                # socket2.sendall(position1)
            
            # 玩家1下棋
            # position1 = socket1.recv(1024)
            # #row1, col1 = map(int, position1.split(','))
            # print(position1,type(position1))
                       
            
            col1,row1,color1=position1.split(",")
            row1_int=int(row1)
            col1_int=int(col1)
            black_chess.append([col1_int,row1_int])
            bcx.append(black_chess[-1][0])
            bcy.append(black_chess[-1][1])
            # print("黑棋序列：",black_chess)

            #玩家一下棋后判断战局情况
            flag_win=gameover(wcx,wcy,bcx,bcy,white_chess,black_chess)
            if flag_win==1:
                print("黑棋赢了")
                data_1='you_win'
                rank_1=get_user_rank(username_1)
                rank_1_int=int(rank_1)+50
                save_user_rank(username_1,str(rank_1_int))

                message_result1=send_packet_2019(data_1,pipei_1)
                socket1.sendall(message_result1)
                data_2='you_fail'

                rank_2=get_user_rank(username_2)
                rank_2_int=int(rank_2)-50
                save_user_rank(username_2,str(rank_2_int))
                message_result2=send_packet_2019(data_2,pipei_2)
                socket2.sendall(message_result2)
                # socket2.sendall(('你输了').encode())
                break
            elif flag_win==0:
                print("白棋赢了")
                data_2='you_win'
                rank_2=get_user_rank(username_2)
                rank_2_int=int(rank_2)+50
                save_user_rank(username_2,str(rank_2_int))
                message_result2=send_packet_2019(data_2,pipei_2)
                socket2.sendall(message_result2)

                data_1='you_fail'
                rank_1=get_user_rank(username_1)
                rank_1_int=int(rank_1)-50
                save_user_rank(username_1,str(rank_1_int))
                message_result1=send_packet_2019(data_1,pipei_1)
                socket1.sendall(message_result1)
                # socket2.sendall(('你赢了').encode())
                # socket1.sendall(('你输了').encode())
                break
            else:
                print("游戏继续")
                data_all='game_continue'
                message_result2=send_packet_2019(data_all,pipei_2)
                socket2.sendall(message_result2)
                
                message_result1=send_packet_2019(data_all,pipei_1)
                socket1.sendall(message_result1)
                # socket2.sendall(('游戏继续').encode())
                # socket1.sendall(('游戏继续').encode())

            # 玩家2下棋
            # position2 = socket2.recv(1024)
            
            packet_2019=socket2.recv(1024)
            type_message_2019,pipei_2019,message_2019=unpacket(packet_2019)
            position2=recv_2019(pipei_2019,message_2019)
            # white_message=position2
            if position2=='surrender':
                print("玩家二认输")
                data="enemy_surrender"
                rank_2=get_user_rank(username_2)
                rank_2_int=int(rank_2)-50
                save_user_rank(username_2,str(rank_2_int))

                message_renshu=send_packet_2019(data,pipei_1)
                socket1.sendall(message_renshu)
                rank_1=get_user_rank(username_1)
                rank_1_int=int(rank_1)+50
                save_user_rank(username_1,str(rank_1_int))
                break
            elif position2=='i_run':
                if play_count==2:
                    print("走了一个")
                    play_count=play_count-1
                    data="enemy_surrender"
                    rank_2=get_user_rank(username_2)
                    rank_2_int=int(rank_2)-50
                    save_user_rank(username_2,str(rank_2_int))
                    message_renshu=send_packet_2019(data,pipei_1)
                    socket1.sendall(message_renshu)
                    rank_1=get_user_rank(username_1)
                    rank_1_int=int(rank_1)+50
                    save_user_rank(username_1,str(rank_1_int))
                    break
                else:
                    break
            else:
                message_qizi=send_packet_2019(position2,pipei_1)
                socket1.sendall(message_qizi)

            #接收玩家二的消息并向玩家一发送反馈信息
            # if position2.decode()=='认输':
            #     print("玩家一认输")
            #     text="对方认输"
            #     socket1.sendall(text.encode())
            #     break
            # elif position2.decode()=='我跑了':
                
            #     if play_count==2:
            #         print("走了一个")
            #         play_count=play_count-1
            #         text="对方认输"
            #         socket1.sendall(text.encode())
            #         break
            #     else:
            #         break
            # else:
            #     socket1.sendall(position2)
            # socket1.sendall(position2)
            col2, row2,color2=position2.split(',')
            row2_int=int(row2)
            col2_int=int(col2)
            white_chess.append([col2_int,row2_int])
            # print("白棋序列：",white_chess)
            wcx.append(white_chess[-1][0])
            wcy.append(white_chess[-1][1])

            #玩家二下棋后判断战局情况
            flag_win=gameover(wcx,wcy,bcx,bcy,white_chess,black_chess)
            if flag_win==1:
                print("黑棋赢了")
                data_1='you_win'
                rank_1=get_user_rank(username_1)
                rank_1_int=int(rank_1)+50
                save_user_rank(username_1,str(rank_1_int))

                message_result1=send_packet_2019(data_1,pipei_1)
                socket1.sendall(message_result1)
                data_2='you_fail'

                rank_2=get_user_rank(username_2)
                rank_2_int=int(rank_2)-50
                save_user_rank(username_2,str(rank_2_int))
                message_result2=send_packet_2019(data_2,pipei_2)
                socket2.sendall(message_result2)
                # socket2.sendall(('你输了').encode())
                break
            elif flag_win==0:
                print("白棋赢了")
                data_2='you_win'
                rank_2=get_user_rank(username_2)
                rank_2_int=int(rank_2)+50
                save_user_rank(username_2,str(rank_2_int))
                message_result2=send_packet_2019(data_2,pipei_2)
                socket2.sendall(message_result2)

                data_1='you_fail'
                rank_1=get_user_rank(username_1)
                rank_1_int=int(rank_1)-50
                save_user_rank(username_1,str(rank_1_int))
                message_result1=send_packet_2019(data_1,pipei_1)
                socket1.sendall(message_result1)
                # socket2.sendall(('你赢了').encode())
                # socket1.sendall(('你输了').encode())
                break
            else:
                print("游戏继续")
                data_all='game_continue'
                message_result2=send_packet_2019(data_all,pipei_2)
                socket2.sendall(message_result2)
                
                message_result1=send_packet_2019(data_all,pipei_1)
                socket1.sendall(message_result1)
            
    root.mainloop()

# 创建一个TCP/IP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定服务器的地址和端口号
server_address = (HOST, PORT)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# 监听连接
sock.listen(10)#10个客户端
print('Waiting for a connection...')
# 创建一个等待队列，存储已经登录的玩家
wait_queue = queue.Queue()

while True:
    # 等待连接
    conn, addr = sock.accept()
    print('Connection from', addr)

    # 创建一个新线程处理客户端请求
    client_thread = threading.Thread(target=handle_client_request, args=(conn, addr))
    client_thread.start()
