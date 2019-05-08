from microbit import *
import speech
import music
import math

display.show(Image.HAPPY)
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
        string = speech.translate("Rock on!")
        speech.pronounce(string,speed=120, pitch=pin2value, throat=100, mouth=pin1value)