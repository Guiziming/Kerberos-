import tkinter as tk
from tkinter import Button, messagebox
from tkinter.messagebox import showinfo, showwarning, showerror
import time
import socket
import sys
from shop_menu import get_bg_flag
import RSA as rsa
import des_for_rsa as des
# from start_menu import start_menu

# HOST = '127.0.0.1'
HOST = '192.168.43.238'  # 服务端地址
PORT = 5000        # 服务端监听的端口号


flag_color='0'
num = b'12'
# 生成签名
# 传入参数，byte,int,int
# 传出参数，int
def get_sign(data, d, n):
    sign = rsa.rsa_encrypt(data, d, n)
    return sign

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

# 拆包报头
def unpacket(packet):
    port, my_port, num, type_message, fin, pipei, rongyu, data = packet.decode().split("|")
    print("来源端口", port, "类型", type(port))
    print("序列号", num)
    print("信息类型", type_message)
    print("结束标识", fin)
    print("匹配为", pipei)
    print("数据", data)
    return type_message,fin, pipei, data  # 返回值添加一个fin

# 打包报头部分
def packet_head(port, num, type_message, fin, pipei, rongyu, data):
    my_port = port
    server_port = port
    serial_num = num
    type_mes = type_message
    FIN = fin
    pipei_num = pipei
    baoliu = rongyu
    baotou = my_port + b'|' + server_port + b'|' + serial_num + b'|' + type_mes + b'|' + FIN + b'|' + pipei_num + b'|' + baoliu
    a_packet = baotou + b'|' + data
    print(a_packet)
    return a_packet

# 拆签名
# 传入参数，int
# 传出参数，byte
def recv_sign(message, e, n):
    data = rsa.rsa_decrypt(message, e, n)
    return data

def get_data_2014(usrname,d_c,n_c):
    sign_2014 = get_sign(b'2019', d_c, n_c)  # int
    message_2014 = usrname + '|' + str(sign_2014)
    return message_2014



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

   
def play_menu_human(client_socket,flag_color,des_c_v,n_c,e_c,d_c,e_v,n_v,IDc,username):
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
    bg_img1=tk.PhotoImage(file='E:\code\mycode\\source\\yugui_final2.png')
    bg_img2=tk.PhotoImage(file='E:\code\mycode\\source\\kitty_final2.png')
    bg_img3= tk.PhotoImage(file='E:\code\mycode\\source\\ameng_final2.png')
    bg_flag=get_bg_flag()
    print("此时的背景是: ",bg_flag)
    if bg_flag==1:
        bg_img=bg_img1
    elif bg_flag==2:
        bg_img=bg_img2
    elif bg_flag==3:
        bg_img=bg_img3
    # 创建画布
    canvas = tk.Canvas(root, width=1050, height=650)
    canvas.pack()

    # 绘制背景图片
    canvas.create_image(0, 0, image=bg_img, anchor='nw')
     # 创建玩家一、玩家二文本框
    player1_name = tk.Entry(root, font=("Arial", 14), width=10, state='normal')
    player1_name.place(x=800, y=200)
    player1_score = tk.Entry(root, font=("Arial", 14), width=10, state='normal')
    player1_score.place(x=800, y=250)
    player2_name = tk.Entry(root, font=("Arial", 14), width=10, state='normal')
    player2_name.place(x=800, y=430)
    player2_score = tk.Entry(root, font=("Arial", 14), width=10, state='normal')
    player2_score.place(x=800, y=480)

    

    def game_judge(game_result):
        if game_result=='you_win':
            print("你赢了")
            wait_label=tk.Label(root, font=("华文行楷", 20),text="你赢了")
            wait_label.place(relx=0.4,rely=0.4,width=200,height=50)
            client_socket.close()
            # start_menu()
            # my_button = tk.Button(root, text="确认", command=my_function)
            return 0
            # sys.exit()
        elif game_result=='you_fail':
            print("你输了")
            wait_label=tk.Label(root, font=("华文行楷", 20),text="你输了")
            wait_label.place(relx=0.4,rely=0.4,width=200,height=50)
            client_socket.close()
            
            return 0
            # sys.exit()
        else:
            return 1
    # 发棋子信息
    def get_surrender_2019(data,d,n):
        # data = x + ',' + y + ',' + color
        sign_2019 = get_sign(b'2019', d, n)
        message_2019 = data + '|' + str(sign_2019)
        return message_2019
    
    def surrender(d_c,n_c):
        message_fail='surrender'
        data_19=get_surrender_2019(message_fail,d_c,n_c)
        encry_message_2019 = des.encryption(data_19, des_c_v)  # str
        packet_2019 = packet_head(b'65434', IDc.encode(), b'2019', b'0', b'1004', b'00000000', encry_message_2019.encode())
        client_socket.sendall(packet_2019)
        # client_socket.sendall(message_fail.encode())
        game_judge('you_fail')
        # sys.exit()
        # sys.exit()
    

    # 创建认输按钮
    surrender_button = tk.Button(root,text="认输", font=("华文行楷", 15),command=lambda:surrender(d_c,n_c))
    surrender_button.place(x=900,y=590,width=80,height=49.44)

    


    wait_label=tk.Label(root, font=("华文行楷", 20),text="等待对手中........")
    wait_label.place(relx=0.4,rely=0.4,width=200,height=50)

    def on_closing():
        # 在关闭窗口前，先执行需要的操作
        try:
            client_run='i_run'
            data_19=get_surrender_2019(client_run,d_c,n_c)
            encry_message_2019 = des.encryption(data_19, des_c_v)  # str
            packet_2019 = packet_head(b'65434', IDc.encode(), b'2019', b'0', b'1004', b'00000000', encry_message_2019.encode())
            client_socket.sendall(packet_2019)
            # client_socket.sendall(client_run.encode())
            game_judge('you_win')
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
    
   
    data14=username
    print("username原始的:",username)
    data_2014 = get_data_2014(data14, d_c, n_c)
    encry_message_2014 = des.encryption(data_2014, des_c_v)  # str
    packet_2014 = packet_head(b'65434', IDc.encode(), b'2019', b'0', b'1004', b'00000000', encry_message_2014.encode())
    print("我已发送自己的玩家信息给服务器!")
    client_socket.sendall(packet_2014)
    print("packet_2014: ",packet_2014)
    packet_2015=client_socket.recv(1024)
    print("packet_2015: ",packet_2015)
    type_message_2015,fin_2015,pipei_2015,message_2015=unpacket(packet_2015) #str
    decry_message_2015 = des.decrypt(message_2015, des_c_v)  # str
    data_2015, sign_2015 = decry_message_2015.split('|')  # str
    user_color_1='0'
    username_1=''
    user_rank_1=''
    user_color_1=''
    username_2=''
    user_rank_2=''
    data_sign_2015 = recv_sign(int(sign_2015), e_v, n_v)
    if b'2019'==data_sign_2015:
        username_1,user_rank_1,user_color_1,username_2,user_rank_2,user_color_2=data_2015.split(',')
        print("玩家信息和积分：",data_2015)
        print("user_color_1:",user_color_1)
        
        #canvas.update()
    else:
        packet_ack_2014 = packet_ack(b'65434', b'1111', b'2000', b'0', b'0114', b'214error')
        

    # username='2'
    # client_socket.sendall(username.encode())
    print("user_color_1:",user_color_1)
    game_message=user_color_1
    print("我接受到了来自服务器的分配")
    wait_label.destroy()
    print("game_message:",game_message)
    if game_message=='0':
        flag_color='0'
        player1_name.insert(tk.END, username_1)
        player1_score.insert(tk.END,user_rank_1) 
        player2_name.insert(tk.END, username_2)
        player2_score.insert(tk.END,user_rank_2)
        print("我是黑棋")
    else:
        flag_color='1'
        player1_name.insert(tk.END, username_2)
        player1_score.insert(tk.END,user_rank_2) 
        player2_name.insert(tk.END, username_1)
        player2_score.insert(tk.END,user_rank_1)
        print("我是白棋")
    
    # 发棋子信息
    def get_message_2019(x,y,color,d,n):
        data = x + ',' + y + ',' + color
        sign_2019 = get_sign(b'2019', d, n)
        message_2019 = data + '|' + str(sign_2019)
        return message_2019
    
    def recv_message_2019(packet_2019):
        type_message_2014,fin_2014,pipei_2014,cont_data=unpacket(packet_2019)
        print("cont_data_2019:",cont_data)
        decry_message_2019 = des.decrypt(cont_data, des_c_v)  # str
        data_2019, sign_2019 = decry_message_2019.split('|')  # str
        data_sign_2019 = recv_sign(int(sign_2019), e_v, n_v).decode()
        print("data_sign_2019: ",data_sign_2019)
        if '2019'==data_sign_2019:
            return data_2019
        else:
            packet_ack_2016=packet_ack(b'65434',b'1111',b'2000',b'0',b'0116',b'216error')
            return '1'
    
    
    

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
                    data_19=get_message_2019(my_x,my_y,my_color,d_c,n_c)
                    encry_message_2019 = des.encryption(data_19, des_c_v)  # str
                    packet_2019 = packet_head(b'65434', IDc.encode(), b'2019', b'0', b'1004', b'00000000', encry_message_2019.encode())
                    client_socket.sendall(packet_2019)
                    
                    packet_2019_1=client_socket.recv(1024)
                    game_result=recv_message_2019(packet_2019_1)
                    
                    # game_result=client_socket.recv(1024).decode()
                    if game_judge(game_result)==1:
                        chess_exist[col][row]=1
                        packet_2019_2=client_socket.recv(1024)
                        white_message=recv_message_2019(packet_2019_2)

                        if white_message=='enemy_surrender':
                            game_judge('you_win')
                        #     flag_exit=0
                        packet_2019_3=client_socket.recv(1024)
                        game_result2=recv_message_2019(packet_2019_3)
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
                    data_19=get_message_2019(my_wx,my_wy,my_color,d_c,n_c)
                    encry_message_2019 = des.encryption(data_19, des_c_v)  # str
                    packet_2019 = packet_head(b'65434', IDc.encode(), b'2019', b'0', b'1004', b'00000000', encry_message_2019.encode())
                    client_socket.sendall(packet_2019)
                    
                    packet_2019_1=client_socket.recv(1024)
                    game_result=recv_message_2019(packet_2019_1)
                    
                    # game_result=client_socket.recv(1024).decode()
                    if game_judge(game_result)==1:
                        chess_exist[col][row]=1
                        packet_2019_2=client_socket.recv(1024)
                        black_message=recv_message_2019(packet_2019_2)

                        if black_message=='enemy_surrender':
                            game_judge('you_win')
                        #     flag_exit=0
                        packet_2019_3=client_socket.recv(1024)
                        game_result2=recv_message_2019(packet_2019_3)
                        #判断战局
                        game_judge(game_result2)     
                        col1_w, row1_w,color1=black_message.split(',')
                        col1_w_int=int(col1_w)
                        row1_w_int=int(row1_w)
                        print("收到的黑棋信息：",black_message)
                        black_chess.append([col1_w_int,row1_w_int])
                        chess_exist[col1_w_int][row1_w_int]=1
                        draw_black_chess(col1_w_int,row1_w_int)
                        flag_huihe=1
                    
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
        packet_2019_2=client_socket.recv(1024)
        black_message=recv_message_2019(packet_2019_2)

        if black_message=='enemy_surrender':
            game_judge('you_win')
        col1_b,row1_b,color1=black_message.split(',')
        col1_b_int=int(col1_b)
        row1_b_int=int(row1_b)
        print("收到的黑棋信息：",black_message)
        black_chess.append([col1_b_int,row1_b_int])
        draw_black_chess(col1_b_int,row1_b_int)
        # draw_chess(white_chess,black_chess)
        print("我绘制了一个黑棋")            
        packet_2019_3=client_socket.recv(1024)
        game_result2=recv_message_2019(packet_2019_3)
        #判断战局
        game_judge(game_result2)  
        chess_exist[col1_b_int][row1_b_int]=1   
        # black_message=client_socket.recv(1024).decode()
        # if black_message=='对方认输':
        #     game_judge('你赢了')
        # col1_b,row1_b,color1=black_message.split(',')
        # col1_b_int=int(col1_b)
        # row1_b_int=int(row1_b)
        # print("收到的黑棋信息：",black_message)
        # black_chess.append([col1_b_int,row1_b_int])
        # draw_black_chess(col1_b_int,row1_b_int)
        # # draw_chess(white_chess,black_chess)
        # print("我绘制了一个黑棋")
        # game_result1=client_socket.recv(1024).decode()
        # #判断战局
        # game_judge(game_result1)               
        # chess_exist[col1_b_int][row1_b_int]=1
     # 绑定鼠标事件
    canvas.bind('<Button-1>', connect_to_server)
     
   
    # 运行主循环
    root.mainloop()
def human_game(des_c_v,n_c,e_c,d_c,e_v,n_v,IDc,username):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        # type_message='2015'
        # client_socket.sendall(type_message.encode())
        # s_t=client_socket.recv(1024) 
        # print(s_t)
        play_menu_human(client_socket,flag_color,des_c_v,n_c,e_c,d_c,e_v,n_v,IDc,username)   


  
   



