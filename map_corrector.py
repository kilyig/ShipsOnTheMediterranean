import cv2
import time
import random

img = cv2.imread("./images/map.png")

correct = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

height, width, channels = img.shape

sea = img[50, 50]
print("Sea color: ", sea)

land = img[height-1, width-1]
print("Land color: ", land)

new_land = [198, 255, 122]

print("Height: ", height)
print("Width: ", width)
print("Channels: ", channels)

for i in range(0, height):
    for j in range(0, width):
        if img[i, j, 0] != sea[0]:
            img[i, j] = land
        if img[i, j, 0] == land[0]:
             img[i, j] = new_land

cv2.imshow('image', img)
