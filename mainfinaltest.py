import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
import cv2
from easygui import *
import os
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string

def recognize_speech():  # Function to recognize speech and display ISL
    r = sr.Recognizer()
    isl_gif = [  # List of phrases for Indian Sign Language (ISL)
        'any questions', 'are you angry', 'are you busy', 'are you hungry', 'be careful',
        'did you finish homework', 'do you have money',
        'do you want something to drink','do you watch TV', 'dont worry', 'flower is beautiful',
        'good afternoon', 'good morning', 'good question', 'happy journey',
        'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing', 
        'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
        'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker',
        'my name is john', 'nice to meet you', 'open the door', 'please call me later',
        'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime', 'shall I help you',
        'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was traffic jam', 'wait I am thinking',
        'what are you doing', 'what is the problem', 'what is todays date', 'what is your father do', 'what is your job',
        'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
        'where is the bathroom', 'where is the police station', 'you are wrong','address','agra','ahemdabad', 'all', 'april', 'assam', 'august', 'australia', 'badoda', 'banana', 'banaras', 'banglore',
        'bihar','bihar','bridge','cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 'coconut', 'crocodile','dasara',
        'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'febuary', 'friday', 'fruits', 'glass', 'grapes', 'gujrat', 'hello',
        'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'july', 'karnataka', 'kerala', 'krishna', 'litre', 'mango',
        'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station',
        'post office', 'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'southafrica',
        'story', 'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa', 'village',
        'voice', 'wednesday', 'weight','please wait for sometime','what is your mobile number','what are you doing','are you busy']
        
    arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
           's','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        while True:  # Main loop for speech recognition
            print('Say something...')  
            audio = r.listen(source)
            try:
                a = r.recognize_google(audio)  # Use Google Web Speech API for better accuracy
                print("you said " + a.lower())
                for c in string.punctuation:
                    a = a.replace(c, "")
                    
                if a.lower() in ['goodbye', 'good bye', 'bye']:  # Check for exit commands
                    print("oops! Time To say good bye")
                    break
                
                elif a.lower() in isl_gif:
                    class ImageLabel(tk.Label):
                        def load(self, im):
                            if isinstance(im, str):
                                im = Image.open(im)
                            self.loc = 0
                            self.frames = []

                            try:
                                for i in count(1):
                                    self.frames.append(ImageTk.PhotoImage(im.copy()))
                                    im.seek(i)
                            except EOFError:
                                pass

                            try:
                                self.delay = im.info['duration']
                            except:
                                self.delay = 100

                            if len(self.frames) == 1:
                                self.config(image=self.frames[0])
                            else:
                                self.next_frame()  # Start the animation by calling next_frame once

                        def unload(self):
                            self.config(image=None)
                            self.frames = None

                        def next_frame(self):
                            if self.frames:
                                self.loc += 1
                                self.loc %= len(self.frames)
                                self.config(image=self.frames[self.loc])
                                self.after(self.delay, self.next_frame)  # Schedule the next frame update

                    root = tk.Tk()  # Create the main window for displaying GIFs
                    window_width = 320  # Set desired width
                    window_height = 180  # Set desired height
                    root.geometry(f"{window_width}x{window_height}")  # Set window size

                    lbl = ImageLabel(root)
                    lbl.pack()
                    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get main1.py directory
                    gif_path = os.path.join(base_dir, "ISL_Gifs", f"{a.lower()}.gif")  # Construct full path
                    im = Image.open(gif_path)
                    # Remove resizing to maintain original dimensions
                    lbl.load(im)

                    root.mainloop()
                else:
                    for i in range(len(a)):
                        if a[i] in arr:
                            base_dir = os.path.dirname(os.path.abspath(__file__))  # Get main1.py directory
                            ImageAddress = os.path.join(base_dir, "letters", f"{a[i]}.jpg")  # Construct full path

                            try:
                                ImageItself = Image.open(ImageAddress)
                                ImageNumpyFormat = np.asarray(ImageItself)
                                plt.imshow(ImageNumpyFormat)
                                plt.draw()
                                plt.pause(0.8)
                            except FileNotFoundError:
                                print(f"Image not found: {ImageAddress}")  # Error message for missing image
                            except Exception as e:
                                print(f"An unexpected error occurred while loading the image: {e}")  # General error handling
                        else:
                            continue

            except sr.UnknownValueError:
                print("Could not understand audio")  # Specific error message for unrecognized audio
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")  # Specific error message for request issues
            except Exception as e:
                print(f"An unexpected error occurred: {e}")  # Capture any unexpected errors
            finally:
                plt.close()

while True:
    image = os.path.join(os.path.dirname(__file__), "signlang.png")
    print(f"Attempting to load image from: {os.path.abspath(image)}")  # Print the absolute path for debugging
    try:
        signlang_image = Image.open(image)  # Attempt to load the sign language image
    except FileNotFoundError:
        print(f"Image not found: {image}")  # Error message for missing image
    except Exception as e:
        print(f"An unexpected error occurred while loading the image: {e}")  # General error handling

    msg = "HEARING IMPAIRMENT ASSISTANT"
    choices = ["Live Voice", "All Done!"] 
    reply = buttonbox(msg, image=image, choices=choices)
    if reply == choices[0]:
        recognize_speech()  # Call the speech recognition function
    if reply == choices[1]:
        quit()
