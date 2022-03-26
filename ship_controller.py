import cv2

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


mediterranean_map = Map(img)
mediterranean_map.sea_color = [255, 221, 122]

starting_location = [375, 1205]
mouse_ship = Ship(starting_location, mediterranean_map)

while(1):
    img[0: height, 0: width] = img_copy[0: height, 0: width]
    cv2.circle(img, (mouse_ship.location[1], mouse_ship.location[0]), Ship.radius, (0, 0, 255), -1)
    cv2.imshow('Ship Controller', img)
    k = cv2.waitKeyEx(33)
    print(k)
    if k==27:    # Esc key to stop
        break
    if k == 2490368: # up
        mouse_ship.move("up")
    if k == 2555904: # right
        mouse_ship.move("right")
    if k == 2621440: # down
        mouse_ship.move("down")
    if k == 2424832: # left
        mouse_ship.move("left")
