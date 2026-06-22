from PIL import Image
import moondream as md

# Initialize with your API key
model = md.vl(api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI5ZWNlMWNiMC1jM2M3LTQwMDMtOWFjZS1hY2Y3YmFlZTZmNTEiLCJvcmdfaWQiOiJybHpONGdWNzdvZUpyc2h1MURqeUJFUWRsSnNJdFNUMSIsImlhdCI6MTc2MDkyNzc2NiwidmVyIjoxfQ.KbUoAxm4BZqI3np5ji9exTccdgHFkgbpf74fTIz5AII')


image_path = "/home/kacooper/Desktop/PYTHON_TEST.JPG"

# Open the image using PIL
image = Image.open(image_path)

# Encode and query
encoded_image = model.encode_image(image)
answer = model.query(encoded_image, "What is in this picture?")["answer"]
print(answer)
