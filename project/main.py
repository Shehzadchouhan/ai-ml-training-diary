# === Jarvis AI Assistant ===
import pyttsx3
import speech_recognition as sr
from textblob import TextBlob
import webbrowser
import os
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
import json
import time
from word2number import w2n
import sys
import re
<<<<<<< HEAD
import matplotlib.pyplot as plt


# GrowMe left here
def growme_create_goal():
    try:
        goal = input("Enter your goal (e.g., weight loss / development): ")
        target = input("Enter your target (e.g., 5kg / portfolio website): ")
        duration = int(input("Enter number of days: "))
        data = {"goal": goal, "target": target, "duration": duration, "progress": []}
        with open("growme.json", "w") as f:
            json.dump(data, f)
        print("GrowMe goal created successfully!")
    except Exception as e:
        print(f"Failed to create GrowMe goal: {e}")

def growme_update_progress():
    try:
        if not os.path.exists("growme.json"):
            print("No goal found. Please create one first.")
            return
        with open("growme.json", "r") as f:
            data = json.load(f)
        score = int(input("Enter today’s progress percentage (0–100): "))
        today = datetime.now().date().isoformat()
        data["progress"].append({"date": today, "score": score})
        with open("growme.json", "w") as f:
            json.dump(data, f)
        print("Progress updated!")
    except Exception as e:
        print(f"Failed to update progress: {e}")

def growme_show_progress():
    try:
        if not os.path.exists("growme.json"):
            print("No data found.")
            return
        with open("growme.json") as f:
            data = json.load(f)
        if not data.get("progress"):
            print("No progress entries yet.")
            return
        dates = [p["date"] for p in data["progress"]]
        scores = [p["score"] for p in data["progress"]]
        plt.figure(figsize=(6, 3))
        plt.plot(dates, scores, marker='o')
        plt.title(f"GrowMe Progress - {data.get('goal','').title()}")
        plt.xlabel("Date")
        plt.ylabel("Progress (%)")
        plt.show()
    except Exception as e:
        print(f"Failed to show progress: {e}")

class Jarvis:
    """Minimal Jarvis class wrapper so the script can instantiate and run.
    This collects existing methods (which are already written as expecting
    a `self` parameter) into the class scope by being placed before them.
    """
    def __init__(self):
        # Initialize TTS engine and recognizer; models will be created later
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.9)
        except Exception:
            self.engine = None

        self.recognizer = sr.Recognizer()
        # reasonable defaults; may be tuned for your microphone
        try:
            self.recognizer.pause_threshold = 0.8
            self.recognizer.energy_threshold = 4000
        except Exception:
            pass

        # Basic command map - you can expand this to match your original map
=======

class Jarvis:
    def __init__(self):
        # Initialize speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
        # Initialize recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.8
        self.recognizer.energy_threshold = 4000
        
        # Command mappings
>>>>>>> c1d6544cf615ef8f79cf546cce7003950de781cd
        self.command_map = {
            "open youtube": self.open_youtube,
            "open google": self.open_google,
            "open whatsapp": self.open_whatsapp,
            "open notepad": self.open_notepad,
            "open calculator": self.open_calculator,
<<<<<<< HEAD
            "open vscode": self.open_vscode,
            "tell time": self.tell_time,
            "take note": self.take_note,
            "analyse sentiment": self.analyze_sentiment,
            "predict marks": self.predict_student_marks,
            "predict house price": self.predict_house_price,
        }

        # Initialize models if the function exists
        try:
            self.initialize_models()
        except Exception:
            pass

    def speak(self, text):
        """Speak text via pyttsx3 if available, and also print it."""
        print(f"Jarvis: {text}")
        try:
            if self.engine:
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception:
            # fail silently if TTS isn't working
            pass

    def listen(self):
        """Try to listen from the microphone, fallback to typed input for testing."""
        # Prefer speech recognition via microphone, but fall back to input()
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=7)
                text = self.recognizer.recognize_google(audio)
                print(f"Heard: {text}")
                return text
        except Exception:
            # Fallback: typed input (useful when PyAudio or mic isn't configured)
            try:
                return input("You (type): ")
            except Exception:
                return None
=======
            "open vs code": self.open_vscode,
            "time": self.tell_time,
            "take note": self.take_note,
            "predict marks": self.predict_student_marks,
            "predict price": self.predict_house_price,
            "guess my mood": self.analyze_sentiment,
            "judge my feelings": self.analyze_sentiment  # Both spellings
        }
        
        # Initialize models
        self.initialize_models()

    def speak(self, text):
        """Improved text-to-speech with error handling"""
        print("Jarvis:", text)
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")

    def listen(self):
        """Improved speech recognition with better error handling"""
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                command = self.recognizer.recognize_google(audio)
                print("You:", command)
                return command.lower()
            except sr.WaitTimeoutError:
                self.speak("I didn't hear anything. Please try again.")
                return ""
            except sr.UnknownValueError:
                self.speak("Sorry, I couldn't understand that.")
                return ""
            except sr.RequestError as e:
                self.speak(f"Sorry, there was an error with the speech service: {e}")
                return ""
            except Exception as e:
                self.speak("An unexpected error occurred.")
                print(f"Error: {e}")
                return ""

    def open_youtube(self):
        webbrowser.open("https://www.youtube.com")
        self.speak("Opening YouTube")
>>>>>>> c1d6544cf615ef8f79cf546cce7003950de781cd

    def open_google(self):
        webbrowser.open("https://www.google.com")
        self.speak("Opening Google")

<<<<<<< HEAD
    def open_youtube(self):
        try:
            webbrowser.open("https://www.youtube.com")
            self.speak("Opening YouTube")
        except Exception as e:
            self.speak("Failed to open YouTube")
            print(f"Error: {e}")

=======
>>>>>>> c1d6544cf615ef8f79cf546cce7003950de781cd
    def open_whatsapp(self):
        webbrowser.open("https://web.whatsapp.com")
        self.speak("Opening WhatsApp Web")

    def open_notepad(self):
        try:
            os.system("notepad")
            self.speak("Opening Notepad")
        except Exception as e:
            self.speak("Failed to open Notepad")
            print(f"Error: {e}")

    def open_calculator(self):
        try:
            os.system("calc" if os.name == 'nt' else "gnome-calculator")
            self.speak("Opening Calculator")
        except Exception as e:
            self.speak("Failed to open Calculator")
            print(f"Error: {e}")

    def open_vscode(self):
        try:
            os.system("code")
            self.speak("Opening Visual Studio Code")
        except Exception as e:
            self.speak("Failed to open VS Code")
            print(f"Error: {e}")

    def tell_time(self):
        current_time = datetime.now().strftime('%I:%M %p')
        self.speak(f"The current time is {current_time}")

    def take_note(self):
        self.speak("What should I note?")
        note = self.listen()
        if note:
            try:
                with open("notes.txt", "a") as f:
                    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: {note}\n")
                self.speak("Note added successfully.")
            except Exception as e:
                self.speak("Failed to save the note")
                print(f"Error: {e}")

    def get_sentiment(self, text):
        """Analyze text sentiment with error handling"""
        if not text:
            return "neutral"
            
        try:
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity
            if sentiment > 0.1:
                return "positive"
            elif sentiment < -0.1:
                return "negative"
            else:
                return "neutral"
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return "neutral"

    def respond_to_sentiment(self, mood):
        """Respond appropriately to user sentiment"""
        responses = {
            "positive": ["You sound happy! That's great.", "Glad to hear you're doing well!"],
            "negative": ["I'm here for you. Don't worry.", "Would you like to talk about it?"],
            "neutral": ["Thanks for sharing.", "I see."]
        }
        response = np.random.choice(responses.get(mood, ["Thanks for sharing."]))
        self.speak(response)

    def analyze_sentiment(self):
        """Handle sentiment analysis command"""
        self.speak("Please tell me something to analyze")
        text = self.listen()
        if text:
            mood = self.get_sentiment(text)
            self.respond_to_sentiment(mood)

    def normalize_command(self, text):
        """Normalize text for better command matching"""
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        return text

    def initialize_models(self):
        """Initialize ML models with better datasets"""
        # Improved student marks model with more realistic data
        study_hours = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
        marks = np.array([30, 45, 55, 65, 72, 78, 82, 86, 90, 93])
        self.student_model = LinearRegression().fit(study_hours, marks)
        
        # Improved house price model with more realistic data
        sizes = np.array([800, 1000, 1200, 1500, 1800, 2000, 2200, 2500]).reshape(-1, 1)
        prices = np.array([250000, 320000, 380000, 450000, 520000, 580000, 630000, 700000])
        self.house_model = LinearRegression().fit(sizes, prices)

    def extract_number_from_speech(self, text):
        """Extract numbers from spoken text — supports both words and digits."""
        if not text:
            return None

<<<<<<< HEAD
        # try direct conversion first
=======
        # Try direct conversion first
>>>>>>> c1d6544cf615ef8f79cf546cce7003950de781cd
        try:
            return float(text)
        except ValueError:
            pass

        # Map number words to digits
        word_to_num = {
            'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
            'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
            'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,
            'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
            'eighteen': 18, 'nineteen': 19, 'twenty': 20,
            'thirty': 30, 'forty': 40, 'fifty': 50,
            'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90,
            'hundred': 100, 'thousand': 1000
        }

        text = text.lower().replace("-", " ").replace(" and ", " ")
        parts = text.strip().split()
        number = 0
        current = 0
        decimal = False
        decimal_str = ""

        for word in parts:
            if word.replace(".", "", 1).isdigit():
                return float(word)  # Handles inputs like "20000" or "3.5"
            if word == 'point':
                decimal = True
                continue
            if word not in word_to_num:
                continue
            value = word_to_num[word]
            if decimal:
                decimal_str += str(value)
            elif value == 100:
                current *= 100
            elif value == 1000:
                current *= 1000
                number += current
                current = 0
            else:
                current += value

        number += current
        if decimal_str:
            return float(f"{number}.{decimal_str}")
        return float(number) if number else None

    def predict_student_marks(self):
        self.speak("Please tell me the number of study hours.")
        hours_input = self.listen()

        if not hours_input:
            self.speak("I didn't get the study hours.")
            return

        try:
            # Extract number from speech
            hours = self.extract_number_from_speech(hours_input)
            if hours is None:
                raise ValueError("Couldn't understand the number")

            # Validate input range
            if hours < 0 or hours > 24:
                self.speak("Please enter realistic study hours between 0 and 24.")
                return

            # Make prediction
            prediction = self.student_model.predict([[hours]])[0]

            # Cap prediction between 0 and 100
            prediction = max(0, min(100, prediction))

            self.speak(f"For {hours} hours of study, the predicted marks are about {int(round(prediction))} out of 100.")
        except Exception as e:
            self.speak("Sorry, I couldn't process that. Please say something like 'two hours' or 'three point five hours'.")
            print(f"Error: {e}")

    def predict_house_price(self):
        self.speak("Please tell me the size of the house in square feet.")
        size_input = self.listen()

        if not size_input:
            self.speak("I didn't get the house size.")
            return

        try:
            # Extract number from speech
            size = self.extract_number_from_speech(size_input)
            if size is None:
                raise ValueError("Couldn't understand the number")

            # Validate input range
            if size < 100 or size > 10000:
                self.speak("Please enter a realistic size between 100 and 10,000 square feet.")
                return

            # Make prediction
            prediction = self.house_model.predict([[size]])[0]

            # Format price nicely
            formatted_price = "₹{:,.2f}".format(prediction)
            self.speak(f"For a {int(size)} square feet house, the predicted price is about {formatted_price}.")
        except Exception as e:
            self.speak("Sorry, I couldn't process that. Please say something like 'one thousand' or 'fifteen hundred'.")
            print(f"Error: {e}")

    # ... (keep all your other imports and class methods the same until run())

    def run(self):
<<<<<<< HEAD
        """Main execution loop"""
        self.speak("Hello, I am your AI assistant Jarvis. How can I help you today?")

        while True:
            try:
                command = self.listen()
                if not command:
                    continue
                    
                command = self.normalize_command(command)
                
                # First check for exit command
                if any(word in command for word in ["exit", "quit", "goodbye"]):
                    self.speak("Goodbye! Have a great day.")
                    sys.exit(0)
                
                # Check for exact command matches first
                command_found = False
                for cmd in self.command_map:
                    if cmd in command:
                        try:
                            self.command_map[cmd]()
                        except Exception as e:
                            print(f"Command '{cmd}' failed: {e}")
                        command_found = True
                        break

                if not command_found:
                    # GrowMe integration
                    if "growme" in command:
                        print("GrowMe options: create / update / show")
                        choice = input("Enter choice: ").lower()
                        if "create" in choice:
                            growme_create_goal()
                        elif "update" in choice:
                            growme_update_progress()
                        elif "show" in choice:
                            growme_show_progress()
                        else:
                            print("Invalid option. Please choose create, update, or show.")
                    else:
                        self.speak("Sorry, I didn't understand that command. try something like 'open YouTube' or 'analyse sentiment'.")
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"Error: {e}")
                self.speak("Sorry, I encountered an error. Please try again.")
                time.sleep(1)
                continue
=======
      """Main execution loop"""
      self.speak("Hello, I am your AI assistant Jarvis. How can I help you today?")
    
      while True:
        try:
            command = self.listen()
            if not command:
                continue
                
            command = self.normalize_command(command)
            
            # First check for exit command
            if any(word in command for word in ["exit", "quit", "goodbye"]):
                self.speak("Goodbye! Have a great day.")
                sys.exit(0)
            
            # Check for exact command matches first
            command_found = False
            for cmd in self.command_map:
                if cmd in command:
                    self.command_map[cmd]()
                    command_found = True
                    break
            
            if not command_found:
                self.speak("Sorry, I didn't understand that command. Try something like 'open YouTube' or 'analyse sentiment'.")
                
        except KeyboardInterrupt:
            self.speak("Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")
            self.speak("Sorry, I encountered an error. Please try again.")
            time.sleep(1)
            continue
>>>>>>> c1d6544cf615ef8f79cf546cce7003950de781cd

# ... (rest of your code remains the same)
if __name__ == "__main__":
    assistant = Jarvis()
    try:
        assistant.run()
    except KeyboardInterrupt:
        assistant.speak("Goodbye!")
    except Exception as e:
        print(f"Fatal error: {e}")
        assistant.speak("Sorry, I encountered a serious error. Restarting might help.")