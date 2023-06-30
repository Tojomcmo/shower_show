import random
from pygame import mixer
from os import listdir

def create_music_dictionary(library_name:str):
    # This function recieves a directory of playlists (single heirarchy)
    # and returns a dictionary with key of playlist name and value of the
    # requisite list of song names
    playlist_names_list = listdir(library_name)
    music_dict = {}
    for playlist in playlist_names_list:
        song_names_list = listdir(library_name + '/' + playlist)
        music_dict[playlist] = song_names_list
    return music_dict

def initialize_playlist_and_song(music_dict:dict):
    # This function recieves a music dictionary as defined in 
    # create_music_dictionary, and populates a current playlist,
    # current song, and initializes a list of played songs with
    # the current song.
    current_playlist = next(iter(music_dict))
    current_song = random.choice(music_dict[current_playlist])
    played_song_list = [current_song]
    return current_playlist, current_song, played_song_list

def get_next_playlist_and_first_song(music_dict:dict, current_playlist:str):
    # This function selects the next playlist in the dictionary and
    # picks the first song from the new playlist as the current song.
    # The function also clears and repopulates the played song list with
    # the new song.
    music_dict_iter = iter(music_dict)
    played_song_list = []
    for key in music_dict_iter:
        if key == current_playlist:
            temp_playlist = next(music_dict_iter, None)     
            if temp_playlist == None:
                next_playlist = next(iter(music_dict))
            else:
                next_playlist = temp_playlist
    next_song = music_dict[next_playlist][0]
    played_song_list.append(next_song)
    return next_playlist, next_song, played_song_list

def get_rand_new_song(music_dict:dict, current_playlist:str, current_song:str):
    # This function selects a random new song from the supplied playlist regardless
    # of previously played songs from the playlist
    song_name_list = music_dict[current_playlist][:]
    if len(song_name_list) == 1:
        next_song = current_song
    else:
        song_name_list.remove(current_song)
        next_song = random.choice(song_name_list)
    return next_song

def get_rand_unplayed_new_song(music_dict:dict, current_playlist:str, played_song_list:list):
    # This function selects a random new song from the supplied playlist
    # that does not overlap with a supplied list of already played songs.
    # The function then updates the list of played songs with the newly
    # selected song.
    song_name_list = music_dict[current_playlist][:]
    played_song_list = played_song_list[:]
    if len(song_name_list) == 1:
        next_song = song_name_list[0]
    else:
        if len(played_song_list) == len(song_name_list):
            next_song = random.choice(song_name_list)
            played_song_list.clear()
            played_song_list.append(next_song)
        else:
            song_name_list_reduced = [ele for ele in song_name_list if ele not in played_song_list]
            next_song = random.choice(song_name_list_reduced)
            played_song_list.append(next_song)
        return next_song, played_song_list

def get_song_path(music_library:str, current_playlist:str, current_song:str):
    # This function concatenates music strings to create a valid call path
    # for mixer music load.
    return (music_library + '/'+ current_playlist + '/' + current_song)

def start_song(music_library:str, current_playlist:str, current_song:str):
    mixer.music.stop()
    mixer.music.load(get_song_path(music_library, current_playlist, current_song))
    mixer.music.play()
    return

def set_song_state(POWER_STATE:bool,
                   PREV_POWER_STATE:bool,
                   CHANGE_SONG_FLAG:bool,
                   CHANGE_PLAYLIST_FLAG:bool,
                   music_dict:dict,
                   music_library:str,
                   current_playlist:str,
                   current_song:str,
                   played_song_list:list):
    # power state logic
    if POWER_STATE:
        # if this is the initial state change to on, begin song
        if not PREV_POWER_STATE:
            current_playlist, current_song, played_song_list = get_next_playlist_and_first_song(music_dict, current_playlist)
            start_song(music_library, current_playlist, current_song)
            CHANGE_SONG_FLAG = False
            CHANGE_PLAYLIST_FLAG = False
            PREV_POWER_STATE = True
        # if the state has been on, check song state
        else:
            # if new playlist flag is true, pick a new playlist and new song and play
            if CHANGE_PLAYLIST_FLAG:
                current_playlist, current_song, played_song_list = get_next_playlist_and_first_song(music_dict, current_playlist)
                start_song(music_library, current_playlist, current_song)
                CHANGE_PLAYLIST_FLAG = False
                CHANGE_SONG_FLAG = False
            # if new song flag is true or if song has ended, pick new song and play
            if CHANGE_SONG_FLAG or not mixer.music.get_busy():
                current_song, played_song_list = get_rand_unplayed_new_song(music_dict, current_playlist, played_song_list)
                start_song(music_library, current_playlist, current_song)
                CHANGE_SONG_FLAG = False
    # if power state is off, stop music and clear flags
    else:
        mixer.music.stop()
        PREV_POWER_STATE = False
        CHANGE_SONG_FLAG = False
        CHANGE_PLAYLIST_FLAG = False
    return PREV_POWER_STATE, CHANGE_SONG_FLAG, CHANGE_PLAYLIST_FLAG, current_playlist, current_song
