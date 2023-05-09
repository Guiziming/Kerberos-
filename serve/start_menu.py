import tkinter as tk
from play_menu_robot import play_menu_robot
from play_menu_human4 import human_game
from shop_menu import shop_menu
from rank_menu import rank_menu

def center_window(window, width, height):
    # 获取屏幕宽度和高度
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # 计算新窗口左上角坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # 设置窗口位置
    window.geometry(f"{width}x{height}+{x}+{y}")

def start_menu():
    # 创建主窗口
    root = tk.Toplevel()
    root.title("主菜单")
    center_window(root,630,627)
    bg_img = tk.PhotoImage(file='E:\网络安全\代码\source\start_menu_final.png')

    # 创建画布
    canvas = tk.Canvas(root, width=630, height=627)
    canvas.pack()

    canvas.create_image(0, 0, image=bg_img, anchor='nw')

    # 创建游戏模式选择按钮
    single_mode_button = tk.Button(root, text="人机模式", font=("华文行楷", 20),command=play_menu_robot)
    single_mode_button.place(relx=0.41, rely=0.25, relwidth=0.22, relheight=0.08)
    double_mode_button = tk.Button(root, text="双人对战", font=("华文行楷", 20),command=human_game)
    double_mode_button.place(relx=0.41, rely=0.37, relwidth=0.22, relheight=0.08)

    # 创建商店按钮
    shop_button = tk.Button(root, text="商店", font=("华文行楷", 20),command=shop_menu)
    shop_button.place(relx=0.41, rely=0.49, relwidth=0.22, relheight=0.08)

    # 创建排名按钮
    rank_button = tk.Button(root, text="排名", font=("华文行楷", 20),command=rank_menu)
    rank_button.place(relx=0.41, rely=0.61, relwidth=0.22, relheight=0.08)

    # 创建退出游戏按钮
    exit_button = tk.Button(root, text="退出游戏", font=("华文行楷", 20), command=root.destroy)
    exit_button.place(relx=0.41, rely=0.73, relwidth=0.22, relheight=0.08)

    # 运行主循环
    root.mainloop()

# start_menu()
