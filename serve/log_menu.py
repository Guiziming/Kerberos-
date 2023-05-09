import tkinter as tk
from PIL import Image, ImageTk
from PIL import ImageFile
from tkinter.messagebox import showinfo, showwarning, showerror
from start_menu import start_menu
import socket
import os
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

HOST='192.168.43.238'
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

def validate_login():
    global username_entry,username_entry
    username = username_entry.get()
    password = password_entry.get()

    if username == "1" and password == "1":
        showinfo(title = "五子棋",
              message = "登陆成功!")
        start_menu()
    else:
        showerror(title = "五子棋",
              message = "您的账户/密码有误!")


def log_menu():
    global username_entry,password_entry
    # 创建主窗口
    root = tk.Tk()
    root.title("Login")

    # 创建画布并设置背景图片
    canvas = tk.Canvas(root, height=630, width=627)
    canvas.pack()
    center_window(root,630,627)
    img = Image.open('E:\网络安全\代码\source\sign_menu_new.png')  # 打开图片
    photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开

    canvas.create_image(0, 0, image=photo, anchor='nw')


    # 创建用户名标签和输入框
    username_entry = tk.Entry(root, font=("Arial", 12))
    username_entry.place(relx=0.37, rely=0.35, relwidth=0.35, relheight=0.05)


    # 创建密码标签和输入框
    password_entry = tk.Entry(root, font=("Arial", 12), show="*")
    password_entry.place(relx=0.37, rely=0.45, relwidth=0.35, relheight=0.05)

    # 创建登录按钮
    login_button = tk.Button(root, text="登录", font=("华文行楷", 15), command=validate_login)
    login_button.place(relx=0.38, rely=0.55, relwidth=0.081, relheight=0.05)

    # 创建用于显示结果的标签
    result_label = tk.Button(root, text="注册", font=("华文行楷", 15), command=validate_login)
    result_label.place(relx=0.6, rely=0.55, relwidth=0.081, relheight=0.05)

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((HOST, PORT_V_SERVE))
        


    # 运行主循环
    root.mainloop()

os.system('python E:\网络安全\代码\\test\C.py')
print("运行了Kerberos的C文件")

log_menu()