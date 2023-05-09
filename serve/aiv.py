import socket
import threading
import queue
from collections import Counter
import time
from enum import IntEnum
import pygame
import sys
from random import randint

HOST = '127.0.0.1'  # 服务端地址
PORT = 5001       # 服务端监听的端口号
MAX = 1008611

level = 13
grade = 10

BOARD_SIZE=13
AI_PLAYER=2


def Autoplay(ch, m, n):
    a1 = [1,-1,1,-1,1,-1,0,0]
    b1 = [1,-1,-1,1,0,0,1,-1]
    rand = randint(0,7)
    while m+a1[rand]>=0 and m+a1[rand]<level and n+b1[rand]>=0 and n+b1[rand]<level and ch[m+a1[rand]][n+b1[rand]]!=0 :
        rand = randint(0,7)
    if(ch[m+ a1[rand]][n+b1[rand]]==0):
        return m + a1[rand], n+b1[rand]
    else:
        Autoplay(ch,m,n)

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
    print(ch)
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

def genmove(self, board, turn):
        moves = []
        for y in range(self.len):
            for x in range(self.len):
                if board[y][x] == 0:
                    score = self.position_isgreat[y][x]
                    moves.append((score, x, y))
        moves.sort(reverse=True)
        return moves

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

def handle_client_request(client_socket,addr):
    # 接收玩家的用户名并加入等待队列
    print("已连接到: ",addr)
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
            flag_win=gameover(wcx,wcy,bcx,bcy,white_chess,black_chess)
            if flag_win==1:
                print("黑棋赢了")
                # socket1.sendall(('你赢了').encode())
                # socket2.sendall(('你输了').encode())
            elif flag_win==0:
                print("白棋赢了")
            # 玩家下棋
            position1 = socket1.recv(1024)
            #row1, col1 = map(int, position1.split(','))
            print("玩家下的位置：",position1,type(position1))
             #向玩家二发送黑棋信息           
            # black_message=position1
            # socket2.sendall(position1)
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
                # socket1.sendall(('你赢了').encode())
                # socket2.sendall(('你输了').encode())
            elif flag_win==0:
                print("白棋赢了")
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
