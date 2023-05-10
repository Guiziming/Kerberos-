import socket
import threading
import queue
from collections import Counter
# HOST = '127.0.0.1'
HOST = '192.168.43.238'  # 服务端地址
PORT = 5000        # 服务端监听的端口号

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

def handle_client_request(client_socket,addr):
    # 接收玩家的用户名并加入等待队列
    print("已连接到: ",addr)
    username = client_socket.recv(1024).decode()
    wait_queue.put((username, client_socket))
    print("我接受到的玩家: ",wait_queue)
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
