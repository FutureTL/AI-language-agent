import pyttsx3
engine = pyttsx3.init()

#Rate
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        # printing current voice rate
engine.setProperty('rate', 150)     # setting up new voice rate

#volume
volume = engine.getProperty('volume')   # getting to know current volume level (min=0 and max=1)
print (volume)                          # printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between

#voice
voices = engine.getProperty('voices')       # getting details of current voices
engine.setProperty('voice', voices[0].id)  # changing index, changes voices. 1 for
# engine.setProperty('voice', voices[1].id)   # changing index, changes voices. 0 for male

def speak(text):
    
    print("AI speaking: ", text)
    engine.say(text)
    engine.runAndWait()
   