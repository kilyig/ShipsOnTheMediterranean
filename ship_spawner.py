import cv2
import random

img = cv2.imread("./images/map.png")
height, width, channels = img.shape
correct = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img_copy = cv2.imread("./images/map.png")


class Map:
    def __init__(self, img):
        self.image = img
        self.height, self.width, self.channels = self.image.shape
        self.original_image = self.image.copy()
        self.sea_color = []

    def pixel(self, x, y):
        try:
            original_image = self.original_image
            return original_image[x, y]
        except IndexError:
            return original_image[0, self.height]


class Ship:
    radius = 5
    def __init__(self, loc, map):
        self.location = loc
        self.map = map

    def move(self, direction):
        location = self.location
        map = self.map
        if direction == "up":
            if (map.pixel(location[0]-1, location[1]) == [255, 221, 122]).all():
                location[0] -= 1
        if direction == "down":
            if (map.pixel(location[0]+1, location[1]) == map.sea_color).all():
                location[0] += 1
        if direction == "right":
            if (map.pixel(location[0], location[1]+1) == map.sea_color).all():
                location[1] += 1
        if direction == "left":
            if (map.pixel(location[0], location[1]-1) == map.sea_color).all():
                location[1] -= 1


shipList = []

mediterranean_map = Map(img)
mediterranean_map.sea_color = [255, 221, 122]


def mouse_clicked(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if (mediterranean_map.pixel(y, x) == mediterranean_map.sea_color).all():
            ship = Ship([y, x], mediterranean_map)
            shipList.append(ship)
            print("Ship count: ", len(shipList))
            #Ship.radius += 1


while(1):
    img[0: height, 0: width] = img_copy[0: height, 0: width]
    for i in range(0, len(shipList)):
        cv2.circle(img, (shipList[i].location[1], shipList[i].location[0]), Ship.radius, (0, 0, 255), -1)
    cv2.imshow('Ship Spawner', img)
    cv2.setMouseCallback('Ship Spawner', mouse_clicked)
    k = cv2.waitKeyEx(33)
    if k==27:    # Esc key to stop
        break

    for i in range(0, len(shipList)):
        rand = random.randint(0, 3)
        if rand == 0: # up
            shipList[i].move("up")
        if rand == 1: # right
            shipList[i].move("right")
        if rand == 2: # down
            shipList[i].move("down")
        if rand == 3: # left
            shipList[i].move("left")

    # time.sleep(0.5)

