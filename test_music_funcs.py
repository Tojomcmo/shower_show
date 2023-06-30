import random
import time
from pygame import mixer
from os import listdir
import music_control_funcs as mcf

if __name__ == "__main__":

    POWER_BTN_STATE      = True
    PREV_POWER_BTN_STATE = False
    CHANGE_SONG_FLAG     = True
    CHANGE_PLAYLIST_FLAG = True

    music_dict = mcf.create_music_dictionary('playlist_dir')
    current_playlist, current_song, played_song_list = mcf.initialize_playlist_and_song(music_dict)
    current_playlist, current_song, played_song_list = mcf.get_next_playlist_and_first_song(music_dict, current_playlist)
    current_song     = mcf.get_rand_new_song(music_dict,current_playlist, current_song)
    current_song, played_song_list = mcf.get_rand_unplayed_new_song(music_dict,current_playlist, played_song_list)
    current_song, played_song_list = mcf.get_rand_unplayed_new_song(music_dict,current_playlist, played_song_list)   
    current_song, played_song_list = mcf.get_rand_unplayed_new_song(music_dict,current_playlist, played_song_list)
    song_path        = mcf.get_song_path(current_playlist, current_song)





    print(song_path)

