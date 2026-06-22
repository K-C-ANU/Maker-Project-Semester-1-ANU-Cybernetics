# Moondream set up
import moondream as md
from PIL import Image

# Initialize with your API key
model = md.vl(api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXlfaWQiOiI5ZWNlMWNiMC1jM2M3LTQwMDMtOWFjZS1hY2Y3YmFlZTZmNTEiLCJvcmdfaWQiOiJybHpONGdWNzdvZUpyc2h1MURqeUJFUWRsSnNJdFNUMSIsImlhdCI6MTc2MDkyNzc2NiwidmVyIjoxfQ.KbUoAxm4BZqI3np5ji9exTccdgHFkgbpf74fTIz5AII')


#model = md.vl(model="moondream")
image = Image.open("/home/kacooper/Desktop/images/boydressedassoldiercanva.png")

#print(model.caption(image).caption)


# Example: Ask a question about the image
answer = model.query(image, "is this a soldier? Answer either with TRUE or FALSE do not elaborate. You are giving us a simple one word answer and nothing else.")["answer"]
print(answer)


