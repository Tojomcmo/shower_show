import random
from pygame import mixer
from os import listdir

def create_music_dictionaries(library_name):
    playlist_names_list = listdir(library_name)
    music_dict = {}
    for playlist in playlist_names_list:
        song_names_list = listdir(library_name + '/' + playlist)
        music_dict[playlist] = song_names_list
    return music_dict

def initialize_playlist_and_song(music_dict):
    current_playlist = next(iter(music_dict))
    current_song = random.choice(music_dict[current_playlist])  
    return current_playlist, current_song  

def get_next_playlist_and_first_song(music_dict, current_playlist):
    music_dict_iter = iter(music_dict)
    for key in music_dict_iter:
        if key == current_playlist:
            next_playlist = next(music_dict_iter, None)
    next_song = music_dict[next_playlist][0]  
    return next_playlist, next_song

def get_rand_new_song(music_dict, current_playlist, current_song):
    song_name_list = music_dict[current_playlist][:]
    if len(song_name_list) == 1:
        next_song = current_song
    else:
        song_name_list.remove(current_song)
        next_song = random.choice(song_name_list)
    return next_song

def get_song_path(current_playlist,
                  current_song):
    return ('playlist_dir/'+ current_playlist + '/' + current_song)

def start_song(current_playlist, current_song):
    mixer.music.stop()
    mixer.music.load(get_song_path(current_playlist, current_song))
    mixer.music.play()
    return

def set_song_state(POWER_STATE,
                   PREV_POWER_STATE,
                   CHANGE_SONG_FLAG,
                   CHANGE_PLAYLIST_FLAG,
                   music_dict,
                   current_playlist,
                   current_song):
    # power state logic
    if POWER_STATE:
        # if this is the initial state change to on, begin song
        if not PREV_POWER_STATE:
            current_playlist, current_song = get_next_playlist_and_first_song(music_dict, current_playlist)
            start_song(current_playlist, current_song)
            CHANGE_SONG_FLAG = False
            CHANGE_PLAYLIST_FLAG = False
            PREV_POWER_STATE = True
        # if the state has been on, check song state
        else:
            # if new song flag is true or if song has ended, pick new song and play
            if CHANGE_PLAYLIST_FLAG:
                current_playlist, current_song = get_next_playlist_and_first_song(music_dict, current_playlist)
                start_song(current_playlist, current_song)
                CHANGE_PLAYLIST_FLAG = False
                CHANGE_SONG_FLAG = False
            if CHANGE_SONG_FLAG or not mixer.music.get_busy():
                current_song = get_rand_new_song(music_dict,current_playlist, current_song)
                start_song(current_playlist, current_song)
                CHANGE_SONG_FLAG = False
    # if power state is off, power off outputs and stop music
    else:
        mixer.music.stop()
        PREV_POWER_STATE = False
        CHANGE_SONG_FLAG = False
        CHANGE_PLAYLIST_FLAG = False
    return PREV_POWER_STATE, CHANGE_SONG_FLAG, CHANGE_PLAYLIST_FLAG, current_playlist, current_song
