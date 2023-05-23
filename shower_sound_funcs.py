import pygame
import gpiozero as gpio
from os import listdir


#define GPIO
on_off_button      = gpio.Button("GPIO17")
song_change_button = gpio.Button("GPIO18")
shower_relay       = gpio.DigitalOutputDevice("GPIO27")
amp_relay          = gpio.DigitalOutputDevice("GPIO22")
disco_relay        = gpio.DigitalOutputDevice("GPIO23")


# open directory of songs
files = listdir("song_list")
print(files)