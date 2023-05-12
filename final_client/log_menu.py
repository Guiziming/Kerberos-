import tkinter as tk
from PIL import Image, ImageTk
from PIL import ImageFile
from tkinter.messagebox import showinfo, showwarning, showerror
from start_menu import start_menu
import socket
import os
import time
from C import get_key_cv
import des_for_rsa as des
import RSA as rsa
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

HOST_V_SERVE='192.168.43.238'
PORT_V_SERVE = 65435
def center_window(window, width, height):
    # 获取屏幕宽度和高度
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # 计算新窗口左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # 设置窗口位置
    window.geometry(f"{width}x{height}+{x}+{y}")

# 拆包报头
def unpacket(packet):
    port, my_port, num, type_message, fin, pipei, rongyu, data = packet.decode().split("|")
    print("来源端口", port, "类型", type(port))
    print("序列号", num)
    print("信息类型", type_message)
    print("结束标识", fin)
    print("匹配为", pipei)
    print("数据", data)
    return type_message, pipei, data  # 返回值添加一个fin

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
    data = rsa.rsa_decrypt(message, e, n)
    return data

# 传入参数str
def get_data_2011(ID,secret):
    data_2011=ID+','+secret
    return data_2011

# packet=b''
# pipei=unpacket_ack(packet)
def recv_ack(pipei):
    if pipei == '0109':
        print("签名失效，注册失败")
    elif pipei =='0111':
        print("签名失效，登录失败")
    elif pipei =='0117':
        print("签名失效，购买失败")
    elif pipei=='0119':
        print("签名失效，坐标更新失败")
    elif pipei=='0121':
        print("签名失效，保护卡使用失败")

def validate_login(key_c_v,nc,ec,dc,ev,nv,IDc):
    global username_entry,username_entry
    username = username_entry.get()
    password = password_entry.get()

    #创建和服务端的通信
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST_V_SERVE, PORT_V_SERVE))
        ID=username
        # secret=password
        data_2011=get_data_2011(ID,password)
        print("C使用的私钥：dc,nc",dc,nc)
        sign_2011 = get_sign(b'2011', dc, nc)  # int 类型
        print("sign_2011",sign_2011)
        message_2011 = data_2011 + '|' + str(sign_2011)  # str
        encry_message_2011 = des.encryption(message_2011, key_c_v)  # str
        packet_2011=packet_head(b'65434', b'1111', b'2011', b'0', IDc.encode(), b'00000000', encry_message_2011.encode())
        client_socket.sendall(packet_2011)
        print("我发送了消息类型")
        packet_2012=client_socket.recv(1024)
        print("收到的packet_2012",packet_2012)
        #接收到服务端发送过来的登录信息
        type_message_2012,pipei_2012,message_2012=unpacket(packet_2012) #str
        # check_message=check_message.decode()
        print('使用的cv密钥：',key_c_v) 
        decry_message_2012 = des.decrypt(message_2012, key_c_v)  # str
        data_2012, sign_2012 = decry_message_2012.split('|')  # str
        print("sign_2012",sign_2012)
        print('使用的v公钥：',ev,nv) 
        # ev,nv = 'int'
        data_sign_2012 = recv_sign(int(sign_2012), ev, nv)
        print("data_sign_2012",data_sign_2012)
        if b'2012'==data_sign_2012:
            print("接收到的登陆情况:",data_2012)
            if data_2012 == '10':
                print("登录成功")
                showinfo(title = "五子棋",message = "登陆成功!")
                client_socket.sendall(b'success')
                client_socket.close()
                print("登录的username:",username)
                start_menu(des_c_v,n_c,e_c,d_c,ev,nv,IDc,username)
            elif data_2012 == '01':
                print("密码错误，请重新登录")
                client_socket.sendall(b'fail')
                showerror(title = "五子棋",message = "您的密码有误!")
            else:
                print("无当前用户，请先联系管理员")
                client_socket.sendall(b'fail')
                showerror(title = "五子棋",message = "无当前用户，请先联系管理员")
        else:
            print("验签错误")
            packet_ack_2012 = packet_ack(b'65434', b'1111', b'2000', b'0', b'0112', b'212error')
            client_socket.sendall(packet_ack_2012)
    # if check_message=='1':
    #     showinfo(title = "五子棋",
    #           message = "登陆成功!")
    #     client_socket.close()
    #     start_menu()
    # else:
    #     showerror(title = "五子棋",
    #           message = "您的账户/密码有误!")

    # if username == "1" and password == "1":
    #     showinfo(title = "五子棋",
    #           message = "登陆成功!")
    #     start_menu()
    # else:
    #     showerror(title = "五子棋",
    #           message = "您的账户/密码有误!")


def log_menu(des_c_v,n_c,e_c,d_c,e_v,n_v,IDc):
    global username_entry,password_entry
    # 创建主窗口
    root = tk.Tk()
    root.title("Login")

    # 创建画布并设置背景图片
    canvas = tk.Canvas(root, height=630, width=627)
    canvas.pack()
    center_window(root,630,627)
    img = Image.open('E:\code\mycode\\source\sign_menu_new.png')  # 打开图片
    photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开

    canvas.create_image(0, 0, image=photo, anchor='nw')


    # 创建用户名标签和输入框
    username_entry = tk.Entry(root, font=("Arial", 12))
    username_entry.place(relx=0.37, rely=0.35, relwidth=0.35, relheight=0.05)


    # 创建密码标签和输入框
    password_entry = tk.Entry(root, font=("Arial", 12), show="*")
    password_entry.place(relx=0.37, rely=0.45, relwidth=0.35, relheight=0.05)

    # 创建登录按钮
    login_button = tk.Button(root, text="登录", font=("华文行楷", 15), command=lambda:validate_login(des_c_v,n_c,e_c,d_c,e_v,n_v,IDc))
    login_button.place(relx=0.47, rely=0.55, relwidth=0.081, relheight=0.05)

    # # 创建用于显示结果的标签
    # result_label = tk.Button(root, text="注册", font=("华文行楷", 15), command=lambda:validate_login(des_c_v,n_c,e_c,d_c,e_v,n_v,IDc))
    # result_label.place(relx=0.6, rely=0.55, relwidth=0.081, relheight=0.05)

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((HOST, PORT_V_SERVE))
        


    # 运行主循环
    root.mainloop()

# os.system('python E:\网络安全\代码\\test\C.py')
# time.sleep(1)
# print("运行了Kerberos的C文件")

des_c_v,n_c,e_c,d_c,e_v,n_v,IDc=get_key_cv()
print("我和服务器使用的DES KEY为: ",des_c_v,n_c,e_c,d_c,e_v,n_v,IDc)

log_menu(des_c_v,n_c,e_c,d_c,e_v,n_v,IDc)