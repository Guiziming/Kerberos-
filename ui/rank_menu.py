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
    root = tk.Tk()
    root.title("排行")
    center_window(root,400,450)
    canvas = tk.Canvas(root, width=400, height=450)
    canvas.pack()
    # 创建玩家排名情况文本框
    rankings_label = tk.Label(root, text="玩家积分排名情况", font=("Helvetica", 14))
    rankings_label.place(relx=0.3,rely=0.03)

    # 创建滑动窗口
    text = scrolledtext.ScrolledText(root, width=40, height=10)
    text.place(relx=0.15,rely=0.15,height=300)

    # 创建更新排名按钮
    update_button = tk.Button(root, text="更新排名", command=update_rankings(text))
    update_button.place(relx=0.42,rely=0.9)

    root.mainloop()
