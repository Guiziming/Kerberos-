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
# from start_menu import start_menu

HOST_SERVE = '192.168.43.238'
# HOST = '192.168.43.238'  # 服务端地址
PORT_V_SERVE = 65435        # 服务端监听的端口号
MAX = 1008611

level = 13
grade = 10

BOARD_SIZE=13
AI_PLAYER=2


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
    print(ch)
    available_moves = []
    
    # 遍历周围8个位置
    for i in range(max(0, m-1), min(m+2, len(ch))):
        for j in range(max(0, n-1), min(n+2, len(ch[0]))):
            # 如果该位置为空，则添加到可用坐标列表
            if ch[j][i] == 0:
                available_moves.append((i, j))
    print("此时可用的坐标: ",available_moves)
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
        
def unpacket(packet):
    port, my_port, num, type_message, fin, rongyu, data = packet.decode().split('|')
    print("来源端口", port, "类型", type(port))
    print("序列号", num)
    print("信息类型", type_message)
    print("结束标识", fin)
    print("数据", data)
    return type_message, fin, data #返回值添加一个fin

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

def process_human_2015(cont_data,client_socket):
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

def process_robot_2014(cont_data,client_socket):
    username = client_socket.recv(1024).decode()
    wait_queue.put((username, client_socket))
    print("我接受到的玩家: ",wait_queue)
    # 如果等待队列中有两个玩家，则开始游戏
    if wait_queue.qsize() == 1:
        # 从等待队列中取出两个玩家并开始游戏
        player1, socket1 = wait_queue.get()
        # 发送游戏开始的消息给两个玩家
        socket1.sendall(('Game Start! You are player1 (Black).').encode())
        board = [[0 for i in range(13)] for j in range(13)]
        #黑白棋子初始化
        black_chess,white_chess=[],[]
        wcx,wcy,bcx,bcy=[],[],[],[] 
        times=0
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
                break
               
            elif position1.decode()=='我跑了':
                break
            col1,row1,color1=position1.decode().split(",")
            row1_int=int(row1)
            col1_int=int(col1)
            #玩家下的位置置为1
            board[row1_int][col1_int]=1
            black_chess.append([col1_int,row1_int])
            bcx.append(black_chess[-1][0])
            bcy.append(black_chess[-1][1])
            print("黑棋序列：",black_chess)
            flag_win=gameover(wcx,wcy,bcx,bcy,white_chess,black_chess)
            if flag_win==1:
                print("黑棋赢了")
                socket1.sendall(('你赢了').encode())
                break
            elif flag_win==0:
                print("白棋赢了")
                socket1.sendall(('你输了').encode())
                break
            else:
                print("游戏继续")
                socket1.sendall(('游戏继续').encode())
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
            print("白棋序列：",white_chess)
            wcx.append(white_chess[-1][0])
            wcy.append(white_chess[-1][1])
            # ai为白棋
            position2=str(col2)+','+str(row2)+','+ "1"
            #向玩家一发送白棋信息
            # white_message=position2
            socket1.sendall(position2.encode())    
            flag_win=gameover(wcx,wcy,bcx,bcy,white_chess,black_chess)
            if flag_win==1:
                print("黑棋赢了")
                socket1.sendall(('你赢了').encode())
                break
            elif flag_win==0:
                print("白棋赢了")
                socket1.sendall(('你输了').encode())
                break
            else:
                print("游戏继续")
                socket1.sendall(('游戏继续').encode())    

def process_shop_2012(cont_data,client_socket):
    pass
def process_rank_2013(cont_data,client_socket):
    pass


def process_log_2011(cont_data,conn):
    message = conn.recv(1024)
    # 打印接收到的消息
    print(message)
    #此时接收到的是账号和密码
    username,password=message.decode().split("|")
    print("username: ",username,"password: ",password)
    true_password=check_password(username)
    if(true_password==password):
        conn.sendall(b'1')
        conn.close()
    else:
        conn.sendall(b'0')
        conn.close()

process_dict = {
    "2011": process_log_2011,
    "2014": process_robot_2014,
    # "2015": process_human_2015,
    '2012': process_shop_2012,
    '2013': process_rank_2013,
}


def check_password(id):
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', password='20020502', database='v_clientinfo')
    print("数据库连接成功")
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

 # 定义一个客户端处理线程
def handle_client(conn, addr):
    with conn:
        print('已连接到：', addr)
        type_message = conn.recv(1024).decode()
        conn.sendall(b"i got type")
        # 打印接收到的消息
        # 注册登录信息
        print(type_message)
        #type_message,pipei,cont_data=unpacket(message)
        print("type_message:",type_message)
        if type_message in process_dict:
            flag=process_dict[type_message]("123",conn)
            print("test",flag)
        else:
                # 处理其他情况
            print("消息类型可能有错误")
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
    print('服务器已启动，等待连接...')
    wait_queue = queue.Queue()

   
    # 循环等待客户端连接
    while True:
        # 接收客户端连接请求
        conn, addr = s.accept()
        # 创建一个新的线程来处理客户端请求
        t = threading.Thread(target=handle_client, args=(conn, addr))
        t.start() 


  
   



