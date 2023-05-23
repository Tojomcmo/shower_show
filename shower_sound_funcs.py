import pygame
import gpiozero as gpio
from os import listdir

# define GPIO pins
in_btn_on_off        = 7
in_btn_song_change   = 11
out_shower_relay     = 12
out_amp_relay        = 13
out_disco_relay      = 15

#set all GPIO outputs to low
on_off_button      = gpio.Button(in_btn_on_off)
song_change_button = gpio.Button(in_btn_song_change)
shower_relay       = gpio.DigitalOutputDevice(out_shower_relay)
amp_relay          = gpio.DigitalOutputDevice(out_amp_relay)
disco_relay        = gpio.DigitalOutputDevice(out_disco_relay)


# open directory of songs
files = listdir("song_list")
print(files)