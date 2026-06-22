import io
import moondream as md
from PIL import Image
from picamera2 import Picamera2

# 1. Initialise the Moondream model
# (Ensure your path matches your local .mf model version)
model = md.vl(api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI5ZWNlMWNiMC1jM2M3LTQwMDMtOWFjZS1hY2Y3YmFlZTZmNTEiLCJvcmdfaWQiOiJybHpONGdWNzdvZUpyc2h1MURqeUJFUWRsSnNJdFNUMSIsImlhdCI6MTc2MDkyNzc2NiwidmVyIjoxfQ.KbUoAxm4BZqI3np5ji9exTccdgHFkgbpf74fTIz5AII')

# 2. Initialise the Raspberry Pi Camera
picam2 = Picamera2()
picam2.start()

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
answer = model.query(encoded_image, "is this a soldier? Give me an answer and a confidence score.")["answer"]

print("\nMoondream Answer:")
print(answer)
