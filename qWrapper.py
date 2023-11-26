# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 12:15:02 2023

@author: fjodo
"""
from PIL import Image
from openai import OpenAI #Remember to set-up your own API_KEY!!!
import requests
client = OpenAI()
response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What’s in this image?"},
        {
          "type": "image_url",
          "image_url": {
            "url": "https://i.postimg.cc/T1QBQLzR/20220105-080746.jpg", #obviously if you intend to run this code, upload your own image!!
            "detail": "high"
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

#print(response.choices[0].message.content)

#The GPT-4V output will surely have excessive text, but Dall-E can work with that anyway
#Since we are trying to recreate the Vatventure Creator functionlaity we need this too
cat_holder = " Now turn it into a Catventurer with some similarity!"

sigma = response.choices[0].message.content + cat_holder

print(sigma)

response = client.images.generate(
  model="dall-e-3",
  prompt=sigma,
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url

# Get the image content from the URL
response = requests.get(image_url)

# Check if the request was successful
if response.status_code == 200:
    # Open a file in binary write mode
    with open("output_image3.png", "wb") as file:
        # Write the content of the image to the file
        file.write(response.content)
else:
    print("Failed to retrieve the image.")
    
image1 = Image.open('output_image3.png')
image2 = Image.open('calendar_grid.png') #I have generated the calendar beforehand

# Calculate the size of the new image
new_width = max(image1.width, image2.width)
new_height = image1.height + image2.height

# Create a new image with the calculated size
merged_image = Image.new('RGBA', (new_width, new_height))

# Paste the first image at the top
merged_image.paste(image1, (0, 0))

# Paste the second image below the first image
merged_image.paste(image2, (0, image1.height))

# Save the merged image
merged_image.save('merged_image.png')