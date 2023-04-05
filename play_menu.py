import tkinter as tk
from tkinter import Button, messagebox
import time

def play_menu():
    # 定义时间限制
    time_limit = 30

    # 创建主窗口
    root = tk.Toplevel()
    root.title("五子棋")

    # 加载背景图片
    bg_img = tk.PhotoImage(file='E:\code\mycode\source\play_menu.png')

    # 创建画布
    canvas = tk.Canvas(root, width=850, height=600)
    canvas.pack()

    # 绘制背景图片
    canvas.create_image(0, 0, image=bg_img, anchor='nw')

    # 绘制棋盘
    for i in range(15):
        for j in range(15):
            canvas.create_rectangle(50 + j * 35, 50 + i * 35, 85 + j * 35, 85 + i * 35, outline='#000000', fill='#ffffff')

    # 绘制网格线
    for i in range(14):
        canvas.create_line(50, 85 + i * 35, 550, 85 + i * 35)
        canvas.create_line(85 + i * 35, 50, 85 + i * 35, 550)

    # 创建玩家一、玩家二状态栏
    player1_label = tk.Label(root, text="玩家一", font=("Arial", 16))
    player1_label.place(x=600, y=150)
    player2_label = tk.Label(root, text="玩家二", font=("Arial", 16))
    player2_label.place(x=600, y=250)

    player1_label = tk.Label(root, text="积分", font=("Arial", 16))
    player1_label.place(x=600, y=200)
    player2_label = tk.Label(root, text="积分", font=("Arial", 16))
    player2_label.place(x=600, y=300)

    # 创建玩家一、玩家二文本框
    player1_name = tk.Entry(root, font=("Arial", 14), width=10, state='disabled')
    player1_name.place(x=700, y=150)
    player1_score = tk.Entry(root, font=("Arial", 14), width=10, state='disabled')
    player1_score.place(x=700, y=200)
    player2_name = tk.Entry(root, font=("Arial", 14), width=10, state='disabled')
    player2_name.place(x=700, y=250)
    player2_score = tk.Entry(root, font=("Arial", 14), width=10, state='disabled')
    player2_score.place(x=700, y=300)

    #倒计时
    time_label=tk.Label(root,text="时间",font=("Arial", 16))
    time_label.place(x=650, y=450)
    time_entry=tk.Entry(root,font=("Arial", 14),width=10,state='disabled')
    time_entry.place(x=700,y=450)
    # 定义落子函数
    def on_click(event):
        start_time = time.time()  # 记录开始时间
        x, y = event.x, event.y
        col, row = (x - 50) // 35, (y - 50) // 35
        if 0 <= col < 15 and 0 <= row < 15:
            canvas.create_oval(50 + col * 35, 50 + row * 35, 85 + col * 35, 85 + row * 35, fill='black')
            elapsed_time = time.time() - start_time  # 计算所用时间
            if elapsed_time > time_limit:  # 如果超时
                messagebox.showinfo("提示", "您已超时！")
                # 进行超时处理

    # 绑定鼠标点击事件
    canvas.bind('<Button-1>', on_click)

    # 运行主循环
    root.mainloop()
