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
# from start_menu import start_menu

HOST_SERVE = '192.168.43.238'
# HOST = '192.168.43.238'  # 服务端地址
PORT_V_SERVE = 65435        # 服务端监听的端口号
MAX = 1008611

level = 13
grade = 10

BOARD_SIZE=13
AI_PLAYER=2

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
    print("发送的完整数据包内容: ",a_packet)
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
    print("验签使用的公钥: ", e, n)
    data = rsa.rsa_decrypt(message, e, n)
    return data

# 获取2010数据段，注册成功flag为1
# 传入参数为byte,int,int
def get_message_2010(enroll_flag,dv,nv):
    sign_2010=get_sign(enroll_flag,dv,nv) #int
    message_2010=enroll_flag.decode()+'|'+str(sign_2010)
    return message_2010

# byte,int,int->str
def get_message_2012(enroll_flag,dv,nv):
    print("签名使用的私钥是:",dv,nv)
    sign_2012=get_sign(b'2012',dv,nv) #int
    print("sign_2012",sign_2012)
    message_2012=enroll_flag.decode()+'|'+str(sign_2012)
    return message_2012

# 人机模式
# str,str,int.int->str
def get_message_2014(data,dv,nv):
    # data=ID+','+scoring
    sign_2014=get_sign(b'2014',dv,nv)
    message_2014=data+'|'+str(sign_2014)
    return message_2014


# 双人模式
def get_message_2015(ID,scoring,dv,nv):
    data = ID + ',' + scoring
    sign_2015 = get_sign(data.encode(), dv, nv)
    message_2015 = data + '|' + str(sign_2015)
    return message_2015

# 排名反馈
def get_message_2016(data,dv,nv):
    #data=ID+','+scoring+','+flag_send
    sign_2016 =get_sign(b'2016',dv,nv)
    message_2016=data+'|'+str(sign_2016)
    return message_2016

# 购买物品反馈
def get_message_2018(scoring,coin,card,skin_type,dv,nv):
    data=scoring+','+coin+','+card+','+skin_type
    sign_2018=get_sign(b'2018',dv,nv)
    message_2018=data+'|'+str(sign_2018)
    return message_2018


#获取v数据库中与tgs通信的密钥
def get_key_sql(id):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v')
    # 
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

#获取v数据库中与tgs通信的密钥
def get_c_sql(pipei):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v')
    # 
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
    # 
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
    # 
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
    # 
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

# def get_rank(username):
#     # 连接数据库
#     conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
#     
#     # 创建游标对象
#     cursor = conn.cursor()


#     # # 执行SQL语句
#     # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
#     # sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
#     # sql = "SELECT v_n v_d FROM mv WHERE v_id ='1003';"
#     sql="SELECT * FROM mvinfo WHERE vinfo_id = '%s';" %username
#     rank='0'
#     try:
#         # 执行SQL语句
#         cursor.execute(sql)
#             # 获取所有记录列表
#         results = cursor.fetchall()
#         for row in results:
#             rank = row[3]
#             # v_d = row[3]
#             # 打印结果
#             # print("admin_id=%s,admin_pass=%s" % (admin_id, admin_pass))
#     except:
#         print("Error: unable to fecth data")
#     return rank


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
    # 
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
    # 
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
    # 
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
    # 
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

def get_rank():
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    
    # 创建游标对象
    cursor = conn.cursor()

    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    # sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
    # sql = "SELECT v_n v_d FROM mv WHERE v_id ='1003';"
    sql="SELECT vinfo_id, vinfo_rank from mvinfo ORDER BY vinfo_rank DESC;"
    flag='0'
    try:
        # 执行SQL语句
        cursor.execute(sql)
            # 获取所有记录列表
        flag = cursor.fetchall()
    except:
        print("Error: unable to fecth data")
    return flag

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
        return '1'
        
def send_packet_2019(data,dv,nv,key_c_v,pipei):
    sign_2019 = get_sign(b'2019', dv, nv)
    message_2019 = data + '|' + str(sign_2019)
    print("加密前的2019（人机模式）内容：",message_2019)
    encry_message_2019 = des.encryption(message_2019, key_c_v)  # str
    packet_2019 = packet_head(b'65434', b'1111', b'2019', b'0', pipei.encode(), b'00000000', encry_message_2019.encode())
    return packet_2019

def Autoplay(ch, m, n):
    # a1 = [1,-1,1,-1,1,-1,0,0]
    # b1 = [1,-1,-1,1,0,0,1,-1]
    # rand = randint(0,7)
    # while m+a1[rand]>=0 and m+a1[rand]<level and n+b1[rand]>=0 and n+b1[rand]<level and ch[m+a1[rand]][n+b1[rand]]!=0 :
    #     rand = randint(0,7)
    # if(ch[m+ a1[rand]][n+b1[rand]]==0):
    #     return m + a1[rand], n+b1[rand]
    # else:
    #     Autoplay(ch,m,n)
    # print(ch)
    available_moves = []
    
    # 遍历周围8个位置
    for i in range(max(0, m-1), min(m+2, len(ch))):
        for j in range(max(0, n-1), min(n+2, len(ch[0]))):
            # 如果该位置为空，则添加到可用坐标列表
            if ch[j][i] == 0:
                available_moves.append((i, j))
    # print("此时可用的坐标: ",available_moves)
    # 如果存在可用坐标，则从中随机选择一个返回
    if available_moves:
        return random.choice(available_moves)
    
    # 如果没有可用坐标，则返回None
    return None

def Scan(chesspad, color):
    shape = [[[0 for high in range(5)] for col in range(13)] for row in range(13)]
    # 扫描每一个点，然后在空白的点每一个方向上做出价值评估！！
    for i in range(13):
        for j in range(13):

            # 如果此处为空 那么就可以开始扫描周边
            if chesspad[i][j] == 0:
                m = i
                n = j
                # 如果上方跟当前传入的颜色参数一致，那么加分到0位！
                while n - 1 >= 0 and chesspad[m][n - 1] == color:
                    n -= 1
                    shape[i][j][0] += grade
                if n-1>=0 and chesspad[m][n - 1] == 0:
                    shape[i][j][0] += 1
                if n-1 >= 0 and chesspad[m][n - 1] == -color:
                    shape[i][j][0] -= 2
                m = i
                n = j
                # 如果下方跟当前传入的颜色参数一致，那么加分到0位！
                while (n + 1 < level  and chesspad[m][n + 1] == color):
                    n += 1
                    shape[i][j][0] += grade
                if n + 1 < level  and chesspad[m][n + 1] == 0:
                    shape[i][j][0] += 1
                if n + 1 < level  and chesspad[m][n + 1] == -color:
                    shape[i][j][0] -= 2
                m = i
                n = j
                # 如果左边跟当前传入的颜色参数一致，那么加分到1位！
                while (m - 1 >= 0 and chesspad[m - 1][n] == color):
                    m -= 1
                    shape[i][j][1] += grade
                if m - 1 >= 0 and chesspad[m - 1][n] == 0:
                    shape[i][j][1] += 1
                if m - 1 >= 0 and chesspad[m - 1][n] == -color:
                    shape[i][j][1] -= 2
                m = i
                n = j
                # 如果右边跟当前传入的颜色参数一致，那么加分到1位！
                while (m + 1 < level  and chesspad[m + 1][n] == color):
                    m += 1
                    shape[i][j][1] += grade
                if m + 1 < level  and chesspad[m + 1][n] == 0:
                    shape[i][j][1] += 1
                if m + 1 < level  and chesspad[m + 1][n] == -color:
                    shape[i][j][1] -= 2
                m = i
                n = j
                # 如果左下方跟当前传入的颜色参数一致，那么加分到2位！
                while (m - 1 >= 0 and n + 1 < level  and chesspad[m - 1][n + 1] == color):
                    m -= 1
                    n += 1
                    shape[i][j][2] += grade
                if m - 1 >= 0 and n + 1 < level  and chesspad[m - 1][n + 1] == 0:
                    shape[i][j][2] += 1
                if m - 1 >= 0 and n + 1 < level  and chesspad[m - 1][n + 1] == -color:
                    shape[i][j][2] -= 2
                m = i
                n = j
                # 如果右上方跟当前传入的颜色参数一致，那么加分到2位！
                while (m + 1 < level  and n - 1 >= 0 and chesspad[m + 1][n - 1] == color):
                    m += 1
                    n -= 1
                    shape[i][j][2] += grade
                if m + 1 < level  and n - 1 >= 0 and chesspad[m + 1][n - 1] == 0:
                    shape[i][j][2] += 1
                if m + 1 < level  and n - 1 >= 0 and chesspad[m + 1][n - 1] == -color:
                    shape[i][j][2] -= 2
                m = i
                n = j
                # 如果左上方跟当前传入的颜色参数一致，那么加分到3位！
                while (m - 1 >= 0 and n - 1 >= 0 and chesspad[m - 1][n - 1] == color):
                    m -= 1
                    n -= 1
                    shape[i][j][3] += grade
                if m - 1 >= 0 and n - 1 >= 0 and chesspad[m - 1][n - 1] == 0:
                    shape[i][j][3] += 1
                if m - 1 >= 0 and n - 1 >= 0 and chesspad[m - 1][n - 1] == -color:
                    shape[i][j][3] -= 2
                m = i
                n = j
                # 如果右下方跟当前传入的颜色参数一致，那么加分到3位！
                while m + 1 < level  and n + 1 < level  and chesspad[m + 1][n + 1] == color:
                    m += 1
                    n += 1
                    shape[i][j][3] += grade
                if m + 1 < level  and n + 1 < level  and chesspad[m + 1][n + 1] == 0:
                    shape[i][j][3] += 1
                if m + 1 < level  and n + 1 < level  and chesspad[m + 1][n + 1] == -color:
                    shape[i][j][3] -= 2
    return shape

def Sort(shape):
    for i in shape:
        for j in i:
            for x in range(5):
                for w in range(3, x - 1, -1):
                    if j[w - 1] < j[w]:
                        temp = j[w]
                        j[w - 1] = j[w]
                        j[w] = temp
    print("This Time Sort Done !")
    return shape

def Evaluate(shape):
    for i in range(level):
        for j in range(level):

            if shape[i][j][0] == 4:
                return i, j, MAX
            shape[i][j][4] = shape[i][j][0]*1000 + shape[i][j][1]*100 + shape[i][j][2]*10 + shape[i][j][3]
    max_x = 0
    max_y = 0
    max = 0
    for i in range(13):
        for j in range(13):
            if max < shape[i][j][4]:
                max = shape[i][j][4]
                max_x = i
                max_y = j
    print("the max is "+ str(max) + " at ( "+ str(max_x)+" , "+str(max_y)+" )")
    return max_x, max_y, max

def BetaGo(ch, m, n, color, times):
    if times < 1000:
        return Autoplay(ch, m, n)
    else:
        shape_P = Scan(ch, -color)
        shape_C = Scan(ch,color)
        shape_P = Sort(shape_P)
        shape_C = Sort(shape_C)
        max_x_P, max_y_P, max_P = Evaluate(shape_P)
        max_x_C, max_y_C, max_C = Evaluate(shape_C)
        if max_P>max_C and max_C<MAX:
            return max_x_P,max_y_P
        else:
            return max_x_C,max_y_C
        
# def unpacket(packet):
#     port, my_port, num, type_message, fin, rongyu, data = packet.decode().split('|')
#     print("来源端口", port, "类型", type(port))
#     print("序列号", num)
#     print("信息类型", type_message)
#     print("结束标识", fin)
#     print("数据", data)
#     return type_message, fin, data #返回值添加一个fin

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

def process_human_2015(cont_data,client_socket,pipei):
    # 接收玩家的用户名并加入等待队列
    # print("已连接到: ",addr)
    #username = client_socket.recv(1024).decode()
    
    username = client_socket.recv(1024).decode()
    wait_queue.put((username, client_socket))
    print("当前队列里: ",wait_queue)
    # 遍历队列并打印每个元素
    # while not wait_queue.empty():
    #     # 获取队列中的下一个元素
    #     item = wait_queue.get()
    #     # 解包元组，获取用户名和socket号
    #     username, socket = item
    #     # 打印用户名和socket号
    #     print(f"Username: {username}, Socket: {socket}")
    #     print("我接受到的玩家: ",wait_queue)
    # 如果等待队列中有两个玩家，则开始游戏
    if wait_queue.qsize() == 2:
        # 从等待队列中取出两个玩家并开始游戏
        player1, socket1 = wait_queue.get()
        player2, socket2 = wait_queue.get()
        # 发送游戏开始的消息给两个玩家
        socket1.sendall(('Game Start! You are player1 (Black).').encode())
        socket2.sendall(('Game Start! You are player2 (White).').encode())
        #黑白棋子初始化
        black_chess,white_chess=[],[]
        wcx,wcy,bcx,bcy=[],[],[],[]
        play_count=2 
        # 等待两个玩家依次下棋
        while True:
            # 玩家1下棋
            position1 = socket1.recv(1024)
            #row1, col1 = map(int, position1.split(','))
            print(position1,type(position1))
                       
            # black_message=position1
            #接收玩家一的消息并向玩家二发送反馈信息
            if position1.decode()=='认输':
                print("玩家一认输")
                text="对方认输"
                socket2.sendall(text.encode())
                break
               
            elif position1.decode()=='我跑了':
                
                if play_count==2:
                    print("走了一个")
                    play_count=play_count-1
                    text="对方认输"
                    socket2.sendall(text.encode())
                    break
                else:
                    break
            else:
                socket2.sendall(position1)
            col1,row1,color1=position1.decode().split(",")
            row1_int=int(row1)
            col1_int=int(col1)
            black_chess.append([col1_int,row1_int])
            bcx.append(black_chess[-1][0])
            bcy.append(black_chess[-1][1])
            print("黑棋序列：",black_chess)

            #玩家一下棋后判断战局情况
            flag_win=gameover(wcx,wcy,bcx,bcy,white_chess,black_chess)
            if flag_win==1:
                print("黑棋赢了")
                socket1.sendall(('你赢了').encode())
                socket2.sendall(('你输了').encode())
                break
            elif flag_win==0:
                print("白棋赢了")
                socket2.sendall(('你赢了').encode())
                socket1.sendall(('你输了').encode())
                break
            else:
                print("游戏继续")
                socket2.sendall(('游戏继续').encode())
                socket1.sendall(('游戏继续').encode())

            # 玩家2下棋
            position2 = socket2.recv(1024)
            
            # white_message=position2

            #接收玩家二的消息并向玩家一发送反馈信息
            if position2.decode()=='认输':
                print("玩家一认输")
                text="对方认输"
                socket1.sendall(text.encode())
                break
            elif position2.decode()=='我跑了':
                
                if play_count==2:
                    print("走了一个")
                    play_count=play_count-1
                    text="对方认输"
                    socket1.sendall(text.encode())
                    break
                else:
                    break
            else:
                socket1.sendall(position2)
            # socket1.sendall(position2)
            col2, row2,color2=position2.decode().split(',')
            row2_int=int(row2)
            col2_int=int(col2)
            white_chess.append([col2_int,row2_int])
            print("白棋序列：",white_chess)
            wcx.append(white_chess[-1][0])
            wcy.append(white_chess[-1][1])

            #玩家二下棋后判断战局情况
            flag_win=gameover(wcx,wcy,bcx,bcy,white_chess,black_chess)
            if flag_win==1:
                print("黑棋赢了")
                socket1.sendall(('你赢了').encode())
                socket2.sendall(('你输了').encode())
                break
                # socket1.close()
                # socket2.close()
            elif flag_win==0:
                print("白棋赢了")
                socket2.sendall(('你赢了').encode())
                socket1.sendall(('你输了').encode())
                break
                # socket1.close()
                # socket2.close()
            else:
                print("游戏继续")
                socket2.sendall(('游戏继续').encode())
                socket1.sendall(('游戏继续').encode())

def process_robot_2013(cont_data,client_socket,pipei):       
    print("C的证书ID: ",pipei)
    key_c_v = get_key_sql(pipei)
    # print("cont_data_2013:",cont_data)
    decry_message_2013 = des.decrypt(cont_data, key_c_v)  # str
    print("解密后的2013(人机模式)报文内容:",decry_message_2013)
    username, sign_2013 = decry_message_2013.split('|')  # str
    #goods_type,username=data_2022.split(',')
    ec=65537
    n_c = get_c_sql(pipei)
    nv,dv=get_myself_sql()
    nv=int(nv)
    dv=int(dv)
    data_sign_2013 = recv_sign(int(sign_2013), ec, int(n_c)).decode()
    # print("data_sign_2013: ",data_sign_2013)
    if '2013'==data_sign_2013:
        print("验签成功")
        wait_queue.put((username,pipei,client_socket))
        # print("我接受到的玩家: ",wait_queue)
        # 如果等待队列中有两个玩家，则开始游戏
        if wait_queue.qsize() == 1:
            # 从等待队列中取出两个玩家并开始游戏
            username, pipei,socket1 = wait_queue.get()
            # 发送游戏开始的消息给两个玩家
            user_rank=get_user_rank(username)
            data_14=username+','+user_rank+','+'0'
            message_2014=get_message_2014(data_14,dv,nv)
            print("加密前的2014(人机模式反馈)报文内容: ",message_2014)
            #message_2016=str(message_2016)
            encry_message_2014=des.encryption(message_2014,key_c_v)
            # print("encry_message_2014",encry_message_2014)
            packet_2014=packet_head(b'65434',b'1111',b'2014',b'0',b'0000',b'000000000',encry_message_2014.encode())
            # print("packet_2014",packet_2014)
            client_socket.sendall(packet_2014)
            # socket1.sendall(('Game Start! You are player1 (Black).').encode())
            board = [[0 for i in range(13)] for j in range(13)]
            #黑白棋子初始化
            black_chess,white_chess=[],[]
            wcx,wcy,bcx,bcy=[],[],[],[] 
            times=0
            # 等待两个玩家依次下棋
            while True:
                # 玩家1下棋
                packet_2019=socket1.recv(1024)
                type_message_2019,pipei_2019,message_2019=unpacket(packet_2019)
                position1=recv_2019(pipei_2019,message_2019)
                # position1 = socket1.recv(1024)
                #row1, col1 = map(int, position1.split(','))
                # print(position1))
                        
                # black_message=position1
                #接收玩家一的消息并向玩家二发送反馈信息
                if position1=='surrender':
                    print("玩家认输")
                    
                    break
                elif position1=='i_run':
                    print("玩家逃跑")
                    break
                col1,row1,color1=position1.split(",")
                row1_int=int(row1)
                col1_int=int(col1)
                #玩家下的位置置为1
                board[row1_int][col1_int]=1
                black_chess.append([col1_int,row1_int])
                bcx.append(black_chess[-1][0])
                bcy.append(black_chess[-1][1])
                # print("黑棋序列：",black_chess)
                flag_win=gameover(wcx,wcy,bcx,bcy,white_chess,black_chess)
                if flag_win==1:
                    print("黑棋赢了")
                    data_19='you_win'
                    packet19=send_packet_2019(data_19,dv,nv,key_c_v,pipei)
                    socket1.sendall(packet19)
                    break
                elif flag_win==0:
                    print("白棋赢了")
                    data_19='you_fail'
                    packet19=send_packet_2019(data_19,dv,nv,key_c_v,pipei)
                    socket1.sendall(packet19)
                    # socket1.sendall(('你输了').encode())
                    break
                else:
                    print("game_continue")
                    data_19='game_continue'
                    packet19=send_packet_2019(data_19,dv,nv,key_c_v,pipei)
                    socket1.sendall(packet19)
                    # socket1.sendall(('游戏继续').encode())
                # 玩家2下棋
                # position2 = socket2.recv(1024)
                color= -1 * 1
                col2,row2=BetaGo(board,col1_int,row1_int,color,times)
                row2_int=int(row2)
                col2_int=int(col2)
                board[row2_int][col2_int]=-1
                times+=1
                print("ai选择的位置是:",col2,row2)
                white_chess.append([col2_int,row2_int])
                # print("白棋序列：",white_chess)
                wcx.append(white_chess[-1][0])
                wcy.append(white_chess[-1][1])
                # ai为白棋
                position2=str(col2)+','+str(row2)+','+ "1"
                 
                #向玩家一发送白棋信息
                # white_message=position2
                packet_position2=send_packet_2019(position2,dv,nv,key_c_v,pipei)
                # print("发送的白棋信息:",packet_position2)
                socket1.sendall(packet_position2)
                socket1.recv(1024)
                flag_win=gameover(wcx,wcy,bcx,bcy,white_chess,black_chess)
                if flag_win==1:
                    print("黑棋赢了")
                    data_19='you_win'
                    packet19=send_packet_2019(data_19,dv,nv,key_c_v,pipei)
                    socket1.sendall(packet19)
                    break
                elif flag_win==0:
                    print("白棋赢了")
                    data_19='you_fail'
                    packet19=send_packet_2019(data_19,dv,nv,key_c_v,pipei)
                    socket1.sendall(packet19)
                    # socket1.sendall(('你输了').encode())
                    break
                else:
                    print("game_continue")
                    data_19='game_continue'
                    packet19=send_packet_2019(data_19,dv,nv,key_c_v,pipei)
                    socket1.sendall(packet19)
                   
                  
        
    else:
        packet_ack_2016=packet_ack(b'65434',b'1111',b'2000',b'0',b'0116',b'216error')
        # b='send'

    # username = client_socket.recv(1024).decode()
   

    
     

def process_shop_2012(cont_data,client_socket,pipei):
    pass


def process_log_2011(message,conn,pipei):
    
    # #此时接收到的是账号和密码
    # username,password=message.split("|")
    # print("username: ",username,"password: ",password)
    # true_password=check_password(username)
    print("C的证书ID: ",pipei)
    key_c_v = get_key_sql(pipei)
    decry_message_2011 = des.decrypt(message, key_c_v)  # str
    print("解密后的2011(登录)报文内容:",decry_message_2011)
    data_2011, sign_2011 = decry_message_2011.split('|')  # str
    ec=65537
    n_c = get_c_sql(pipei)
    nv,dv=get_myself_sql()
    nv=int(nv)
    dv=int(dv)
    # print("2011(登录)报文的数字签名:",sign_2011)
    #返回值是byte
    data_sign_2011 = recv_sign(int(sign_2011), ec, int(n_c)).decode()
    # print("data_2011:",data_2011)
    # print("data_sign_2011:",data_sign_2011)
    if '2011' == data_sign_2011:
        print("验签成功!")
        username,password=data_2011.split(',')
        # flag_ID='0'
        true_password=check_password(username)

        # b='查找数据库，是否有当前ID用户，存在则为1否则为0'
        if true_password==0:
            #账号错误
            print("用户账号验证错误，不存在当前帐号")
            message_2012=get_message_2012(b'00',dv,nv)
            print("加密前的2012(登陆反馈)报文内容: ",message_2012)
            encry_message_2012 = des.encryption(message_2012, key_c_v)
            packet_2012=packet_head(b'65434',b'1111',b'2012',b'0',b'0000',b'00000000',encry_message_2012.encode())
            conn.sendall(packet_2012)
        else:

            # flag_secret='0'
            # b = '查找数据库，是否有当前ID用户密码是否正确，正确则为1否则为0'
            if password==true_password:
                print("用户信息验证正确，准备发送登录反馈")
                message_2012=get_message_2012(b'10',dv,nv)
                print("加密前的2012(登陆反馈)报文内容: ",message_2012)
                encry_message_2012=des.encryption(message_2012,key_c_v)
                packet_2012=packet_head(b'65434',b'1111',b'2012',b'0',b'0000',b'00000000',encry_message_2012.encode())
                conn.sendall(packet_2012)
            else:
                print("登录密码错误！准备发送登录反馈")
                message_2012 = get_message_2012(b'01', dv, nv)
                print("加密前的2012(登陆反馈)报文内容: ",message_2012)
                encry_message_2012 = des.encryption(message_2012, key_c_v)
                packet_2012=packet_head(b'65434',b'1111',b'2012',b'0',b'0000',b'00000000',encry_message_2012.encode())
                conn.sendall(packet_2012)
        
    else:
        packet_ack_2011=packet_ack(b'65434',b'1111',b'2000',b'0',b'0111',b'211error')
        conn.sendall(packet_ack_2011)
    conn.recv(1024)
    # if(true_password==password):
    #     conn.sendall(b'1')
    #     conn.close()
    # else:
    #     conn.sendall(b'0')
    #     conn.close()

def process_card_2017(cont_data,client_socket,pipei):
    print("C的证书ID: ",pipei)
    key_c_v = get_key_sql(pipei)
    decry_message_2017 = des.decrypt(cont_data, key_c_v)  # str
    print("解密后的2017(购买)报文内容:",decry_message_2017)
    data_2017, sign_2017 = decry_message_2017.split('|')  # str
    goods_type,username=data_2017.split(',')
    ec=65537
    n_c = get_c_sql(pipei)
    nv,dv=get_myself_sql()
    nv=int(nv)
    dv=int(dv)
    data_sign_2017 = recv_sign(int(sign_2017), ec, int(n_c)).decode()
    # print("data_sign_2017: ",data_sign_2017)
    if '2017'==data_sign_2017:
        print("验签成功!")
        # goods_type=data_2017
        if goods_type=='00':
            print("请求购买保护卡")
            user_coins=get_coins(username)
            user_coins_int=int(user_coins)
            if user_coins_int>=50:
                user_coins_int=user_coins_int-50
                user_card=get_card(username)
                user_card_int=int(user_card)+1
                save_coins_card(username,str(user_coins_int),str(user_card_int))
                scoring=get_user_rank(username)
                # scoring, coin, card, skin_type='更新后的数据'
                message_2018=get_message_2018(scoring,str(user_coins_int),str(user_card_int),"00",dv,nv)
                message_2018=str(message_2018)
                encry_message_2018=des.encryption(message_2018,key_c_v)
                packet_2018=packet_head(b'65434',b'1111',b'2018',b'0',b'0000',b'000000000',encry_message_2018.encode())
                client_socket.sendall(packet_2018)
                print("packet_2018:",packet_2018)
                print("发送购买保护卡反馈")
            else:
                packet_2018=packet_head(b'65434',b'1111',b'2018',b'1',b'0000',b'000000000',b'error')
                client_socket.sendall(packet_2018)
                print("发送购买保护卡失败反馈")
# get_user_rank()
        elif goods_type=='01':
            user_coins=get_coins(username)
            user_coins_int=int(user_coins)
            user_card=get_card(username)
            scoring=get_user_rank(username)
            print("请求购买玉桂狗皮肤")
            user_yugui=get_yugui(username)
            if user_yugui=='1':
                message_2018=get_message_2018(scoring,user_coins,user_card,"01",dv,nv)
                message_2018=str(message_2018)
                print("加密前的2018(购买玉桂反馈)报文内容: ",message_2018)
                encry_message_2018=des.encryption(message_2018,key_c_v)
                packet_2018 = packet_head(b'65434', b'1111', b'2018', b'0', b'0000', b'000000000', encry_message_2018.encode())
                client_socket.sendall(packet_2018)
                # print("packet_2018:",packet_2018)
                print("发送装备玉桂狗皮肤反馈")
            else:
                if user_coins_int>=200:
                    print("钱够")
                    user_coins_int=user_coins_int-200
                    save_coins_yugui(str(user_coins_int),username)
                    message_2018=get_message_2018(scoring,str(user_coins_int),user_card,"01",dv,nv)
                    message_2018=str(message_2018)
                    print("加密前的2018(购买玉桂反馈)报文内容: ",message_2018)
                    encry_message_2018=des.encryption(message_2018,key_c_v)
                    packet_2018 = packet_head(b'65434', b'1111', b'2018', b'0', b'0000', b'000000000', encry_message_2018.encode())
                    client_socket.sendall(packet_2018)
                    # print("packet_2018:",packet_2018)
                    print("发送购买并装备玉桂狗皮肤反馈")
                else:
                    print("钱不够")
                    packet_2018=packet_head(b'65434',b'1111',b'2018',b'1',b'0000',b'000000000',b'error')
                    client_socket.sendall(packet_2018)
                    print("发送购买玉桂狗失败反馈")

            
        elif goods_type=='10':
            user_coins=get_coins(username)
            user_coins_int=int(user_coins)
            user_card=get_card(username)
            scoring=get_user_rank(username)
            print("请求购买kitty皮肤")
            user_kitty=get_kitty(username)
            if user_kitty=='1':
                message_2018=get_message_2018(scoring,user_coins,user_card,"10",dv,nv)
                message_2018=str(message_2018)
                print("加密前的2018(购买kitty反馈)报文内容: ",message_2018)
                encry_message_2018=des.encryption(message_2018,key_c_v)
                packet_2018 = packet_head(b'65434', b'1111', b'2018', b'0', b'0000', b'000000000', encry_message_2018.encode())
                client_socket.sendall(packet_2018)
                # print("packet_2018:",packet_2018)
                print("发送装备kitty皮肤反馈")
            else:
                if user_coins_int>=200:
                    print("钱够")
                    user_coins_int=user_coins_int-200
                    save_coins_kitty(str(user_coins_int),username)
                    message_2018=get_message_2018(scoring,str(user_coins_int),user_card,"10",dv,nv)
                    message_2018=str(message_2018)
                    print("加密前的2018(购买kitty反馈)报文内容: ",message_2018)
                    encry_message_2018=des.encryption(message_2018,key_c_v)
                    packet_2018 = packet_head(b'65434', b'1111', b'2018', b'0', b'0000', b'000000000', encry_message_2018.encode())
                    client_socket.sendall(packet_2018)
                    # print("packet_2018:",packet_2018)
                    print("发送购买并装备kitty皮肤反馈")
                else:
                    print("钱不够")
                    packet_2018=packet_head(b'65434',b'1111',b'2018',b'1',b'0000',b'000000000',b'error')
                    client_socket.sendall(packet_2018)
                    print("发送购买kitty失败反馈")
        elif goods_type=='11':
            user_coins=get_coins(username)
            user_coins_int=int(user_coins)
            user_card=get_card(username)
            scoring=get_user_rank(username)
            print("请求购买哆啦A梦皮肤")
            user_ameng=get_ameng(username)
            if user_ameng=='1':
                message_2018=get_message_2018(scoring,user_coins,user_card,"11",dv,nv)
                message_2018=str(message_2018)
                print("加密前的2018(购买哆啦A梦反馈)报文内容: ",message_2018)
                encry_message_2018=des.encryption(message_2018,key_c_v)
                packet_2018 = packet_head(b'65434', b'1111', b'2018', b'0', b'0000', b'000000000', encry_message_2018.encode())
                client_socket.sendall(packet_2018)
                # print("packet_2018:",packet_2018)
                print("发送装备哆啦A梦皮肤反馈")
            else:
                if user_coins_int>=200:
                    print("钱够")
                    user_coins_int=user_coins_int-200
                    save_coins_ameng(str(user_coins_int),username)
                    message_2018=get_message_2018(scoring,str(user_coins_int),user_card,"11",dv,nv)
                    message_2018=str(message_2018)
                    print("加密前的2018(购买哆啦A梦反馈)报文内容: ",message_2018)
                    encry_message_2018=des.encryption(message_2018,key_c_v)
                    packet_2018 = packet_head(b'65434', b'1111', b'2018', b'0', b'0000', b'000000000', encry_message_2018.encode())
                    client_socket.sendall(packet_2018)
                    # print("packet_2018:",packet_2018)
                    print("发送购买并装备哆啦A梦皮肤反馈")
                else:
                    print("钱不够")
                    packet_2018=packet_head(b'65434',b'1111',b'2018',b'1',b'0000',b'000000000',b'error')
                    client_socket.sendall(packet_2018)
                    print("发送购买哆啦A梦失败反馈")

    else:
        packet_ack_2017=packet_ack(b'65434',b'1111',b'2000',b'0',b'0117',b'217error')
        # b='send'

def process_rank_2022(cont_data,client_socket,pipei):
    print("C的证书ID: ",pipei)
    key_c_v = get_key_sql(pipei)
    # print("cont_data_2022:",cont_data)
    decry_message_2022 = des.decrypt(cont_data, key_c_v)  # str
    print("解密后的2022(排名)报文内容:",decry_message_2022)
    data_2022, sign_2022 = decry_message_2022.split('|')  # str
    #goods_type,username=data_2022.split(',')
    ec=65537
    n_c = get_c_sql(pipei)
    nv,dv=get_myself_sql()
    nv=int(nv)
    dv=int(dv)
    data_sign_2022 = recv_sign(int(sign_2022), ec, int(n_c)).decode()
    # print("data_sign_2022: ",data_sign_2022)
    if '2022'==data_sign_2022:
        print("验签成功!")
        all_rank=get_rank()
        print("当前排名情况:",all_rank)
        message_2016=get_message_2016(str(all_rank),dv,nv)
        print("加密前的2016(排名反馈)报文内容: ",message_2016)
        #message_2016=str(message_2016)
        encry_message_2016=des.encryption(message_2016,key_c_v)
        packet_2016=packet_head(b'65434',b'1111',b'2016',b'0',b'0000',b'000000000',encry_message_2016.encode())
        client_socket.sendall(packet_2016)


    else:
        packet_ack_2016=packet_ack(b'65434',b'1111',b'2000',b'0',b'0116',b'216error')
        # b='send'


process_dict = {
    "2011": process_log_2011,
    # "2015": process_human_2015,
    '2012': process_shop_2012,
    '2013': process_robot_2013,
    '2017': process_card_2017,
    '2022': process_rank_2022,
}


def check_password(id):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    # 
    # 创建游标对象
    cursor = conn.cursor()
    admin_pass='1'

    # # 执行SQL语句
    # sql = "INSERT INTO mas(as_id, as_e, as_n) VALUES (%s, %s, %s)" % (id,e,n)
    # sql = "UPDATE mas SET as_n='%s' WHERE as_id='%s';" %(n,id)
    #sql = "SELECT vinfo_password FROM mvinfo WHERE vinfo_id ='%s';" %(id)
    sql="SELECT * FROM mvinfo WHERE vinfo_id = '%s'" %id
    try:
        # 执行SQL语句
        cursor.execute(sql)
            # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            admin_id = row[0]
            admin_pass = row[1]
            # 打印结果
            print("admin_id=%s,admin_pass=%s" % (admin_id, admin_pass))
    except:
        print("Error: unable to fecth data")
        return 0
    # result=''
    # cursor.execute(sql)  # 执行sql语句
    # result = cursor.fetchone()[0]

    # results = cursor.fetchall()
    # for row in results:
    #     admin_id = row[0]
    #     admin_pass = row[1]
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
    return admin_pass

class PrintToGUI(object):
    def __init__(self, root):
        self.text = tk.Text(root)
        self.text.pack()

        # 重定向标准输出到Text小部件
        sys.stdout = self
          
    def write(self, message):
        self.text.insert(tk.END, str(message))

 # 定义一个客户端处理线程
def handle_client(conn, addr):
    root = tk.Tk()
    root.title("V_SERVE所接收到的内容")
    app = PrintToGUI(root)
    with conn:
        global IDc
        print('已连接到：', addr)
        packet_all=conn.recv(1024)
        # print("packet_all",packet_all)
        type_message,pipei,data=unpacket(packet_all) #str
        # type_message = conn.recv(1024).decode()
        # conn.sendall(b"i got type")
        # 打印接收到的消息
        # 注册登录信息
        print("收到的消息类型:",type_message)
        #type_message,pipei,cont_data=unpacket(message)
        # print("type_message:",type_message)
        if type_message in process_dict:
            flag=process_dict[type_message](data,conn,pipei)
            # print("test",flag)
        else:
                # 处理其他情况
            print("消息类型可能有错误")
    root.mainloop()
            # if type_message in process_dict:
            #     flag=process_dict[type_message](cont_data)
            #     print("test",flag)

            # else:
            #     # 处理其他情况
            #     print("可能有错误")
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

# 定义一个socket对象
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 绑定服务器IP地址和端口号
    s.bind((HOST_SERVE, PORT_V_SERVE))
    # 开始监听
    s.listen()
    print('V_SERVE服务器已启动,等待连接...')
    wait_queue = queue.Queue()

   
    # 循环等待客户端连接
    while True:
        # 接收客户端连接请求
        conn, addr = s.accept()
        # 创建一个新的线程来处理客户端请求
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start() 






  
   



