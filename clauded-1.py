import io
import moondream as md
from PIL import Image
from picamera2 import Picamera2
import gpiod
import time

### SETUP

model = md.vl(api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI5ZWNlMWNiMC1jM2M3LTQwMDMtOWFjZS1hY2Y3YmFlZTZmNTEiLCJvcmdfaWQiOiJybHpONGdWNzdvZUpyc2h1MURqeUJFUWRsSnNJdFNUMSIsImlhdCI6MTc2MDkyNzc2NiwidmVyIjoxfQ.KbUoAxm4BZqI3np5ji9exTccdgHFkgbpf74fTIz5AII')

picam2 = Picamera2()
picam2.start()

chip = gpiod.Chip('gpiochip4')
red = chip.get_line(2)
green = chip.get_line(3)
red.request(consumer='led', type=gpiod.LINE_REQ_DIR_OUT)
green.request(consumer='led', type=gpiod.LINE_REQ_DIR_OUT)

MOONDREAM_TIMEOUT = 30  # seconds
PROMPT = "is this a soldier? Answer either with TRUE or FALSE do not elaborate. You are giving us a simple one word answer and nothing else."


### HELPER FUNCTIONS

def set_leds(r, g):
    """Set red and green LED states."""
    red.set_value(r)
    green.set_value(g)


def flash_leds(r, g, duration=5):
    """Turn on the specified LEDs for a duration, then switch both off."""
    set_leds(r, g)
    time.sleep(duration)
    set_leds(0, 0)


def blink_leds(times=2, interval=0.5):
    """Blink both LEDs on and off."""
    for _ in range(times):
        set_leds(1, 1)
        time.sleep(interval)
        set_leds(0, 0)
        time.sleep(interval)


def capture_image():
    """Capture a JPEG from the Pi camera and return it as an RGB PIL Image."""
    stream = io.BytesIO()
    picam2.capture_file(stream, format="jpeg")
    stream.seek(0)
    return Image.open(stream).convert("RGB")


def query_moondream(image, prompt, timeout=MOONDREAM_TIMEOUT):
    """Query Moondream with a timeout. Returns the answer string or None on failure."""
    import concurrent.futures
    encoded = model.encode_image(image)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(model.query, encoded, prompt)
        try:
            result = future.result(timeout=timeout)
            return result["answer"]
        except concurrent.futures.TimeoutError:
            print(f"Moondream timed out after {timeout}s.")
            return None
        except Exception as e:
            print(f"Moondream error: {e}")
            return None


### MAIN LOOP

print("Starting up...")
blink_leds()

try:
    while True:
        print("\nCapturing image...")
        image = capture_image()

        print("Querying Moondream...")
        answer = query_moondream(image, PROMPT)

        if answer == 'TRUE':
            print("That's a soldier!")
            flash_leds(0, 1)
        elif answer == 'FALSE':
            print("That's NOT a soldier!")
            flash_leds(1, 0)
        else:
            print(f"Unexpected response: {answer}")
            blink_leds(times=3, interval=0.3)

        time.sleep(1)  # short pause between iterations

except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    set_leds(0, 0)
    picam2.stop()
