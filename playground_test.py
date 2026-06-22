import board
import digitalio

# Access physical GPIO pins on the Raspberry Pi header
pin = digitalio.DigitalInOut(board.D4)
print("Blinka is successfully communicating with Raspberry Pi hardware!")


import time
import neopixel

# The 10 built-in NeoPixels are assigned to board.NEOPIXEL
NUM_PIXELS = 10

# Initialize the LED ring
# brightness=0.2 keeps it at a comfortable, low power consumption level (Max is 1.0)
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=0.2, auto_write=True)

print("Starting the LED color cycle loop. Press Ctrl+C to exit.")

try:
    while True:
        # 1. Turn all LEDs RED (Red, Green, Blue values range from 0 to 255)
        print("Setting LEDs to Red")
        pixels.fill((255, 0, 0))
        time.sleep(1.0)

        # 2. Turn all LEDs GREEN
        print("Setting LEDs to Green")
        pixels.fill((0, 255, 0))
        time.sleep(1.0)

        # 3. Turn all LEDs BLUE
        print("Setting LEDs to Blue")
        pixels.fill((0, 0, 255))
        time.sleep(1.0)

except KeyboardInterrupt:
    # Safely clear the lights if you press Ctrl+C in the terminal
    pixels.fill((0, 0, 0))
    print("\nLoop stopped. LEDs turned off.")
