import random
import time
from pygame import mixer
from os import listdir
import music_control_funcs as mcf

if __name__ == "__main__":


    music_dict = mcf.create_music_dictionaries('playlist_dir')
    current_playlist, current_song = mcf.initialize_playlist_and_song(music_dict)
    current_playlist, current_song = mcf.get_next_playlist_and_first_song(music_dict, current_playlist)
    current_song     = mcf.get_rand_new_song(music_dict,current_playlist, current_song)
    current_song     = mcf.get_rand_new_song(music_dict,current_playlist, current_song)  
    song_path        = mcf.get_song_path(current_playlist, current_song)

    print(current_playlist + "   " + current_song)
    print(song_path)
    # initiate music mixer
    # mixer.init()
    # mixer.music.load(song_str)
    # mixer.music.set_volume(1.0)

