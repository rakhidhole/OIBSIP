import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("User:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't get that.")
    except sr.RequestError:
        speak("Sorry, I'm having trouble connecting to the service.")
    return ""

def respond_to_command(command):
    if "hello" in command:
        speak("Hello! How can I help you?")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
    elif "date" in command:
        today = datetime.datetime.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")
    elif "search" in command:
        speak("What should I search for?")
        query = listen_command()
        if query:
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            speak(f"Here are the results for {query}")
    elif "stop" in command or "exit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I can't do that yet.")

def main():
    speak("Voice Assistant started. Say something.")
    while True:
        command = listen_command()
        if command:
            respond_to_command(command)

if __name__ == "__main__":
    main()
