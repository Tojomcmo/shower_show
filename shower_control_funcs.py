import RPi.GPIO as GPIO
import random
import time
from pygame import mixer



def pick_rand_new_song(enum_list:list, prev_enum:str):
    if len(enum_list) == 1:
        new_song_enum = prev_enum
    else:
        enum_list = enum_list[:]
        enum_list.remove(prev_enum)
        new_song_enum = random.sample(enum_list,1)[0]
    return new_song_enum

def get_song_path(name_list, enum):
    return 'song_list/' + str(name_list[enum])

def start_song(name_list, enum):
    mixer.music.stop()
    mixer.music.load(get_song_path(name_list, enum))
    mixer.music.play()
    return

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

def set_song_state(POWER_STATE, PREV_POWER_STATE, CHANGE_SONG_FLAG, song_names_list, song_enum_list, song_enum):
    # power state logic
    if POWER_STATE:
        # if this is the initial state change to on, begin song
        if not PREV_POWER_STATE:
            song_enum = pick_rand_new_song(song_enum_list, song_enum)
            start_song(song_names_list, song_enum)
            CHANGE_SONG_FLAG = False
            PREV_POWER_STATE = True
        # if the state has been on, check song state
        else:
            # if new song flag is true or if song has ended, pick new song and play
            if CHANGE_SONG_FLAG or not mixer.music.get_busy():
                song_enum = pick_rand_new_song(song_enum_list, song_enum)
                start_song(song_names_list, song_enum)
                CHANGE_SONG_FLAG = False
    # if power state is off, power off outputs and stop music
    else:
        mixer.music.stop()
        PREV_POWER_STATE = False
        CHANGE_SONG_FLAG = False
    return PREV_POWER_STATE, CHANGE_SONG_FLAG, song_enum

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
            if SHOWER_CHANGE_FLAG or (shower_start_time - shower_duration_time >= 0):
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