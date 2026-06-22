import gpiod
import time

# Here's the pin diagram:
# https://cdn.shopify.com/s/files/1/0195/1344/2404/files/pi-5-diagram.jpg?v=1762784407 


# Setup GPIO control on GPIO 2 (which is pin 3 see the diagram above)
chip = gpiod.Chip('gpiochip4')
line = chip.get_line(2)
line.request(consumer='led', type=gpiod.LINE_REQ_DIR_OUT)


# Now blink the LED on and off.
line.set_value(1)
time.sleep(2)
line.set_value(0)
time.sleep(2)
line.set_value(1)
time.sleep(2)
line.set_value(0)
time.sleep(2)
line.set_value(1)
time.sleep(2)
line.set_value(0)
time.sleep(2)
line.set_value(1)
time.sleep(2)
line.set_value(0)
time.sleep(2)
line.set_value(1)
time.sleep(2)
line.set_value(0)
time.sleep(2)
line.set_value(1)
time.sleep(2)
line.set_value(0)
time.sleep(2)
line.set_value(1)

line.release()

