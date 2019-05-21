# Sample code!

### Tetris

#### Micro-Python
```
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
                
    

ori = 0
xi_prev = 0
deBounce = False

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
```
### Music synthetiser

#### Micro-Python
```
from microbit import *
import speech
import music
import math
while True:
    while button_a.is_pressed():
        pin0.set_analog_period_microseconds(256)
        pin2value = pin2.read_analog()
        pin1value = pin1.read_analog()
        while button_b.is_pressed():
            duration = pin2.read_analog()
            step = pin1.read_analog()
            for i in range(0, 1023, 1):
                for j in range(0, duration, step):
                    pin0.write_analog(i)
            for i in range(1023,0,-1):
                for j in range(0, duration, step):
                    pin0.write_analog(i)

        music.pitch(pin2value, pin1value)
        sleep(pin1value)
    while button_b.is_pressed():
        pin2value = pin2.read_analog()
        pin2value = math.floor(pin2value / 4)
        pin1value = pin1.read_analog()
        pin1value = math.floor(pin1value / 4)
        string = speech.translate("Rock the ")
        speech.pronounce(string,speed=120, pitch=pin2value, throat=100, mouth=pin1value)
```
#### Makecode

![Part list from Digikey](./makecode/makecode_letters_chat.png)

### Chat application

#### Micro-Python
```
from microbit import *
import speech
import music
import math
import radio

def mapInteger(anInteger, from1, to1, from2, to2):
    span1 = to1 - from1
    span2 = to2 - from2
    scaling_factor = span1 / span2
    return math.floor(anInteger / scaling_factor)

def selectLetter(alphabet):
    letter_index = mapInteger(pin1.read_analog(),0,1023,0,len(min_alphabet))
    letter = alphabet[letter_index]
    return letter

def send_message(message):
    display.show(Image.HAPPY)
    radio.send(message)
    sleep(1000)

def show_and_pronounce(word):
    string = speech.translate(word)
    speech.pronounce(string,speed=120, pitch=100, throat=100, mouth=200)
    display.scroll(word)

def pronounce(word):
    string = speech.translate(word)
    speech.pronounce(string,speed=120, pitch=100, throat=100, mouth=200)

radio.on()
special_characters = "_?!"
min_alphabet = "abcdefghijklmnopqrstuvwxyz" + special_characters
cap_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + special_characters
outgoing = ""

while True:
    if button_a.is_pressed():
        letter = selectLetter(cap_alphabet)
    else:
        letter = selectLetter(min_alphabet)

    display.show(letter)
    incoming = radio.receive()
    if incoming != None:
        display.scroll("*** ")
        show_and_pronounce(incoming)
        display.scroll("*** ")

    if accelerometer.was_gesture("shake"):
        show_and_pronounce(outgoing)

    if accelerometer.was_gesture("face down"):
        pronounce(outgoing)

    i = 0
    while button_b.is_pressed():
        if i == 0:
            outgoing += letter
            i += 1
        elif i > 5: #when a pressed for more then 1.25 sec
            outgoing = outgoing[:-1]
            send_message(outgoing)
            break
        else:
            i += 1
        sleep(250)
```
#### Makecode



## Makecode