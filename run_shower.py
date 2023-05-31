import RPi.GPIO as GPIO
import random
import time
from pygame import mixer
from os import listdir

import shower_control_funcs as scf


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    # open directory of songs, pick initial song
    song_names_list = listdir("song_list")
    song_enum_list  = list(range(0,len(song_names_list)))
    song_enum       = random.sample(song_enum_list,1)[0]

    # initiate music mixer
    mixer.init()
    song_str = scf.get_song_path(song_names_list, song_enum)
    mixer.music.load(song_str)
    mixer.music.set_volume(1.0)

    power_state_btn = 17
    song_change_btn = 18
    hard_kill_btn   = 24
    GPIO.setup(power_state_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(song_change_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(hard_kill_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # create button filters
    song_btn_filt   = [0] * 30
    power_btn_filt  = [0] * 30
    SONG_BTN_STATE  = False
    POWER_BTN_STATE = False
    btn_deadzone    = 0.9

    # define logic states
    PREV_SONG_BTN_STATE      = False
    PREV_POWER_BTN_STATE     = False
    CHANGE_SONG_FLAG         = False

    # set print scheduele
    print_time = 0.2
    t1         = time.time()
    try:
        while(True):
            if GPIO.input(hard_kill_btn):
                raise RuntimeError("hard kill button pressed")
            else:    
                # check button states with filter for noisy state change
                SONG_BTN_STATE,song_btn_filt = scf.button_press_filter(GPIO.input(song_change_btn),
                                                                        song_btn_filt,
                                                                        btn_deadzone,
                                                                        SONG_BTN_STATE)
                
                POWER_BTN_STATE,power_btn_filt = scf.button_press_filter(GPIO.input(power_state_btn),
                                                                        power_btn_filt,
                                                                        btn_deadzone,
                                                                        POWER_BTN_STATE)
                
                CHANGE_SONG_FLAG, PREV_SONG_BTN_STATE = scf.set_change_song_flag(SONG_BTN_STATE, 
                                                                                PREV_SONG_BTN_STATE, 
                                                                                CHANGE_SONG_FLAG)

                PREV_POWER_BTN_STATE, CHANGE_SONG_FLAG, song_enum = scf.set_song_state(POWER_BTN_STATE, 
                                                                                      PREV_POWER_BTN_STATE, 
                                                                                      CHANGE_SONG_FLAG, 
                                                                                      song_names_list, 
                                                                                      song_enum_list, 
                                                                                      song_enum)

                t1 = scf.print_state(t1, 
                                    print_time, 
                                    CHANGE_SONG_FLAG,
                                    song_enum,
                                    PREV_SONG_BTN_STATE,
                                    PREV_POWER_BTN_STATE)

    except KeyboardInterrupt:
        print("cleaning up GPIOs with except from keyboard interrupt")
        GPIO.cleanup()


    except RuntimeError:
        print("cleaning up GPIOs with except from kill button")
        GPIO.cleanup()
