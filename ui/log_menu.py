import tkinter as tk
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo, showwarning, showerror

def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "password":
        showinfo(title = "五子棋",
              message = "登陆成功!")
    else:
        showerror(title = "五子棋",
              message = "您的账户/密码有误!")



# 创建主窗口
root = tk.Tk()
root.title("Login")

# 创建画布并设置背景图片
canvas = tk.Canvas(root, height=700, width=474)
canvas.pack()
img = Image.open('E:\code\mycode\source\sign.png')  # 打开图片
photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开

canvas.create_image(0, 0, image=photo, anchor='nw')


# 创建用户名标签和输入框
username_label = tk.Label(root, text="Username:", font=("Arial", 12), bg="#b3cde0")
username_label.place(relx=0.2, rely=0.35, relwidth=0.2, relheight=0.05)
username_entry = tk.Entry(root, font=("Arial", 12))
username_entry.place(relx=0.45, rely=0.35, relwidth=0.35, relheight=0.05)

# 创建密码标签和输入框
password_label = tk.Label(root, text="Password:", font=("Arial", 12), bg="#b3cde0")
password_label.place(relx=0.2, rely=0.45, relwidth=0.2, relheight=0.05)
password_entry = tk.Entry(root, font=("Arial", 12), show="*")
password_entry.place(relx=0.45, rely=0.45, relwidth=0.35, relheight=0.05)

# 创建登录按钮
login_button = tk.Button(root, text="Login", font=("Arial", 12), command=validate_login, bg="#b3cde0")
login_button.place(relx=0.23, rely=0.55, relwidth=0.2, relheight=0.05)

# 创建用于显示结果的标签
result_label = tk.Label(root, text="sign", font=("Arial", 12), bg="#b3cde0")
result_label.place(relx=0.57, rely=0.55, relwidth=0.2, relheight=0.05)

# 运行主循环
root.mainloop()
