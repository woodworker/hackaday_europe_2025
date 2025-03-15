from machine import I2C, Pin
import time

LED_ARM_COUNT = 8
LEDS_PER_ARM = 7

counter = 0
chars = {
 "w": [104,126,  4, 16, 64,126,  4, 20],
 "m": [ 64,126,  4, 20,104,126,  4, 16],
 "o": [ 64, 64, 64, 64, 64, 64, 64, 64],
 "d": [124,  14,  2, 4, 16,126,  4, 16],
 "y": [ 32,  1,  4, 32,  3, 16,  1,  4],
 " ": [  0,  0,  0,  0,  0,  0,  0,  0],
}

frames = [
    chars["w"],
    chars["o"],
    chars["o"],
    chars["d"],
    chars["y"],
    chars[" "],
    chars[" "],
]

time_per_char = 200

def write_leds(led_arm, which_leds):
    print("=======")
    print(led_arm, which_leds)
    print("=======")
    petal_bus.writeto_mem(PETAL_ADDRESS, led_arm, bytes(which_leds))
        
def clear_leds():
    for i in range(1,9):
        write_leds(i, [0])

def rotate_frame(single_frame, time_ms):
"""
 since the display is rotaional symetric we can transpose ever frame to rotate arround
"""
  clear_leds()
    for start in range(LED_ARM_COUNT):
        for i in range(1, LED_ARM_COUNT+1):
            start_offset = ((i+start) % LED_ARM_COUNT)
            write_leds(i, [single_frame[start_offset]])
        time.sleep_ms(time_ms)
        clear_leds()
        

def play_frames(frames, sleep_per_led):
    clear_leds();
    time.sleep_ms(sleep_per_led)
    for row in frames:
        clear_leds();
        time.sleep_ms(20)
        for j, which_leds in enumerate(row):
            write_leds(j+1, [which_leds])
            time.sleep_ms(10)
        time.sleep_ms(sleep_per_led)

def startup(order, sleep):
    for j in order:
        which_leds = (1 << (j+1)) - 1 
        for i in range(1,9):
            print(which_leds)
            write_leds(i, [which_leds])
            #petal_bus.writeto_mem(PETAL_ADDRESS, i, bytes([which_leds]))
            time.sleep_ms(sleep)
            write_leds(i, [which_leds])
            #petal_bus.writeto_mem(PETAL_ADDRESS, i, bytes([which_leds]))
    # and clear
    clear_leds()    
#

## do a quick spiral to test
if petal_bus:
    clear_leds();
    
    play_frames(frames,time_per_char)
    
    rotate_frame(chars["w"], time_per_char)
    rotate_frame(chars["o"], time_per_char)
    rotate_frame(chars["o"], time_per_char)
    rotate_frame(chars["d"], time_per_char)
    rotate_frame(chars["y"], time_per_char)
    rotate_frame(chars[" "], time_per_char)
    
    clear_leds();
    #startup(range(8), 30);


while True:

    ## display button status on RGB
    check = 0
    if petal_bus:
        if not buttonA.value():
            check = check + 1
            petal_bus.writeto_mem(PETAL_ADDRESS, 2, bytes([0x80]))
        else:
            petal_bus.writeto_mem(PETAL_ADDRESS, 2, bytes([0x00]))

        if not buttonB.value():
            check = check + 1
            petal_bus.writeto_mem(PETAL_ADDRESS, 3, bytes([0x80]))
        else:
            petal_bus.writeto_mem(PETAL_ADDRESS, 3, bytes([0x00]))

        if not buttonC.value():
            check = check + 1
            petal_bus.writeto_mem(PETAL_ADDRESS, 4, bytes([0x80]))
        else:
            petal_bus.writeto_mem(PETAL_ADDRESS, 4, bytes([0x00]))

    #if check == 3:
    #    startup([1,2,3,4,5,6,7],90);

    play_frames(frames,time_per_char)

    ## see what's going on with the touch wheel
    if touchwheel_bus:
        tw = touchwheel_read(touchwheel_bus)

    ## display touchwheel on petal
    if petal_bus and touchwheel_bus:
        if tw > 0:
            tw = (128 - tw) % 256 
            petal = int(tw/32) + 1
        else: 
            petal = 999
        for i in range(1,9):
            if i == petal:
                petal_bus.writeto_mem(0, i, bytes([0x7F]))
            else:
                petal_bus.writeto_mem(0, i, bytes([0x00]))


    
    time.sleep_ms(100)
    bootLED.off()
