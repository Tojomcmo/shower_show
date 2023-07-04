import RPi.GPIO as GPIO
import random
import time
from pygame import mixer
from os import listdir

import shower_control_funcs as scf
import music_control_funcs as mcf


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    #------ Define system parameters ------#
    # define music directory top folder name
    #music_library = 'playlist_dir'
    music_library = '/home/pi/playlist_dir'

    # define GPIO pins
    power_state_btn = 24
    shower_start_btn = 23
    song_change_btn = 18
    playlist_change_btn = 12
    shower_relay_out = 25
    hard_kill_btn   = 17

    # Define button press filter length and deadzone cutoff
    button_press_filt_len = 20
    btn_deadzone = 0.9

    # define CLI print delay and enable bool
    CLI_PRINT_ENABLED = True
    print_delay_time = 0.2

    #define shower duration in seconds
    shower_duration_time = 30

    ## open directory of songs, pick initial song
    music_dict = mcf.create_music_dictionary(music_library)
    current_playlist, current_song, played_song_list = mcf.initialize_playlist_and_song(music_dict)

    # initialize music mixer
    mixer.init()
    song_path  = mcf.get_song_path(music_library, current_playlist, current_song)
    mixer.music.load(song_path)
    mixer.music.set_volume(1.0)

    #initialize GPIOs
    GPIO.setup(power_state_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(song_change_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(playlist_change_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   
    GPIO.setup(shower_start_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(hard_kill_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(shower_relay_out, GPIO.OUT)
    GPIO.output(shower_relay_out, 0)

    # initialize button filters and bool values
    song_btn_filt      = [0] * button_press_filt_len
    playlist_btn_filt  = [0] * button_press_filt_len
    power_btn_filt     = [0] * button_press_filt_len
    shower_btn_filt    = [0] * button_press_filt_len
    SONG_BTN_STATE     = False
    PLAYLIST_BTN_STATE = False
    POWER_BTN_STATE    = False
    SHOWER_BTN_STATE   = False
    SHOWER_STATE       = False

    # initialize logic states
    PREV_SONG_BTN_STATE      = False
    PREV_PLAYLIST_BTN_STATE  = False
    PREV_POWER_BTN_STATE     = False
    PREV_SHOWER_BTN_STATE    = False
    CHANGE_SONG_FLAG         = False
    CHANGE_PLAYLIST_FLAG     = False
    CHANGE_SHOWER_FLAG       = False

    # start timers
    print_time  = time.time()
    shower_start_time = time.time()

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
                
                PLAYLIST_BTN_STATE,playlist_btn_filt = scf.button_press_filter(GPIO.input(playlist_change_btn),
                                                                        playlist_btn_filt,
                                                                        btn_deadzone,
                                                                        PLAYLIST_BTN_STATE)                
                
                POWER_BTN_STATE,power_btn_filt = scf.button_press_filter(GPIO.input(power_state_btn),
                                                                        power_btn_filt,
                                                                        btn_deadzone,
                                                                        POWER_BTN_STATE)

                SHOWER_BTN_STATE,shower_btn_filt = scf.button_press_filter(GPIO.input(shower_start_btn),
                                                                        shower_btn_filt,
                                                                        btn_deadzone,
                                                                        SHOWER_BTN_STATE)
                
                CHANGE_SONG_FLAG, PREV_SONG_BTN_STATE = scf.set_flag(SONG_BTN_STATE,
                                                                    PREV_SONG_BTN_STATE,
                                                                    CHANGE_SONG_FLAG)

                CHANGE_PLAYLIST_FLAG, PREV_PLAYLIST_BTN_STATE = scf.set_flag(PLAYLIST_BTN_STATE,
                                                                            PREV_PLAYLIST_BTN_STATE,
                                                                            CHANGE_PLAYLIST_FLAG)
                
                CHANGE_SHOWER_FLAG, PREV_SHOWER_BTN_STATE = scf.set_flag(SHOWER_BTN_STATE,
                                                                        PREV_SHOWER_BTN_STATE,
                                                                        CHANGE_SHOWER_FLAG)

                PREV_POWER_BTN_STATE, CHANGE_SONG_FLAG, CHANGE_PLAYLIST_FLAG, current_playlist, current_song, played_song_list = mcf.set_song_state(POWER_BTN_STATE,
                                                                                                                                PREV_POWER_BTN_STATE,
                                                                                                                                CHANGE_SONG_FLAG,
                                                                                                                                CHANGE_PLAYLIST_FLAG,
                                                                                                                                music_dict,
                                                                                                                                music_library,
                                                                                                                                current_playlist,
                                                                                                                                current_song,
                                                                                                                                played_song_list)
                
                SHOWER_STATE, CHANGE_SHOWER_FLAG, shower_start_time = scf.set_shower_state(POWER_BTN_STATE,
                                                                                            SHOWER_STATE,
                                                                                            CHANGE_SHOWER_FLAG,
                                                                                            shower_relay_out,
                                                                                            shower_start_time,
                                                                                            shower_duration_time)
                if CLI_PRINT_ENABLED:
                    t1 = scf.print_state(print_time,
                                        print_delay_time,
                                        SONG_BTN_STATE,
                                        PLAYLIST_BTN_STATE,
                                        POWER_BTN_STATE,
                                        SHOWER_BTN_STATE,
                                        current_song,
                                        current_playlist)

    except KeyboardInterrupt:
        print("cleaning up GPIOs with except from keyboard interrupt")
        GPIO.cleanup()


    except RuntimeError as err:
        print(err.args)
        print("cleaning up GPIOs")
        GPIO.cleanup()