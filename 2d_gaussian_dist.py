import numpy as np
import matplotlib.pyplot as plt

IMAGE_WIDTH = 8
IMAGE_HEIGHT = 8

center_x = IMAGE_WIDTH/2
center_y = IMAGE_HEIGHT/2

R = np.sqrt(center_x**2 + center_y**2)

Gauss_map = np.zeros((IMAGE_HEIGHT, IMAGE_WIDTH))

# 利用 for 循环 实现
for i in range(IMAGE_HEIGHT):
    for j in range(IMAGE_WIDTH):
        dis = np.sqrt((i-center_x)**2+(j-center_x)**2)
        Gauss_map[i, j] = np.exp(-2.0*dis/R)
        print("i, j, value:",i-center_x,j-center_x,Gauss_map)

# 显示和保存生成的图像
plt.figure()
plt.imshow(Gauss_map, plt.cm.gray)
plt.imsave('out_2.jpg', Gauss_map, cmap=plt.cm.gray)
plt.show()
