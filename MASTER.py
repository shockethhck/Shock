import os
import speech_recognition as sr
import pyttsx3
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google import genai

# 1. SETUP - Copy your keys and IDs here
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
GEMINI_API_KEY = "YOUR_API_KEY_HERE"

# Initialize the "Brain"
client = genai.Client(api_key=GEMINI_API_KEY)
chat_session = client.chats.create(model="gemini-2.0-flash")

# 2. YOUTUBE LOGIC (From your project.txt)
def get_youtube_service():
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    return build('youtube', 'v3', credentials=credentials)

def play_on_youtube(service, song_name):
    request = service.search().list(q=song_name, part='snippet', type='video', maxResults=1)
    response = request.execute()
    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        webbrowser.open(f"https://www.youtube.com/watch?v={video_id}")

# 3. VOICE LOGIC (From your support files)
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio).lower()
        except:
            return ""

# 4. THE MAIN LOOP (The "Router")
if __name__ == "__main__":
    youtube_service = get_youtube_service()
    speak("Assistant is ready.")
    
    while True:
        query = listen()
        
        if 'play' in query:
            song = query.replace('play', '').strip()
            play_on_youtube(youtube_service, song)
        elif 'stop' in query:
            break
        elif query: # If it's anything else, ask Gemini
            response = chat_session.send_message(query)
            speak(response.text)
