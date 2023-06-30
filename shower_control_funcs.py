import RPi.GPIO as GPIO
import random
import time
from pygame import mixer
from os import listdir

def button_press_filter(button_val:int, filt:list, pass_criterion:float, STATE:bool):
    val = button_val
    filt.pop(0)
    filt.append(val)
    if (sum(filt)/len(filt)) < (1 - pass_criterion):
        STATE = False
    elif (sum(filt)/len(filt)) > (pass_criterion):
        STATE = True
    return STATE, filt

def set_flag(BTN_STATE, PREV_PRESSED_BTN, FLAG_STATE):
    if BTN_STATE:
        if not PREV_PRESSED_BTN:
            FLAG_STATE = True
        PREV_PRESSED_BTN = True
    else:
        PREV_PRESSED_BTN = False
    return FLAG_STATE, PREV_PRESSED_BTN

def set_shower_state(POWER_STATE, 
                     SHOWER_STATE,
                     SHOWER_CHANGE_FLAG,
                     GPIO_output_pin,
                     shower_start_time,
                     shower_duration_time):
    if POWER_STATE:
        if not SHOWER_STATE:
            if SHOWER_CHANGE_FLAG:
                GPIO.output(GPIO_output_pin, 1)
                SHOWER_STATE = True
                SHOWER_CHANGE_FLAG = False
                shower_start_time = time.time()        
        elif SHOWER_STATE:
            elapsed_time = time.time() - shower_start_time
            if SHOWER_CHANGE_FLAG or (elapsed_time > shower_duration_time):
                GPIO.output(GPIO_output_pin, 0)
                SHOWER_STATE = False
                SHOWER_CHANGE_FLAG = False
    else:
        SHOWER_STATE = False
        GPIO.output(GPIO_output_pin, 0)
    return SHOWER_STATE, SHOWER_CHANGE_FLAG, shower_start_time

def print_state(t1, 
                print_time, 
                CHANGE_SONG_FLAG,
                song_enum,
                PREV_PRESSED_SONG_CHANGE,
                PREV_PRESSED_POWER):
    time_elapsed = time.time() - t1
    if time_elapsed > print_time:
        print("chg_song_flag  ,  song_num  ,  song_btn  , pwr_btn  , music_state:  ",
            CHANGE_SONG_FLAG, " , ",
            song_enum, " , ",
            PREV_PRESSED_SONG_CHANGE, "  ,  ",
            PREV_PRESSED_POWER, "  ,  ",
            mixer.music.get_busy())
        t1 = time.time()
    return t1    