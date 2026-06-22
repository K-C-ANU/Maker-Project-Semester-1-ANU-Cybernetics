import io
import moondream as md
from PIL import Image
from picamera2 import Picamera2
import gpiod
import time

### SETUP

# 1. Initialise the Moondream model
# (Ensure your path matches your local .mf model version)
model = md.vl(api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI5ZWNlMWNiMC1jM2M3LTQwMDMtOWFjZS1hY2Y3YmFlZTZmNTEiLCJvcmdfaWQiOiJybHpONGdWNzdvZUpyc2h1MURqeUJFUWRsSnNJdFNUMSIsImlhdCI6MTc2MDkyNzc2NiwidmVyIjoxfQ.KbUoAxm4BZqI3np5ji9exTccdgHFkgbpf74fTIz5AII')

# 2. Initialise the Raspberry Pi Camera
picam2 = Picamera2()
picam2.start()

# Setup GPIO control on GPIO 2 (which is pin 3 see the diagram above)
chip = gpiod.Chip('gpiochip4')
red = chip.get_line(2)
green = chip.get_line(3)
red.request(consumer='led', type=gpiod.LINE_REQ_DIR_OUT)
green.request(consumer='led', type=gpiod.LINE_REQ_DIR_OUT)

print("Blinking the lights...")
red.set_value(1)
green.set_value(1)
time.sleep(0.5)
red.set_value(0)
green.set_value(0)
time.sleep(0.5)
red.set_value(1)
green.set_value(1)
time.sleep(0.5)
print("Lights have been blinked.")

### TEST WITH THE CAMERA

# 3. Capture a picture directly into RAM using a BytesIO stream
stream = io.BytesIO()
picam2.capture_file(stream, format="jpeg")
stream.seek(0) # Rewind the stream to the beginning to read it

# 4. Convert the captured stream directly to a PIL image and force RGB
image = Image.open(stream).convert("RGB")

# 5. Stop the camera to free up GPU/system memory resources
picam2.stop()

# 6. Process the image with Moondream
print("Encoding image and querying Moondream...")
encoded_image = model.encode_image(image)
answer = model.query(image, "is this a soldier? Answer either with TRUE or FALSE do not elaborate. You are giving us a simple one word answer and nothing else.")["answer"]

if answer == 'TRUE':
	print("That's a soldier!")
	red.set_value(0)
	green.set_value(1)
	time.sleep(5)
	red.set_value(0)
	green.set_value(0)
elif answer == 'FALSE':
	print("That's NOT a soldier!")
	red.set_value(1)
	green.set_value(0)
	time.sleep(5)
	red.set_value(0)
	green.set_value(0)
else:
	print("Moondream did something strange.")
	red.set_value(1)
	green.set_value(0)
	time.sleep(5)
	red.set_value(0)
	green.set_value(0)

print("\nMoondream Answer:")
print(answer)


### TEST WITH AN IMAGE THAT IS A SOLDIER

print("testing with an image of a soldier in the bush with a grenade...")

#model = md.vl(model="moondream")
image = Image.open("/home/kacooper/Desktop/images/soldierinbushwithgrenade.png")

# Example: Ask a question about the image
answer = model.query(image, "is this a soldier? Answer either with TRUE or FALSE do not elaborate. You are giving us a simple one word answer and nothing else.")["answer"]
print("Answer:", answer)

if answer == 'TRUE':
	print("That's a soldier!")
	red.set_value(0)
	green.set_value(1)
	time.sleep(5)
	red.set_value(0)
	green.set_value(0)
elif answer == 'FALSE':
	print("That's NOT a soldier!")
	red.set_value(1)
	green.set_value(0)
	time.sleep(5)
	red.set_value(0)
	green.set_value(0)
else:
	print("Moondream did something strange.")
	red.set_value(1)
	green.set_value(0)
	time.sleep(5)
	red.set_value(0)
	green.set_value(0)

### TEST WITH AN IMAGE THAT IS <<NOT>> A SOLDIER

print("testing with an image of a farmer on a foggy day...")

#model = md.vl(model="moondream")
image = Image.open("/home/kacooper/Desktop/images/farmerfoggydaycanva.png")

# Example: Ask a question about the image
answer = model.query(image, "is this a soldier? Answer either with TRUE or FALSE do not elaborate. You are giving us a simple one word answer and nothing else.")["answer"]
print("Answer:", answer)

if answer == 'TRUE':
	print("That's a soldier!")
	red.set_value(0)
	green.set_value(1)
	time.sleep(5)
	red.set_value(0)
	green.set_value(0)
elif answer == 'FALSE':
	print("That's NOT a soldier!")
	red.set_value(1)
	green.set_value(0)
	time.sleep(5)
	red.set_value(0)
	green.set_value(0)
else:
	print("Moondream did something strange.")
	red.set_value(1)
	green.set_value(0)
	time.sleep(5)
	red.set_value(0)
	green.set_value(0)
