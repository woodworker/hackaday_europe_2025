from machine import I2C, Pin
import time

LED_ARM_COUNT = 8
LEDS_PER_ARM = 7

LETTER_OFFSET = 0

time_per_char = 400
nickname = "abcdefghijklmnopqrstuvwxyz"



counter = 0
chars = {
 " ": [  0,  0,  0,  0,  0,  0,  0,  0],
 "a": [  0, 31,  5,  9, 62,  2,  4, 32],
 "b": [120,  0,  1,  4, 17,127,  5, 18],
 "c": [112, 96,  0,  0,112,112,112,112],
 "d": [127,  1,  2,  4, 16,126,  4, 16],
 "e": [114, 64,  0,  0,112,127,  5, 17],
 "f": [ 64,  0,  0,  0,112,127,  5, 17],
 "g": [114,120,  0, 16,120, 62,  4, 17],
 "h": [ 66,126,  4, 16, 64,127,  5, 17],
 "i": [ 64,  0,  0,  0,  0,126,  4, 16],
 "j": [126,  2,  4, 16,112, 64,  0,  0],
 "k": [ 72, 32,  0,  7,  1,255,  5, 18],
 "l": [112, 64,  0,  0,  0,126,  4, 16],
 "m": [ 64,126,  4, 20,104,126,  4, 16],
 "n": [ 68,126,  5, 18, 72,126,  4, 17],
 "o": [ 64, 64, 64, 64, 64, 64, 64, 64],
 "p": [ 65,  2,  4, 16,112,126,  5, 17],
 "q": [126, 34,  4, 16,112, 62,  4, 18],
 "r": [ 72, 33,  4, 16, 96,255,  5, 18],
 "s": [127,  0,  0,  0,127,  0,  0,  0],
 "t": [ 32,  0,  0,  3,121, 33,  2,  8],
 "u": [112,126,  4, 16, 64, 62,  4, 16],
 "v": [ 62,  2,  4, 32,  0, 30,  4,  8],
 "w": [104,126,  4, 16, 64,126,  4, 20],
 "x": [  4, 33,  4, 33,  4, 33,  4, 33],
 "y": [ 32,  1,  4, 32,  3, 16,  1,  4],
 "z": [120, 32,  3,  8,120, 32,  3,  8],
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


def write_leds(led_arm, which_leds):
    petal_bus.writeto_mem(PETAL_ADDRESS, led_arm, bytes(which_leds))
        
def clear_leds():
    for i in range(1,9):
        write_leds(i, [0])

def rotate_array(arr, offset):
    """
    positive offset will rotate counterclockwise
    negative offset will rotate clockwise
    """
    offset = offset % len(arr)
    # Rotate by slicing and concatenating
    return arr[-offset:] + arr[:-offset]

def rotate_frame(single_frame, time_ms):
    clear_leds()
    for offset in range(LED_ARM_COUNT):
        new_frame = rotate_array(single_frame, offset*-1)
        for i, num in enumerate(new_frame):
            write_leds(i+1, [num])
        time.sleep_ms(time_ms)
        clear_leds()

def write_chars(string, sleep_per_char, offset=0):
    string = string.strip() + "  "
    for c in string:
        if c not in chars:
            c = " "
        clear_leds();
        time.sleep_ms(20)
        char_frame = chars[c]
        char_frame = rotate_array(char_frame, offset)
        for j, which_leds in enumerate(char_frame):
            write_leds(j+1, [which_leds])
            time.sleep_ms(10)
        time.sleep_ms(sleep_per_char)
            

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
    
    #play_frames(frames,time_per_char)
    write_chars(nickname, time_per_char, LETTER_OFFSET)

    clear_leds();
    #startup(range(8), 30);


while True:

    ## display button status on RGB
    check = 0
    if petal_bus:
        if not buttonA.value():
            check = check + 1
            
            
            """
            rotate the letters by one strand clockwise
            """
            isNeg = LETTER_OFFSET < 0
            LETTER_OFFSET = (LETTER_OFFSET-1) % LED_ARM_COUNT
            if isNeg:
                LETTER_OFFSET = LETTER_OFFSET * -1
            
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
            
            """
            rotate the letters by one strand counter clockwise
            """
            isNeg = LETTER_OFFSET < 0
            LETTER_OFFSET = (LETTER_OFFSET+1) % LED_ARM_COUNT
            if isNeg:
                LETTER_OFFSET = LETTER_OFFSET * -1
            
            petal_bus.writeto_mem(PETAL_ADDRESS, 4, bytes([0x80]))
        else:
            petal_bus.writeto_mem(PETAL_ADDRESS, 4, bytes([0x00]))

    #play_frames(frames,time_per_char)
    write_chars(nickname, time_per_char, LETTER_OFFSET)

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
