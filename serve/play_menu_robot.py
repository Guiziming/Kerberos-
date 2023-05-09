import tkinter as tk
from tkinter import Button, messagebox
import time

def center_window(window, width, height):
    # 获取屏幕宽度和高度
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # 计算新窗口左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # 设置窗口位置
    window.geometry(f"{width}x{height}+{x}+{y}")

'''
def check_win(row, col):
    # 判断横向是否有五个相同的棋子
    if all(board[row][j] == player for j in range(col-4, col+1)):
        return True
    # 判断竖向是否有五个相同的棋子
    if all(board[i][col] == player for i in range(row-4, row+1)):
        return True
    # 判断正斜向是否有五个相同的棋子
    if all(board[i][j] == player for i, j in zip(range(row-4, row+1), range(col-4, col+1))):
        return True
    # 判断反斜向是否有五个相同的棋子
    if all(board[i][j] == player for i, j in zip(range(row-4, row+1), range(col+4, col-1, -1))):
        return True
    return False
'''

def surrender():
    pass

def play_menu_robot():
    # 定义时间限制
    time_limit = 30

    # 创建主窗口
    root = tk.Toplevel()
    root.title("五子棋")
    center_window(root,1050,650)
    # 加载背景图片
    #kitty_best/ameng_new/yugui_new
    bg_img = tk.PhotoImage(file='E:\\网络安全\\代码\\source\\base_final.png')
    img=tk.PhotoImage(file='E:\\网络安全\\代码\\source\\renshu.png')
    # 创建画布
    canvas = tk.Canvas(root, width=1050, height=650)
    canvas.pack()

    # 绘制背景图片
    canvas.create_image(0, 0, image=bg_img, anchor='nw')

    # 绘制棋盘
    for i in range(15):
        for j in range(15):
            canvas.create_rectangle(50 + j * 35, 50 + i * 35, 85 + j * 35, 85 + i * 35, outline='#000000')

    # 绘制网格线
    for i in range(14):
        canvas.create_line(50, 85 + i * 35, 550, 85 + i * 35)
        canvas.create_line(85 + i * 35, 50, 85 + i * 35, 550)

    # 创建玩家一、玩家二文本框
    player1_name = tk.Entry(root, font=("Arial", 14), width=10, state='disabled')
    player1_name.place(x=800, y=200)
    player1_score = tk.Entry(root, font=("Arial", 14), width=10, state='disabled')
    player1_score.place(x=800, y=250)
    player2_name = tk.Entry(root, font=("Arial", 14), width=10, state='disabled')
    player2_name.place(x=800, y=430)
    player2_score = tk.Entry(root, font=("Arial", 14), width=10, state='disabled')
    player2_score.place(x=800, y=480)

    # 创建认输按钮
    surrender_button = tk.Button(root,text="认输", font=("华文行楷", 15), command=surrender)
    surrender_button.place(x=900,y=590,width=80,height=49.44)
    # #倒计时
    # time_label=tk.Label(root,text="时间",font=("Arial", 16))
    # time_label.place(x=650, y=450)
    # time_entry=tk.Entry(root,font=("Arial", 14),width=10,state='disabled')
    # time_entry.place(x=850,y=450)
    
 
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
    # 定义落子函数

    
    # 运行主循环
    root.mainloop()

