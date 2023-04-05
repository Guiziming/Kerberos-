import tkinter as tk
from play_menu import play_menu
# 创建主窗口
root = tk.Tk()
root.title("五子棋")

bg_img = tk.PhotoImage(file='E:\code\mycode\source\main_menu.png')

# 创建画布
canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()

canvas.create_image(0, 0, image=bg_img, anchor='nw')

# 创建游戏模式选择按钮
mode_label = tk.Label(root, text="选择游戏模式", font=("Arial", 14))
mode_label.place(relx=0.35, rely=0.1, relwidth=0.3, relheight=0.1)
single_mode_button = tk.Button(root, text="人机模式", font=("Arial", 14),command=play_menu)
single_mode_button.place(relx=0.2, rely=0.2, relwidth=0.2, relheight=0.1)
double_mode_button = tk.Button(root, text="双人对战", font=("Arial", 14),command=play_menu)
double_mode_button.place(relx=0.6, rely=0.2, relwidth=0.2, relheight=0.1)

# 创建商店按钮
shop_button = tk.Button(root, text="商店", font=("Arial", 14))
shop_button.place(relx=0.35, rely=0.4, relwidth=0.3, relheight=0.1)

# 创建排名按钮
rank_button = tk.Button(root, text="排名", font=("Arial", 14))
rank_button.place(relx=0.35, rely=0.6, relwidth=0.3, relheight=0.1)

# 创建退出游戏按钮
exit_button = tk.Button(root, text="退出游戏", font=("Arial", 14), command=root.quit)
exit_button.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.1)

# 运行主循环
root.mainloop()