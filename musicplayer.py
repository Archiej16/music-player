import keyboard 
import tkinter as tk
from tkinter import messagebox, scrolledtext
import speech_recognition as sr
import pyttsx3
import pywhatkit
import threading

# TTS Setup
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1)

def speak(text):
    print(f"🎧 Genie says: {text}")
    engine.say(text)
    engine.runAndWait()

# GUI Functions
import keyboard  # Add this to your imports at the top

def listen_and_play():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        update_status("🎙️ Listening...")
        speak("I'm listening, go ahead.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        input_box.delete(0, tk.END)
        input_box.insert(0, f"You said: {command}")

        if "play" in command:
            song = command.replace("play", "").strip()
            if song:
                message = f"🎵 Playing: {song}"
                update_status(message)
                speak(message)
                pywhatkit.playonyt(song)
                playlist.insert(tk.END, f"• {song}\n")
            else:
                update_status("❗ Say the song name after 'play'.")
                speak("Please say the name of the song.")
        elif "pause" in command or "resume" in command:
            speak("Toggling play and pause.")
            keyboard.press_and_release('space')
            update_status("⏯️ Toggled play/pause.")
        elif "stop" in command or "close" in command:
            speak("Closing the music tab.")
            keyboard.press_and_release('ctrl+w')
            update_status("🛑 Closed the tab.")
        elif "exit" in command:
            speak("Goodbye, music lover.")
            update_status("👋 Exiting...")
            app.after(2000, app.quit)
        else:
            speak("I didn't understand that. Try saying play, pause, or stop.")
            update_status("❓ Command not recognized.")

    except sr.UnknownValueError:
        speak("I couldn't understand you.")
        update_status("😕 Didn't catch that.")
    except sr.RequestError:
        speak("Check your internet connection.")
        update_status("⚠️ Network error.")


def update_status(text):
    status_label.config(text=text)

def threaded_listen():
    threading.Thread(target=listen_and_play).start()

# GUI Setup
app = tk.Tk()
app.title("🎶 Stylish Voice Music Genie")
app.geometry("450x500")
app.configure(bg="#121212")

# Styling
font_main = ("Helvetica", 16, "bold")
font_secondary = ("Helvetica", 12)

# Title
title = tk.Label(app, text="🎧 Voice Music Player", font=font_main, bg="#121212", fg="#00FFD1")
title.pack(pady=15)

# Status Label
status_label = tk.Label(app, text="Click and say 'Play [song]'", font=font_secondary, bg="#121212", fg="#BBBBBB")
status_label.pack(pady=10)

# Command Display
input_box = tk.Entry(app, font=("Helvetica", 12), width=40, bd=2, relief="solid", justify="center")
input_box.pack(pady=10)

# Speak Button
speak_btn = tk.Button(app, text="🎤 Speak", font=font_main, bg="#00FFD1", fg="#121212", activebackground="#1DB9A0",
                      relief="flat", bd=0, padx=30, pady=10, command=threaded_listen)
speak_btn.pack(pady=10)

# Playlist Label
playlist_label = tk.Label(app, text="🎵 Recent Songs", font=("Helvetica", 14), bg="#121212", fg="#00FFD1")
playlist_label.pack(pady=(20, 5))

# Playlist Display
playlist = scrolledtext.ScrolledText(app, height=8, width=45, bg="#1e1e1e", fg="white", font=("Helvetica", 10),
                                     wrap=tk.WORD, relief="solid", borderwidth=1)
playlist.pack(pady=5)

# Exit Button
exit_btn = tk.Button(app, text="Exit", font=("Helvetica", 12), bg="#FF4D4D", fg="white", relief="flat",
                     padx=20, pady=5, command=app.quit)
exit_btn.pack(pady=15)

app.mainloop()

