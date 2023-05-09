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
    center_window(root,630,627)
    # 创建画布
    bg_img = tk.PhotoImage(file='E:\网络安全\代码\source\shop_final.png')

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

    # 创建保护卡的图片
    card_image = tk.PhotoImage(file="E:\网络安全\代码\source\card_new.png")  
    card_label = tk.Label(root, image=card_image)
    card_label.place(relx=0.29, rely=0.33)

    future_image = tk.PhotoImage(file="E:\\网络安全\\代码\\source\\future_shop_new.png")  
    future_label = tk.Label(root, image=future_image)
    future_label.place(relx=0.59, rely=0.33)

    bg_yugui_image=tk.PhotoImage(file="E:\网络安全\代码\source\shop_yugui_new.png")
    bg_yugui_label = tk.Label(root, image=bg_yugui_image)
    bg_yugui_label.place(relx=0.24, rely=0.56)

    bg_kitty_image=tk.PhotoImage(file="E:\网络安全\代码\source\shop_kitty_new.png")
    bg_kitty_label = tk.Label(root, image=bg_kitty_image)
    bg_kitty_label.place(relx=0.44, rely=0.56)

    bg_ameng_image=tk.PhotoImage(file="E:\网络安全\代码\source\shop_ameng_new.png")
    bg_ameng_label = tk.Label(root, image=bg_ameng_image)
    bg_ameng_label.place(relx=0.64, rely=0.56)
    # 创建购买按钮的函数
    def buy_card():
        #发送购买请求给服务器
        show_custom_info()

    # 创建购买按钮
    buy_card_button = tk.Button(root, text="售价: 50",font=("华文行楷",11), command=buy_card)
    buy_card_button.place(relx=0.305,rely=0.45)
    buy_future_button = tk.Button(root, text="即将上线",font=("华文行楷",11), command=buy_card)
    buy_future_button.place(relx=0.6,rely=0.45)
    buy_yugui_button = tk.Button(root, text="售价: 200",font=("华文行楷",11),command=buy_card)
    buy_yugui_button.place(relx=0.25,rely=0.68)
    buy_kitty_button = tk.Button(root, text="售价: 200",font=("华文行楷",11), command=buy_card)
    buy_kitty_button.place(relx=0.45,rely=0.68)
    buy_ameng_button = tk.Button(root, text="售价: 300",font=("华文行楷",11), command=buy_card)
    buy_ameng_button.place(relx=0.65,rely=0.68)
    # 启动主循环
    root.mainloop()
