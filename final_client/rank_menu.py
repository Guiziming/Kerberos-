import tkinter as tk
from tkinter import scrolledtext
import socket
import RSA as rsa
import des_for_rsa as des

HOST_V_SERVE='192.168.43.238'
PORT_V_SERVE = 65435

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

def get_data_2022(goods_type,d_c,n_c):
    sign_2022 = get_sign(b'2022', d_c, n_c)  # int
    message_2022 = goods_type.decode() + '|' + str(sign_2022)
    return message_2022

def center_window(window, width, height):
    # 获取屏幕宽度和高度
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # 计算新窗口左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # 设置窗口位置
    window.geometry(f"{width}x{height}+{x}+{y}")

def update_rankings(text,des_c_v,n_c,e_c,d_c,e_v,n_v,IDc,username):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST_V_SERVE, PORT_V_SERVE))
        data22=b'0000'
        data_2022 = get_data_2022(data22, d_c, n_c)
        encry_message_2022 = des.encryption(data_2022, des_c_v)  # str
        packet_2022 = packet_head(b'65434', IDc.encode(), b'2022', b'0', b'1004', b'00000000', encry_message_2022.encode())
        client_socket.sendall(packet_2022)
        print("packet_2022: ",packet_2022)
        packet_2016=client_socket.recv(1024)
        print("packet_2016: ",packet_2016)
        type_message_2016,fin_2016,pipei_2016,message_2016=unpacket(packet_2016) #str
        decry_message_2016 = des.decrypt(message_2016, des_c_v)  # str
        data_2016, sign_2016= decry_message_2016.split('|')  # str
        data_sign_2016 = recv_sign(int(sign_2016), e_v, n_v)
        if b'2016'==data_sign_2016:
            for item in eval(data_2016):
                text.insert(tk.END, "账户号：{}，积分：{}\n".format(item[0], item[1]))
                # c.execute("INSERT INTO users (username, score) VALUES (?, ?)", (item[0], item[1]))
        else:
            packet_ack_2018 = packet_ack(b'65434', b'1111', b'2000', b'0', b'0118', b'218error')
            client_socket.sendall(packet_2016)
    # # 从数据库请求积分信息
    # # 模拟更新排名情况
    # rankings = [
    #     {"account": "user1", "score": 100},
    #     {"account": "user2", "score": 90},
    #     {"account": "user3", "score": 80},
    #     # 其他玩家信息
    # ]
    
    
    # # 更新滑动窗口中的文本
    # for ranking in rankings:
    #     text.insert(tk.END, "账户号：{}，积分：{}\n".format(ranking["account"], ranking["score"]))

def rank_menu(des_c_v,n_c,e_c,d_c,e_v,n_v,IDc,username):
    root = tk.Toplevel()
    root.title("排行")
    center_window(root,630,627)
    bg_img = tk.PhotoImage(file='E:\code\mycode\\source\\rank_menu.png')

    # 创建画布
    canvas = tk.Canvas(root, width=630, height=627)
    canvas.pack()

    canvas.create_image(0, 0, image=bg_img, anchor='nw')

    # 创建滑动窗口
    text = scrolledtext.ScrolledText(root, width=24, height=20)
    text.place(relx=0.365,rely=0.25,height=290)

    # 创建更新排名按钮
    update_button = tk.Button(root, text="更新排名",font=('华文行楷',14),command=lambda:update_rankings(text,des_c_v,n_c,e_c,d_c,e_v,n_v,IDc,username))
    update_button.place(relx=0.45,rely=0.89,width=81,height=50)

    root.mainloop()

# rank_menu()