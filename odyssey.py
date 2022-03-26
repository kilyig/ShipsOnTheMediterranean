import cv2
from grid import Grid
from dijkstra import dijkstra
import time
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
    def __init__(self, loc, map, path=[]):
        self.location = loc
        self.map = map
        self.path = path
        self.path_iterator = iter(self.path)

    def move(self, direction):
        location = self.location
        map = self.map
        if direction == "up":
            if (map.pixel(location[0]-1, location[1]) == [255, 221, 122]).all():
                location[0] -= 1
        elif direction == "down":
            if (map.pixel(location[0]+1, location[1]) == map.sea_color).all():
                location[0] += 1
        elif direction == "right":
            if (map.pixel(location[0], location[1]+1) == map.sea_color).all():
                location[1] += 1
        elif direction == "left":
            if (map.pixel(location[0], location[1]-1) == map.sea_color).all():
                location[1] -= 1
        elif direction == "random":
            rand = random.randint(0, 3)
            if rand == 0:
                self.move("up")
            if rand == 1:
                self.move("right")
            if rand == 2:
                self.move("down")
            if rand == 3:
                self.move("left")

    def set_path(self, path):
        self.path = path
        self.path_iterator = iter(self.path)

    def update(self):
        try:
            self.location = next(self.path_iterator)
        except StopIteration:
            self.location = self.location


rows = height
cols = width

mediterranean_map = Map(img)
mediterranean_map.sea_color = [255, 221, 122]

obstacles = []
for i in range(rows):
    for j in range(cols):
        if (mediterranean_map.pixel(i, j) != mediterranean_map.sea_color).all():
            obstacles.append((i, j))

grid = Grid(cols, rows, obstacles)

itinerary = []

itinerary.append((351, 1033)) # ithaca
itinerary.append((287, 1212)) # troy
itinerary.append((247, 1195)) # ismaros
itinerary.append((527, 678)) # tunis
itinerary.append((399, 795)) # cyclops
itinerary.append((344, 839)) # aeolia
itinerary.append((405, 769)) # south of sicily
itinerary.append((351, 1023)) # somewhere near ithaca
itinerary.append((405, 769)) # south of sicily
itinerary.append((344, 839)) # aeolia
itinerary.append((413, 574)) # telepylos
itinerary.append((231, 777)) # circe
itinerary.append((303, 334)) # underworld
itinerary.append((231, 777)) # circe
itinerary.append((275, 815)) # sirens
itinerary.append((357, 863)) # scylla
itinerary.append((453, 826)) # helios
itinerary.append((357, 863)) # scylla
itinerary.append((447, 818)) # ogygia (calypso)
itinerary.append((298, 1006)) # scheria
itinerary.append((351, 1033)) # ithaca

ship = Ship(itinerary[0], mediterranean_map)

path = []
for location in range(len(itinerary)-1):
    path = path + dijkstra(grid, itinerary[location], itinerary[location+1])
    print("Completed", location, "-", (location+1))

ship.set_path(path)


while 1:
    img[0: height, 0: width] = img_copy[0: height, 0: width]
    for location in itinerary:
        if location[0] == 405 and location[1] == 769:
            continue
        if location[0] == 351 and location[1] == 1023:
            continue
        cv2.circle(img, (location[1], location[0]), 5, (255, 0, 0), -1)
    cv2.circle(img, (ship.location[1], ship.location[0]), Ship.radius, (0, 0, 255), -1)
    ship.update()
    cv2.imshow('Odysseus\' Journey', img)
    k = cv2.waitKeyEx(33)
    if k==27:    # Esc key to stop
        break
