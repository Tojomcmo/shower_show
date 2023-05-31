import random
import gpiozero as gpio
import time
from os import listdir
from pygame import mixer

def pick_rand_new_song(enum_list:list, prev_enum:str):
    if len(enum_list) == 1:
        new_song_enum = prev_enum
    else:
        enum_list = enum_list[:]
        enum_list.remove(prev_enum)
        new_song_enum = random.sample(enum_list,1)[0]
    return new_song_enum

def button_press_filter(button:gpio.Button, filt:list, pass_criterion:float, STATE:bool):
    val = button.value
    filt.pop(0)
    filt.append(val)
    if (sum(filt)/len(filt)) < (1 - pass_criterion):
        STATE = False
    elif (sum(filt)/len(filt)) > (pass_criterion):
        STATE = True
    return STATE, filt

def get_song_path(name_list, enum):
    return 'song_list/' + str(name_list[enum])

def start_song(name_list, enum):
    mixer.music.stop()
    mixer.music.load(get_song_path(name_list, enum))
    mixer.music.play()
    return

#define GPIO inputs
power_button       = gpio.Button("GPIO17")
song_change_button = gpio.Button("GPIO18")
hard_kill          = gpio.Button("GPIO24")
# define GPIO outputs
shower_relay       = gpio.DigitalOutputDevice("GPIO27")
amp_relay          = gpio.DigitalOutputDevice("GPIO22")
disco_relay        = gpio.DigitalOutputDevice("GPIO23")



# open directory of songs, pick initial song
song_names_list = listdir("song_list")
song_enum_list  = list(range(0,len(song_names_list)))
song_enum       = random.sample(song_enum_list,1)[0]
# initiate music mixer
# song_thread = mixer.init()
# song_thread.music.load("song_list/", str(song_names_list[song_enum]))
mixer.init()
song_str = get_song_path(song_names_list, song_enum)
mixer.music.load(song_str)
mixer.music.set_volume(0.5)

# create button filters
song_button_filter = [0] * 30
power_filter       = [0] * 30
SONG_BUTTON_STATE  = False
POWER_STATE        = False
BUTTON_DEADZONE    = 0.9

# define logic states
PREV_PRESSED_SONG_CHANGE = False
PREV_PRESSED_POWER       = False
CHANGE_SONG_FLAG         = False

# set print scheduele
print_time = 0.1
t1         = time.time()

# main loop
while(True):
    #check whether the kill-switch is pressed
    if hard_kill.is_pressed:
        exit()
    else:    
        # check button states with filter for noisy state change
        SONG_BUTTON_STATE,song_button_filter = button_press_filter(song_change_button,
                                                                song_button_filter,
                                                                BUTTON_DEADZONE,
                                                                SONG_BUTTON_STATE)
        POWER_STATE,power_filter = button_press_filter(power_button,
                                                        power_filter,
                                                        BUTTON_DEADZONE,
                                                        POWER_STATE)
        
        # music change logic
        # if first state change and not continued press, set song change flag to true, else do nothing
        if SONG_BUTTON_STATE:
            if not PREV_PRESSED_SONG_CHANGE:
                CHANGE_SONG_FLAG = True
            PREV_PRESSED_SONG_CHANGE = True
        else:
            PREV_PRESSED_SONG_CHANGE = False

        # power state logic
        if POWER_STATE:
            # if this is the initial state change to on, turn on outputs and begin song
            if not PREV_PRESSED_POWER:
                shower_relay.on()
                amp_relay.on()
                disco_relay.on()
                song_enum = pick_rand_new_song(song_enum_list, song_enum)
                start_song(song_names_list, song_enum)
                CHANGE_SONG_FLAG = False
                PREV_PRESSED_POWER = True
            # if the state has been on, check song state
            else:
                # if new song flag is true or if song has ended, pick new song and play
                if CHANGE_SONG_FLAG or not mixer.music.get_busy():
                    song_enum = pick_rand_new_song(song_enum_list, song_enum)
                    start_song(song_names_list, song_enum)
                    CHANGE_SONG_FLAG = False
        # if power state is off, power off outputs and stop music
        else:
            shower_relay.off()
            amp_relay.off()
            disco_relay.off()
            mixer.music.stop()
            PREV_PRESSED_POWER = False

        time_elapsed = time.time() - t1
        if time_elapsed > print_time:
            print("chg_song_flag  ,  song_num  ,  song_btn  , pwr_btn  , music_state:  ",
                CHANGE_SONG_FLAG, " , ",
                song_enum, " , ",
                PREV_PRESSED_SONG_CHANGE, "  ,  ",
                PREV_PRESSED_POWER, "  ,  ",
                mixer.music.get_busy())
            # print("current song: ", song_enum)
            # print("is on: ", prev_pressed_power)
            t1 = time.time()