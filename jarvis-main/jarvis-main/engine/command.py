import pyttsx3
import speech_recognition as sr
import eel
import time
import datetime
import webbrowser
import requests
import openai

# Set up OpenAI API
openai.api_key = "YOUR_OPENAI_API_KEY"

def speak(text):
    """Speak the given text"""
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():
    """Take a voice command from the user"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)
    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
    return query.lower()

def get_weather(city):
    """Get the weather for a given city"""
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"]!= "404":
        main = data["main"]
        temperature = main["temp"]
        humidity = main["humidity"]
        pressure = main["pressure"]
        weather_description = data["weather"][0]["description"]
        return f"Weather in {city}: Temperature={temperature}K, Humidity={humidity}%, Pressure={pressure}Pa, Description={weather_description}"
    else:
        return "City Not Found"

def chat_with_gpt(query):
    """Chat with the GPT model"""
    response = openai.Completion.create(
        engine="davinci",
        prompt=query,
        max_tokens=1024,
        temperature=0.5,
    )
    return response.choices[0].text

@eel.expose
def allCommands(message=1):
    """Handle all voice commands"""
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:
        if "open" in query:
            if "youtube" in query:
                speak("Opening YouTube")
                webbrowser.open("https://youtube.com/")
            elif "google" in query:
                speak("Opening Google")
                webbrowser.open("https://www.google.com")
            elif "weather" in query:
                speak("Opening weather forecasting")
                webbrowser.open("https://www.weather.com/")
            else:
                # Add your custom logic here
                pass
        elif "date" in query:
            today = datetime.date.today()
            speak(f"Today's date is {today}")
        elif "day" in query:
            today = datetime.date.today()
            speak(f"Today is {today.strftime('%A')}")
        elif "time" in query:
            now = datetime.datetime.now()
            speak(f"Current time is {now.strftime('%I:%M %p')}")
        elif "weather" in query:
            city = query.split("in ")[1]
            weather_info = get_weather(city)
            speak(weather_info)
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, I didn't understand that.")