from microbit import *
import math
import random


def mapInteger(anInteger, from1, to1, from2, to2):
    span1 = math.fabs(to1 - from1 + 1)
    span2 = math.fabs(to2 - from2 + 1)
    scaling_factor = span1 / span2
    return int(from2 + math.floor(anInteger / scaling_factor))
    
def selectCoordinates(min_x, max_x):
    x_index = mapInteger(pin1.read_analog(),0,1023,0,4)
    x_index = max_x if x_index > (max_x - 1) else x_index
    x_index = min_x if x_index < min_x else x_index
    y_index = mapInteger(pin2.read_analog(),0,1023,0,4)
    coordinates = [x_index, y_index]
    return coordinates

def selectXCoordinate(min_x, max_x):
    x_index = mapInteger(pin1.read_analog(),0,1023,0,4)
    x_index = max_x if x_index > (max_x - 1) else x_index
    x_index = min_x if x_index < min_x else x_index
    return x_index

def binaryDecompositon(integer):
    b1 = integer % 2 == 1
    b2 = (integer - 2) >= 0
    sn1 = 1 if b1 == 1 else -1
    sn2 = 1 if b2 == 1 else -1
    return [b1, b2, sn1, sn2]

def switchOn(x, y):
    if 0 <= y <= 4 and 0 <= x <= 4:
        display.set_pixel(x, y, 9)

def refreshDisplay(shape_obj, ground_obj):
    display.clear()
    removeFullLine(ground_obj)
    updateVertices(shape_obj)
    draw(shape_obj)
    draw(ground_obj)
    
def draw(an_object):
    for tup in an_object.vertices:
        switchOn(tup[0], tup[1])

def checkIntersection(shape_obj, ground_obj):
    return not set(ground_obj.vertices).isdisjoint(shape_obj.vertices)

def updateVertices(shape):
    
    if shape.type == 0: #dot
        shape.x = selectXCoordinate(0,4)
        v0 = (shape.x, shape.y)
        shape.vertices = [v0]
    
    if shape.type == 1: #two pixels line
        b, _, _, sn = binaryDecompositon(shape.orientation)
        shape.x = selectXCoordinate(0 - sn * b, 4 - sn * b)
        v0 = (shape.x, shape.y)
        v1 = ((shape.x + sn * b ) % 5, shape.y + sn * (not b))
        shape.vertices = [v0, v1]
    
    if shape.type == 2: #three pixels l-shape
        b1, _, _, sn1 = binaryDecompositon(shape.orientation)
        b2, _, _, sn2 = binaryDecompositon((shape.orientation + 1) % 4)
        offset = sn1 * b1 + sn2 * b2
        l_offset = offset if offset < 0 else 0
        r_offset = offset if offset > 0 else 0
        shape.x = selectXCoordinate(0 - l_offset, 4 - r_offset)
        v0 = (shape.x, shape.y)
        v1 = ((shape.x + sn1 * b1 ) % 5, shape.y + sn1 * (not b1))
        v2 = ((shape.x + sn2 * b2 ) % 5, shape.y + sn2 * (not b2))
        shape.vertices = [v0, v1, v2]
        
    if shape.type == 3: #three pixels line
        b, _, _, sn = binaryDecompositon(shape.orientation)
        shape.x = selectXCoordinate(0 + b, 4 - b)
        v0 = (shape.x, shape.y)
        v1 = ((shape.x + sn * b ) % 5, shape.y + sn * (not b))
        v2 = ((shape.x - sn * b ) % 5, shape.y - sn * (not b))
        shape.vertices = [v0, v1, v2]
        
def removeFullLine(ground):
    prev_vertices = [tup for tup in ground.vertices if tup[1] != 5]
    ys = [tup[1] for tup in prev_vertices]
    full_lines = []
    for i in set(ys):
        count = sum([1 for y in ys if y == i])
        if count == 5:
            full_lines.append(i)
    ground.vertices = [(0,5), (1,5), (2,5), (3,5), (4,5)]
    for tup in prev_vertices:
        if tup[1] not in full_lines:
            collapse = sum([1 for i in full_lines if tup[1] < i])
            ground.vertices.append((tup[0], tup[1] + collapse))

class Shape(object):
    
    def __init__(self):
        self.type = random.randint(0, 3) # an integer between 0 and 3 included
        self.orientation = 0 # an integer between 0 and 3 included
        self.x = 0 # x index of control vertex
        self.y = 1 # y index of control vertex
        self.vertices = []
        
    def drop(self, ground_obj):
        while True:
            self.y += 1
            updateVertices(self)
            if checkIntersection(self, ground_obj):
                self.y -= 1
                updateVertices(self)
                break


class Ground(object):
    
    def __init__(self):
        self.vertices = [(0,5), (1,5), (2,5), (3,5), (4,5)]
        
    def addShape(self, shape_obj):
        for tup in shape_obj.vertices:
            self.vertices.append(tup)
                
    

# Variable initialization
ori = 0
xi_prev = 0
deBounce = False

# Game initialization
ground_obj = Ground()
shape_obj = Shape()
refreshDisplay(shape_obj, ground_obj)


while True:
    
    while button_a.is_pressed():
        if deBounce == False:
            shape_obj.drop(ground_obj)
            ground_obj.addShape(shape_obj)
            shape_obj = Shape()
            refreshDisplay(shape_obj, ground_obj)
            deBounce = True
        else:
            deBounce = True

    
    while button_b.is_pressed():
        if deBounce == False:
            ori = (ori + 1) % 4
            shape_obj.orientation = ori
            refreshDisplay(shape_obj, ground_obj)
            deBounce = True
        else:
            deBounce = True
    deBounce = False
    
    x_index = mapInteger(pin1.read_analog(),0,1023,0,4)
    if xi_prev != x_index:
        xi_prev = x_index
        refreshDisplay(shape_obj, ground_obj)