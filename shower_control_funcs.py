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

def set_change_song_flag(SONG_BUTTON_STATE, PREV_PRESSED_SONG_CHANGE, CHANGE_SONG_FLAG):
    if SONG_BUTTON_STATE:
        if not PREV_PRESSED_SONG_CHANGE:
            CHANGE_SONG_FLAG = True
        PREV_PRESSED_SONG_CHANGE = True
    else:
        PREV_PRESSED_SONG_CHANGE = False
    return CHANGE_SONG_FLAG, PREV_PRESSED_SONG_CHANGE


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


def print_state(t1, print_time, CHANGE_SONG_FLAG,song_enum,PREV_PRESSED_SONG_CHANGE,PREV_PRESSED_POWER):
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