from gtts import gTTS
#import os
import pygame
import sys

# Read the input file containing the text
input_file = sys.argv[1]
with open(input_file, 'r') as file:
    text = file.read()

# Create a gTTS object and save the audio as output.mp3
object = gTTS(text=text, lang='en', slow=False)
object.save('output.mp3')

# Initialize pygame
pygame.init()

# Load the audio file
pygame.mixer.music.load('output.mp3')

# Play the audio file
pygame.mixer.music.play()

# Wait until the audio finishes playing
while pygame.mixer.music.get_busy():
    continue

# Clean up resources
pygame.mixer.quit()
