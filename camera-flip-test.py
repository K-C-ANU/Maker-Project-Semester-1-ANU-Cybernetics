from PIL import Image

from picamera2 import Picamera2

# Open your image file
img = Image.open('your_image.jpg')


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


# Flip the image vertically
flipped_img = imgage.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

# Save or display the result
flipped_img.save('vertical_flip.jpg')
flipped_img.show()


