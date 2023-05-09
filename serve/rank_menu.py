import tkinter as tk
from tkinter import scrolledtext

def center_window(window, width, height):
    # 获取屏幕宽度和高度
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # 计算新窗口左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # 设置窗口位置
    window.geometry(f"{width}x{height}+{x}+{y}")

def update_rankings(text):
    # 从数据库请求积分信息
    # 模拟更新排名情况
    rankings = [
        {"account": "user1", "score": 100},
        {"account": "user2", "score": 90},
        {"account": "user3", "score": 80},
        # 其他玩家信息
    ]
    
    # 清空滑动窗口中的文本
    text.delete("1.0", tk.END)
    
    # 更新滑动窗口中的文本
    for ranking in rankings:
        text.insert(tk.END, "账户号：{}，积分：{}\n".format(ranking["account"], ranking["score"]))

def rank_menu():
    root = tk.Toplevel()
    root.title("排行")
    center_window(root,630,627)
    bg_img = tk.PhotoImage(file='E:\\网络安全\\代码\\source\\rank_menu.png')

    # 创建画布
    canvas = tk.Canvas(root, width=630, height=627)
    canvas.pack()

    canvas.create_image(0, 0, image=bg_img, anchor='nw')

    # 创建滑动窗口
    text = scrolledtext.ScrolledText(root, width=24, height=20)
    text.place(relx=0.365,rely=0.25,height=290)

    # 创建更新排名按钮
    update_button = tk.Button(root, text="更新排名",font=('华文行楷',14),command=update_rankings(text))
    update_button.place(relx=0.45,rely=0.89,width=81,height=50)

    root.mainloop()

# rank_menu()