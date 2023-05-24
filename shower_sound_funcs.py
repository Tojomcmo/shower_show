import pygame
import random
import gpiozero as gpio
import time
from os import listdir


def pick_rand_new_song(song_enum_list, prev_song_enum):
    if len(song_enum_list) == 1:
        new_song_enum = prev_song_enum
    else:
        enum_list = song_enum_list[:]
        enum_list.remove(prev_song_enum)
        new_song_enum = random.sample(enum_list,1)[0]
    return new_song_enum    

def button_press_filter(button, filter, pass_criterion, state):
    val = button.value
    filter.pop(0)
    filter.append(val)
    if (sum(filter)/len(filter)) < (1 - pass_criterion):
        state = False
    elif (sum(filter)/len(filter)) > (pass_criterion):  
        state = True
    return state, filter     

#define GPIOs
on_off_button      = gpio.Button("GPIO17")
song_change_button = gpio.Button("GPIO18")
shower_relay       = gpio.DigitalOutputDevice("GPIO27")
amp_relay          = gpio.DigitalOutputDevice("GPIO22")
disco_relay        = gpio.DigitalOutputDevice("GPIO23")


# open directory of songs, pick initial song
song_names_list = listdir("song_list")
song_enum_list  = list(range(0,len(song_names_list)))
song_enum       = random.sample(song_enum_list,1)[0]

# create button filters
song_button_filter = [0] * 30
on_off_filter      = [0] * 30
song_button_state  = False
on_off_state       = False
button_deadzone    = 0.9

# define logic states
prev_pressed_song_change = False
prev_pressed_on_off      = False
change_song_flag         = False

# set print scheduele
print_time = 0.1
t1 = time.time()
while(True):
    song_button_state,song_button_filter = button_press_filter(song_change_button,
                                                               song_button_filter,
                                                               button_deadzone,
                                                               song_button_state)
    if song_button_state:
        if not prev_pressed_song_change: 
            change_song_flag = True
        prev_pressed_song_change = True
    else:
        prev_pressed_song_change = False

    on_off_state,on_off_filter = button_press_filter(on_off_button,
                                                     on_off_filter,
                                                     button_deadzone,
                                                     on_off_state)
    if on_off_state:
        if not prev_pressed_on_off:
            shower_relay.on()
            amp_relay.on()
            disco_relay.on()
            if change_song_flag:
                song_enum = pick_rand_new_song(song_enum_list, song_enum)
                change_song_flag = False
        else:
            if change_song_flag:
                song_enum = pick_rand_new_song(song_enum_list, song_enum)
                change_song_flag = False
        prev_pressed_on_off = True
    else:
        shower_relay.off()
        amp_relay.off()
        disco_relay.off()
        prev_pressed_on_off = False    

    time_elapsed = time.time() - t1 
    if time_elapsed > print_time:
        print("songflag  ,  song  ,  song_prev_press  , is on: ", 
              change_song_flag, " , ", 
              song_enum, " , ", 
              prev_pressed_song_change, "  ,  ",
              prev_pressed_on_off)
        # print("current song: ", song_enum)
        # print("is on: ", prev_pressed_on_off)
        t1 = time.time()