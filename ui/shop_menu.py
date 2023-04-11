import tkinter as tk
from tkinter.messagebox import showinfo

def show_custom_info():
    top = tk.Toplevel()
    top.title("购买")
    top.geometry("200x100")
    
    label = tk.Label(top, text="购买成功!")
    label.pack(pady=10)
    
    ok_button = tk.Button(top, text="确定", command=top.destroy)
    ok_button.pack()

def center_window(window, width, height):
    # 获取屏幕宽度和高度
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # 计算新窗口左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # 设置窗口位置
    window.geometry(f"{width}x{height}+{x}+{y}")

def shop_menu():
    # 创建主窗口
    root = tk.Toplevel()
    root.title("商店")
    center_window(root,400,400)
    # 创建画布
    canvas = tk.Canvas(root, width=400, height=400)
    canvas.pack()

    # 定义金币数量和保护卡数量的变量
    coin_count = 100
    card_count = 5


    # 创建金币数量和保护卡数量的标签
    coin_label = tk.Label(root, text="金币数量：{}".format(coin_count))
    coin_label.place(relx=0.35, rely=0.1, relwidth=0.3, relheight=0.1)
    card_label = tk.Label(root, text="保护卡数量：{}".format(card_count))
    card_label.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.1)

    # 创建保护卡的图片
    card_image = tk.PhotoImage(file="E:\code\mycode\source\card.png")  # 替换为实际的图片文件名
    card_label = tk.Label(root, image=card_image)
    card_label.place(relx=0.31, rely=0.4)

    cost_label = tk.Label(root, text="价格: 50")
    cost_label.place(relx=0.35, rely=0.74, relwidth=0.3, relheight=0.1)
    # 创建购买按钮的函数
    def buy_card():
        #发送购买请求给服务器
        show_custom_info()

    # 创建购买按钮
    buy_button = tk.Button(root, text="购买保护卡", command=buy_card)
    buy_button.place(relx=0.41,rely=0.84)


    # 启动主循环
    root.mainloop()
