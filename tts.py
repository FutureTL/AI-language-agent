def speak(text):
    import pyttsx3

    engine = pyttsx3.init()  # 🔥 re-init every time

    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    print("AI speaking:")

    engine.say(text)
    engine.runAndWait()
    engine.stop()