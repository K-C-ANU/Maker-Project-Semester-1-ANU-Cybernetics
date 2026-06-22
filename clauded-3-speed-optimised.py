import io
import moondream as md
from PIL import Image
from picamera2 import Picamera2
import gpiod
import time
import threading
import concurrent.futures

### CONFIGURATION

MOONDREAM_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI5ZWNlMWNiMC1jM2M3LTQwMDMtOWFjZS1hY2Y3YmFlZTZmNTEiLCJvcmdfaWQiOiJybHpONGdWNzdvZUpyc2h1MURqeUJFUWRsSnNJdFNUMSIsImlhdCI6MTc2MDkyNzc2NiwidmVyIjoxfQ.KbUoAxm4BZqI3np5ji9exTccdgHFkgbpf74fTIz5AII'
MOONDREAM_TIMEOUT = 30  # seconds
CAPTURE_RESOLUTION = (640, 480)  # Lower = faster. Try (320, 240) for max speed.
PROMPT = (
    "is this a soldier? Answer either with TRUE or FALSE "
    "do not elaborate. You are giving us a simple one word answer "
    "and nothing else."
)
RESULT_DISPLAY_SECONDS = 5

### SETUP

# Moondream vision model
model = md.vl(api_key=MOONDREAM_API_KEY)

# Raspberry Pi Camera — configured at a lower resolution for speed
picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": CAPTURE_RESOLUTION})
picam2.configure(config)
picam2.start()

# GPIO LEDs (red on GPIO 2 / pin 3, green on GPIO 3 / pin 5)
# Wiring diagram: https://cdn.shopify.com/s/files/1/0195/1344/2404/files/pi-5-diagram.jpg?v=1762784407
chip = gpiod.Chip('gpiochip4')
red = chip.get_line(2)
green = chip.get_line(3)
red.request(consumer='led', type=gpiod.LINE_REQ_DIR_OUT)
green.request(consumer='led', type=gpiod.LINE_REQ_DIR_OUT)


### HELPER FUNCTIONS

def set_leds(r, g):
    """Set red and green LED states."""
    red.set_value(r)
    green.set_value(g)


def flash_leds(r, g, duration=RESULT_DISPLAY_SECONDS):
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


def blink_while_waiting(stop_event, interval=0.15):
    """Rapidly blink both LEDs until stop_event is set."""
    while not stop_event.is_set():
        set_leds(1, 1)
        if stop_event.wait(interval):
            break
        set_leds(0, 0)
        if stop_event.wait(interval):
            break
    set_leds(0, 0)


def capture_image():
    """Capture a JPEG from the Pi camera and return it as an RGB PIL Image."""
    stream = io.BytesIO()
    picam2.capture_file(stream, format="jpeg")
    stream.seek(0)
    return Image.open(stream).convert("RGB")


def query_moondream(image, prompt, timeout=MOONDREAM_TIMEOUT):
    """Query Moondream with a timeout. Returns the answer string or None on failure."""
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

print(f"Starting up (capture resolution: {CAPTURE_RESOLUTION[0]}x{CAPTURE_RESOLUTION[1]})...")
blink_leds()

try:
    while True:
        # Steady hold while capturing
        print("\nCapturing image...")
        set_leds(1, 1)
        start = time.monotonic()
        image = capture_image()
        capture_ms = (time.monotonic() - start) * 1000
        set_leds(0, 0)
        print(f"  Captured {image.size[0]}x{image.size[1]} in {capture_ms:.0f}ms")
        time.sleep(0.3)

        # Rapid blink while Moondream is thinking
        print("Querying Moondream...")
        stop_event = threading.Event()
        blink_thread = threading.Thread(target=blink_while_waiting, args=(stop_event,))
        blink_thread.start()

        start = time.monotonic()
        answer = query_moondream(image, PROMPT)
        query_ms = (time.monotonic() - start) * 1000
        print(f"  Response in {query_ms:.0f}ms")

        stop_event.set()
        blink_thread.join()
        time.sleep(0.3)

        # Result indicator
        if answer == 'TRUE':
            print("That's a soldier!")
            flash_leds(0, 1)
        elif answer == 'FALSE':
            print("That's NOT a soldier!")
            flash_leds(1, 0)
        else:
            print(f"Unexpected response: {answer}")
            blink_leds(times=3, interval=0.3)

        time.sleep(1)

except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    set_leds(0, 0)
    picam2.stop()
