# Moondream set up
import moondream as md
from PIL import Image

# Initialize with your API key
model = md.vl(api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI5ZWNlMWNiMC1jM2M3LTQwMDMtOWFjZS1hY2Y3YmFlZTZmNTEiLCJvcmdfaWQiOiJybHpONGdWNzdvZUpyc2h1MURqeUJFUWRsSnNJdFNUMSIsImlhdCI6MTc2MDkyNzc2NiwidmVyIjoxfQ.KbUoAxm4BZqI3np5ji9exTccdgHFkgbpf74fTIz5AII')


#set for camera to take photo
from picamera2 import Picamera2

#1. Initialise the camera
camera = Picamera2()
#2 Start the camera preview 
camera.start()




#3  Take the picture and save it in to directory
# camera.capture_file("PYTHON_TEST.JPG")

# 3' Capture image/photo and save it into a variable
my_photo = camera.capture_array("main")

# 3'' Convert format for moondream
my_pil_photo = Image.fromarray(my_photo, mode="RGB")
#4 Stop the camera and free up system resources
camera.stop()

print("Photo Taken")


# Example: Ask a question about the image
encoded_photo = model.encode_image(my_pil_photo)
answer = model.query(encoded_photo, "is this a a soldier? Give me a confidence score.")["answer"]
print("Answer:", answer) 
