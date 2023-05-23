from gpiozero import LED, Button
from signal import pause
 
led = LED(17)
button = Button(3)
 
button.when_pressed = print("on")
button.when_released = print("off")
 
pause()