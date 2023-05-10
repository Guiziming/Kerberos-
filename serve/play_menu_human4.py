import tkinter as tk
from tkinter import Button, messagebox
from tkinter.messagebox import showinfo, showwarning, showerror
import time
import socket
import sys
# from start_menu import start_menu

# HOST = '127.0.0.1'
HOST = '192.168.43.238'  # 服务端地址
PORT = 5000        # 服务端监听的端口号


flag_color='0'
num = b'12'
# 打包报头部分
def packet_head(port, num, type_message, fin, rongyu, data):
    my_port = port
    server_port = port
    serial_num = num
    type_mes = type_message
    FIN = fin
    baoliu = rongyu
    baotou = my_port + b'|' + server_port + b'|' + serial_num + b'|' + type_mes + b'|' + FIN + b'|' + baoliu
    a_packet = baotou + b'|' + data
    print(a_packet)
    return a_packet

# 拆包报头
def unpacket(packet):
    port, my_port, num, type_message, fin, rongyu, data = packet.decode().split("|")
    print("来源端口", port, "类型", type(port))
    print("序列号", num)
    print("信息类型", type_message)
    print("结束标识", fin)
    print("数据", data)
    return type_message , fin , data #返回值添加一个fin

# 字符串转换为int，用于处理用户输入的内容
# 传入参数：要转换的字符串
# 返回值：转换后的结果
def change_to_uint(str):
    str1=str.decode()
    # result = int.from_bytes(str, 'big')
    result=int(str1)
    return result


# 转换为字节，一个数对应32位
# 传入参数：要转换的数
# 返回值：转换后的结果
def change_to_bytes(my_uint):
    str1=str(my_uint)
    result=str1.encode()
    return result


def center_window(window, width, height):
    # 获取屏幕宽度和高度
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # 计算新窗口左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # 设置窗口位置
    window.geometry(f"{width}x{height}+{x}+{y}")


# def get_data():
#     count_data = data.count
#     return data,count_data

   
def play_menu_human(client_socket,flag_color):
    # 定义时间限制
    time_limit = 30
    
    flag_huihe=0
    

    # 创建主窗口
    root = tk.Toplevel()
    root.title("五子棋")

    

    center_window(root,1050,650)
    # 加载背景图片
    #kitty_besteng_new/yugui_new
    img_board=tk.PhotoImage(file='E:\code\mycode\\source\\chess_board_new.png')
    img_bchess=tk.PhotoImage(file='E:\code\mycode\\source\\heiqi_new.png')
    img_wchess=tk.PhotoImage(file='E:\code\mycode\\source\\baiqi_new.png')
    bg_img = tk.PhotoImage(file='E:\code\mycode\\source\\base_final3.png') #base_final3,ameng_final2,yugui_final2,kitty_final2
    # 创建画布
    canvas = tk.Canvas(root, width=1050, height=650)
    canvas.pack()

    # 绘制背景图片
    canvas.create_image(0, 0, image=bg_img, anchor='nw')
     # 创建玩家一、玩家二文本框
    player1_name = tk.Entry(root, font=("Arial", 14), width=10, state='disabled')
    player1_name.place(x=800, y=200)
    player1_score = tk.Entry(root, font=("Arial", 14), width=10, state='disabled')
    player1_score.place(x=800, y=250)
    player2_name = tk.Entry(root, font=("Arial", 14), width=10, state='disabled')
    player2_name.place(x=800, y=430)
    player2_score = tk.Entry(root, font=("Arial", 14), width=10, state='disabled')
    player2_score.place(x=800, y=480)

    

    def game_judge(game_result):
        if game_result=='你赢了':
            print("你赢了")
            wait_label=tk.Label(root, font=("华文行楷", 20),text="你赢了")
            wait_label.place(relx=0.4,rely=0.4,width=200,height=50)
            client_socket.close()
            # start_menu()
            # my_button = tk.Button(root, text="确认", command=my_function)
            return 0
            # sys.exit()
        elif game_result=='你输了':
            print("你输了")
            wait_label=tk.Label(root, font=("华文行楷", 20),text="你输了")
            wait_label.place(relx=0.4,rely=0.4,width=200,height=50)
            client_socket.close()
            
            return 0
            # sys.exit()
        else:
            return 1
        
    def surrender():
        message_fail='认输'
        client_socket.sendall(message_fail.encode())
        game_judge('你输了')
        # sys.exit()
    

    # 创建认输按钮
    surrender_button = tk.Button(root,text="认输", font=("华文行楷", 15), command=surrender)
    surrender_button.place(x=900,y=590,width=80,height=49.44)

    


    wait_label=tk.Label(root, font=("华文行楷", 20),text="等待对手中........")
    wait_label.place(relx=0.4,rely=0.4,width=200,height=50)

    def on_closing():
        # 在关闭窗口前，先执行需要的操作
        try:
            client_run='我跑了'
            client_socket.sendall(client_run.encode())
            game_judge('你赢了')
        except socket.error:
            print("Socket is closed")
        # result = client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        # if result==0:  
        # sys.exit()
        root.destroy()
        # start_menu()
        

    # 在窗口关闭按钮事件上重写自定义函数
    root.protocol("WM_DELETE_WINDOW", on_closing)
    # global data

    #棋盘定义 13x13棋盘
    chess_board=[[]]
    def set_chess_board():
        x,y=0,0
        while True:
            if x==520:
                x=0
                y+=40
                if y<520:
                    chess_board.append([])
            if y==520:   
                break
            chess_board[-1].append([x,y])
            x+=40
    set_chess_board()
    chess_exist=[[0 for i in range(13)]for j in range(13)]
    #黑白棋子初始化
    black_chess,white_chess=[],[]
    #棋子类型
    chess_kind=1    #1为黑棋，0为白棋
    wcx,wcy,bcx,bcy=[],[],[],[]   #white_chess_x

    def draw_board():
        #横坐标
        for i in chess_board:
            for j in i:
                # 使用Tkinter来更新界面
                canvas.create_image(j[0]+73, j[1]+69, image=img_board)
                canvas.update()
    draw_board()
    def draw_black_chess(col,row):
        canvas.create_image((col+1) * 40+13, (row+1) * 40+9, image=img_bchess, anchor='nw')
        canvas.update()

    def draw_white_chess(col,row):
        canvas.create_image((col+1) * 40+13, (row+1) * 40+9, image=img_wchess, anchor='nw')
        canvas.update()

    # def draw_chess(white_chess,black_chess):
    #         # 绘制白色棋子
    #     for i in white_chess:
    #         canvas.create_image(i[0] * 40+13, i[1] * 40+9, image=img_wchess, anchor='nw')
    #     # 绘制黑色棋子
    #     for i in black_chess:
    #         canvas.create_image(i[0] * 40+13, i[1] * 40+9, image=img_bchess, anchor='nw')
    
   
    username='2011'
    client_socket.sendall(username.encode())
    print("我已发送自己的玩家信息给服务器!")
    game_message=client_socket.recv(1024)
    print("我接受到了来自服务器的分配")
    wait_label.destroy()
    print("game_message:",game_message)
    if game_message.decode()=='Game Start! You are player1 (Black).':
        flag_color='0'
        print("我是黑棋")
    else:
        flag_color='1'
        print("我是白棋")
    
    
    

    def connect_to_server(event):
        # global flag_color
        x, y = event.x, event.y
        # draw_chess(white_chess,black_chess)
        print("black_chess",black_chess)
        print("white_chess",white_chess)
        print(type(x))
        col, row = ((x-10) // 40)-1, ((y-10)// 40)-1
        if 0 <= col < 14 and 0 <= row < 14:
            if chess_exist[col][row]==0:
                #默认为黑棋
                if flag_color=='0':
                    black_chess.append([col,row])
                    #print(col,row)
                    print(black_chess)
                    draw_black_chess(col,row)
                    # draw_chess(white_chess,black_chess)
                    bcx.append(black_chess[-1][0])
                    bcy.append(black_chess[-1][1])
                    my_x=str(col)
                    print(my_x)
                    my_y=str(row)
                    my_color=flag_color
                    data=my_x+','+my_y+','+my_color
                    # message=packet_head(b'5000',num,b'2019',b'1',b'2',data)
                    client_socket.sendall(data.encode())
                    game_result=client_socket.recv(1024).decode()
                    if game_judge(game_result)==1:
                        chess_exist[col][row]=1
                        white_message=client_socket.recv(1024).decode()
                        if white_message=='对方认输':
                            game_judge('你赢了')
                            flag_exit=0
                        game_result2=client_socket.recv(1024).decode()
                        #判断战局
                        game_judge(game_result2)     
                        col1_w, row1_w,color1=white_message.split(',')
                        col1_w_int=int(col1_w)
                        row1_w_int=int(row1_w)
                        print("收到的白棋信息：",white_message)
                        white_chess.append([col1_w_int,row1_w_int])
                        chess_exist[col1_w_int][row1_w_int]=1
                        draw_white_chess(col1_w_int,row1_w_int)
                        flag_huihe=1
                    
                    canvas.update()
                    #白棋
                else:      
                    white_chess.append([col,row])
                    print("white_chess",white_chess)
                    draw_white_chess(col,row)
                    # draw_chess(white_chess,black_chess)
                    wcx.append(white_chess[-1][0])
                    wcy.append(white_chess[-1][1])
                    my_wx=str(col)
                    print(my_wx)
                    my_wy=str(row)
                    my_color=flag_color
                    data2=my_wx+','+my_wy+','+my_color
                    # message2=packet_head(b'5000',num,b'2019',b'1',b'2',data2)
                    client_socket.sendall(data2.encode())
                    game_result=client_socket.recv(1024).decode()
                    if game_judge(game_result)==1:
                    #client_socket.sendall(f'{white_chess}\n'.encode('utf-8'))
                        chess_exist[col][row]=1
                        black_message=client_socket.recv(1024).decode()
                        if black_message=='对方认输':
                            game_judge('你赢了')
                        game_result2=client_socket.recv(1024).decode()
                        #判断战局
                        game_judge(game_result2)
                        col1_b,row1_b,color1=black_message.split(',')
                        col1_b_int=int(col1_b)
                        row1_b_int=int(row1_b)
                        print("收到的黑棋信息：",black_message)
                        black_chess.append([col1_b_int,row1_b_int])
                        draw_black_chess(col1_b_int,row1_b_int)
                        flag_huihe=1
                        # draw_chess(white_chess,black_chess)
                        print("我绘制了一个黑棋")
                        chess_exist[col1_b_int][row1_b_int]=1
                    
                    # draw_chess(white_chess,black_chess)
                    # if client_socket.recv(1024).decode()=='你赢了':
                    #     print(white_message)
                    # elif client_socket.recv(1024).decode()=='你赢了':
                    #     print(white_message) 
                    canvas.update()
            else:
                print("下棋错误")
                # canvas.bind('<Button-1>', connect_to_server)
        # draw_chess(white_chess,black_chess)
        return 1
    print("flag_coler为:",flag_color)
    if flag_color=='1':
        black_message=client_socket.recv(1024).decode()
        if black_message=='对方认输':
            game_judge('你赢了')
        col1_b,row1_b,color1=black_message.split(',')
        col1_b_int=int(col1_b)
        row1_b_int=int(row1_b)
        print("收到的黑棋信息：",black_message)
        black_chess.append([col1_b_int,row1_b_int])
        draw_black_chess(col1_b_int,row1_b_int)
        # draw_chess(white_chess,black_chess)
        print("我绘制了一个黑棋")
        game_result1=client_socket.recv(1024).decode()
        #判断战局
        game_judge(game_result1)               
        chess_exist[col1_b_int][row1_b_int]=1
     # 绑定鼠标事件
    canvas.bind('<Button-1>', connect_to_server)
     
   
    # 运行主循环
    root.mainloop()
def human_game():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        # type_message='2015'
        # client_socket.sendall(type_message.encode())
        # s_t=client_socket.recv(1024) 
        # print(s_t)
        play_menu_human(client_socket,flag_color)   


  
   



