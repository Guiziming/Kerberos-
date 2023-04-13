from PIL import Image

# 打开原始图像
image = Image.open("E:\\code\\mycode\\source\\future_shop.png")

# 设置目标尺寸
new_width = 76
new_height = 62.5

# 使用thumbnail方法按照目标尺寸缩放图像，保持原始图像的纵横比
image.thumbnail((new_width, new_height))

# 保存缩放后的图像
image.save("E:\\code\\mycode\\source\\future_shop_new.png")
