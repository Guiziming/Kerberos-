import tkinter as tk
from tkinter.messagebox import showinfo
import socket
import RSA as rsa
import des_for_rsa as des


HOST_V_SERVE='192.168.43.238'
PORT_V_SERVE = 65435

global bg_flag
bg_flag=0
def get_bg_flag():
    global bg_flag
    
    return bg_flag
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

def show_custom_info_fail():
    top = tk.Toplevel()
    top.title("购买")
    top.geometry("200x100")

    # 获取屏幕的宽度和高度
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()

    # 计算窗口左上角坐标的x和y值，以将其放置在屏幕的中心位置
    x = (screen_width - top.winfo_reqwidth()) // 2
    y = (screen_height - top.winfo_reqheight()) // 2
    top.geometry("+{}+{}".format(x, y))

    label = tk.Label(top, text="氪点钱吧!")
    label.pack(pady=10)

    ok_button = tk.Button(top, text="确定", command=top.destroy)
    ok_button.pack()

    # 将窗口放置在最前面
    top.lift()

def show_custom_info():
    top = tk.Toplevel()
    top.title("购买")
    top.geometry("200x100")

    # 获取屏幕的宽度和高度
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()

    # 计算窗口左上角坐标的x和y值，以将其放置在屏幕的中心位置
    x = (screen_width - top.winfo_reqwidth()) // 2
    y = (screen_height - top.winfo_reqheight()) // 2
    top.geometry("+{}+{}".format(x, y))

    label = tk.Label(top, text="购买成功!")
    label.pack(pady=10)

    ok_button = tk.Button(top, text="确定", command=top.destroy)
    ok_button.pack()

    # 将窗口放置在最前面
    top.lift()

# def show_custom_info():
#     top = tk.Toplevel()
#     top.title("购买")
#     top.geometry("200x100")
    
#     label = tk.Label(top, text="购买成功!")
#     label.pack(pady=10)
    
#     ok_button = tk.Button(top, text="确定", command=top.destroy)
#     ok_button.pack()

def center_window(window, width, height):
    # 获取屏幕宽度和高度
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # 计算新窗口左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # 设置窗口位置
    window.geometry(f"{width}x{height}+{x}+{y}")

def shop_menu(des_c_v,n_c,e_c,d_c,e_v,n_v,IDc,username):
    # 创建主窗口
    root = tk.Toplevel()
    root.title("商店")
    center_window(root,630,627)
    # 创建画布
    bg_img = tk.PhotoImage(file='E:\code\mycode\\source\shop_final.png')

    # 创建画布
    canvas = tk.Canvas(root, width=630, height=627)
    canvas.pack()

    canvas.create_image(0, 0, image=bg_img, anchor='nw')

    # # 定义金币数量和保护卡数量的变量
    # coin_count = 100
    # card_count = 5


    # # 创建金币数量和保护卡数量的标签
    # coin_label = tk.Label(root, text="金币数量：{}".format(coin_count))
    # coin_label.place(relx=0.35, rely=0.1, relwidth=0.3, relheight=0.1)
    # card_label = tk.Label(root, text="保护卡数量：{}".format(card_count))
    # card_label.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.1)

    # # 创建保护卡的图片
    # card_image = tk.PhotoImage(file="E:\code\mycode\\source\card_new.png")  
    # card_label = tk.Label(root, image=card_image)
    # card_label.place(relx=0.29, rely=0.33)

    future_image = tk.PhotoImage(file="E:\code\mycode\\source\\future_shop_new.png")  
    future_label = tk.Label(root, image=future_image)
    future_label.place(relx=0.44, rely=0.54)

    bg_yugui_image=tk.PhotoImage(file="E:\code\mycode\\source\shop_yugui_new.png")
    bg_yugui_label = tk.Label(root, image=bg_yugui_image)
    bg_yugui_label.place(relx=0.24, rely=0.31)

    bg_kitty_image=tk.PhotoImage(file="E:\code\mycode\\source\shop_kitty_new.png")
    bg_kitty_label = tk.Label(root, image=bg_kitty_image)
    bg_kitty_label.place(relx=0.44, rely=0.31)

    bg_ameng_image=tk.PhotoImage(file="E:\code\mycode\\source\shop_ameng_new.png")
    bg_ameng_label = tk.Label(root, image=bg_ameng_image)
    bg_ameng_label.place(relx=0.64, rely=0.31)
    # 创建购买按钮的函数
    def get_data_2017(goods_type,d_c,n_c):
        sign_2017 = get_sign(b'2017', d_c, n_c)  # int
        message_2017 = goods_type.decode() + '|' + str(sign_2017)
        return message_2017

    def buy_card():
        #发送购买请求给服务器
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST_V_SERVE, PORT_V_SERVE))
            data17=b'00'+b','+username.encode()
            data_2017 = get_data_2017(data17, d_c, n_c)
            encry_message_2017 = des.encryption(data_2017, des_c_v)  # str
            packet_2017 = packet_head(b'65434', IDc.encode(), b'2017', b'0', b'1004', b'00000000', encry_message_2017.encode())
            client_socket.sendall(packet_2017)
            print("packet_2017: ",packet_2017)
            packet_2018=client_socket.recv(1024)
            print("packet_2018: ",packet_2018)
            type_message_2018,fin_2018,pipei_2018,message_2018=unpacket(packet_2018) #str
            if fin_2018=='1':
                print(message_2018)
                show_custom_info_fail()
            else:
                decry_message_2018 = des.decrypt(message_2018, des_c_v)  # str
                data_2018, sign_2018 = decry_message_2018.split('|')  # str
                data_sign_2018 = recv_sign(int(sign_2018), e_v, n_v)
                if b'2018'==data_sign_2018:
                    new_scoring,new_coin,new_card,new_skin=data_2018.split(',')
                    show_custom_info()
                else:
                    packet_ack_2018 = packet_ack(b'65434', b'1111', b'2000', b'0', b'0118', b'218error')
                    client_socket.sendall(packet_2018)


    def buy_null():
        pass

    def buy_yugui():
        #发送购买请求给服务器
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST_V_SERVE, PORT_V_SERVE))
            data17=b'01'+b','+username.encode()
            data_2017 = get_data_2017(data17, d_c, n_c)
            encry_message_2017 = des.encryption(data_2017, des_c_v)  # str
            packet_2017 = packet_head(b'65434', IDc.encode(), b'2017', b'0', b'1004', b'00000000', encry_message_2017.encode())
            client_socket.sendall(packet_2017)
            print("packet_2017: ",packet_2017)
            packet_2018=client_socket.recv(1024)
            print("packet_2018: ",packet_2018)
            type_message_2018,fin_2018,pipei_2018,message_2018=unpacket(packet_2018) #str
            if fin_2018=='1':
                print(message_2018)
                show_custom_info_fail()
            else:
                decry_message_2018 = des.decrypt(message_2018, des_c_v)  # str
                data_2018, sign_2018 = decry_message_2018.split('|')  # str
                data_sign_2018 = recv_sign(int(sign_2018), e_v, n_v)
                if b'2018'==data_sign_2018:
                    new_scoring,new_coin,new_card,new_skin=data_2018.split(',')
                    show_custom_info()
                    global bg_flag
                    bg_flag=1
                else:
                    packet_ack_2018 = packet_ack(b'65434', b'1111', b'2000', b'0', b'0118', b'218error')
                    client_socket.sendall(packet_2018)

    def buy_kitty():
        #发送购买请求给服务器
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST_V_SERVE, PORT_V_SERVE))
            data17=b'10'+b','+username.encode()
            data_2017 = get_data_2017(data17, d_c, n_c)
            encry_message_2017 = des.encryption(data_2017, des_c_v)  # str
            packet_2017 = packet_head(b'65434', IDc.encode(), b'2017', b'0', b'1004', b'00000000', encry_message_2017.encode())
            client_socket.sendall(packet_2017)
            print("packet_2017: ",packet_2017)
            packet_2018=client_socket.recv(1024)
            print("packet_2018: ",packet_2018)
            type_message_2018,fin_2018,pipei_2018,message_2018=unpacket(packet_2018) #str
            if fin_2018=='1':
                print(message_2018)
                show_custom_info_fail()
            else:
                decry_message_2018 = des.decrypt(message_2018, des_c_v)  # str
                data_2018, sign_2018 = decry_message_2018.split('|')  # str
                data_sign_2018 = recv_sign(int(sign_2018), e_v, n_v)
                if b'2018'==data_sign_2018:
                    new_scoring,new_coin,new_card,new_skin=data_2018.split(',')
                    show_custom_info()
                    global bg_flag
                    bg_flag=2
                else:
                    packet_ack_2018 = packet_ack(b'65434', b'1111', b'2000', b'0', b'0118', b'218error')
                    client_socket.sendall(packet_2018)

    def buy_ameng():
           #发送购买请求给服务器
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST_V_SERVE, PORT_V_SERVE))
            data17=b'11'+b','+username.encode()
            data_2017 = get_data_2017(data17, d_c, n_c)
            encry_message_2017 = des.encryption(data_2017, des_c_v)  # str
            packet_2017 = packet_head(b'65434', IDc.encode(), b'2017', b'0', b'1004', b'00000000', encry_message_2017.encode())
            client_socket.sendall(packet_2017)
            print("packet_2017: ",packet_2017)
            packet_2018=client_socket.recv(1024)
            print("packet_2018: ",packet_2018)
            type_message_2018,fin_2018,pipei_2018,message_2018=unpacket(packet_2018) #str
            if fin_2018=='1':
                print(message_2018)
                show_custom_info_fail()
            else:
                decry_message_2018 = des.decrypt(message_2018, des_c_v)  # str
                data_2018, sign_2018 = decry_message_2018.split('|')  # str
                data_sign_2018 = recv_sign(int(sign_2018), e_v, n_v)
                if b'2018'==data_sign_2018:
                    new_scoring,new_coin,new_card,new_skin=data_2018.split(',')
                    show_custom_info()
                    global bg_flag
                    bg_flag=3
                else:
                    packet_ack_2018 = packet_ack(b'65434', b'1111', b'2000', b'0', b'0118', b'218error')
                    client_socket.sendall(packet_2018)


    # 创建购买按钮
    # buy_card_button = tk.Button(root, text="售价: 50",font=("华文行楷",11), command=buy_card)
    # buy_card_button.place(relx=0.305,rely=0.45)
    buy_future_button = tk.Button(root, text="即将上线",font=("华文行楷",11), command=buy_null)
    buy_future_button.place(relx=0.45,rely=0.68)
    buy_yugui_button = tk.Button(root, text="售价: 200",font=("华文行楷",11),command=buy_yugui)
    buy_yugui_button.place(relx=0.25,rely=0.45)
    buy_kitty_button = tk.Button(root, text="售价: 200",font=("华文行楷",11), command=buy_kitty)
    buy_kitty_button.place(relx=0.45,rely=0.45)
    buy_ameng_button = tk.Button(root, text="售价: 300",font=("华文行楷",11), command=buy_ameng)
    buy_ameng_button.place(relx=0.65,rely=0.45)
    # 启动主循环
    root.mainloop()
