import gpiod
import time

# Here's the pin diagram:
# https://cdn.shopify.com/s/files/1/0195/1344/2404/files/pi-5-diagram.jpg?v=1762784407 


# Setup GPIO control on GPIO 2 (which is pin 3 see the diagram above)
chip = gpiod.Chip('gpiochip4')
red = chip.get_line(2)
green = chip.get_line(3)
red.request(consumer='led', type=gpiod.LINE_REQ_DIR_OUT)
green.request(consumer='led', type=gpiod.LINE_REQ_DIR_OUT)



# Blink the LEDs together
red.set_value(1)
green.set_value(1)
time.sleep(2)
red.set_value(0)
green.set_value(0)
time.sleep(2)
red.set_value(1)
green.set_value(1)
time.sleep(2)

# Now alternate the LEDs on and off.
red.set_value(1)
green.set_value(0)
time.sleep(2)
red.set_value(0)
green.set_value(1)
time.sleep(2)
red.set_value(0)
green.set_value(1)
time.sleep(2)

red.release()
green.release()
