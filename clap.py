import sounddevice as sd
import numpy as np
import pyautogui
import time
import threading
import tkinter as tk
from scipy.signal import butter, lfilter
import queue
import json
from vosk import Model, KaldiRecognizer

# ---------------- Clap Detection ----------------
THRESHOLD = 0.15         # sensitivity for loudness
SHARPNESS_MIN = 0.018    # sharpness of clap
MIN_INTERVAL = 0.4       # minimum gap between claps
last_clap = 0

# ---------------- Voice Detection ----------------
VOICE_MIN_INTERVAL = 0.8  
last_voice = 0
q = queue.Queue()

# ---------------- Filters ----------------
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut=800.0, highcut=5000.0, fs=44100, order=6):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    return lfilter(b, a, data)

# ---------------- Clap ----------------
def clap_callback(indata, frames, time_info, status):
    global last_clap
    filtered = bandpass_filter(indata[:, 0])
    energy = np.linalg.norm(filtered)
    sharpness = np.mean(np.abs(np.diff(filtered)))

    if energy > THRESHOLD and sharpness > SHARPNESS_MIN:
        now = time.time()
        if now - last_clap > MIN_INTERVAL:
            pyautogui.click()
            root.after(0, lambda: update_status("👏 Clap detected → Mouse Click"))
            last_clap = now

# ---------------- Voice ----------------
def voice_callback(indata, frames, time_info, status):
    q.put(bytes(indata))

def listen_voice():
    global last_voice
    model = Model("vosk-model-small-en-us-0.15")
    rec = KaldiRecognizer(model, 16000)

    mic = sd.RawInputStream(
        samplerate=16000,
        blocksize=800,
        dtype="int16",
        channels=1,
        callback=voice_callback
    )

    with mic:
        root.after(0, lambda: update_status("🎤 Voice Ready (say 'play' or 'pause')"))
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if "text" in result:
                    spoken = result["text"].strip().lower()
                    if spoken in ["play", "pause"]:
                        now = time.time()
                        if now - last_voice > VOICE_MIN_INTERVAL:
                            pyautogui.click()
                            root.after(0, lambda: update_status(f"🗣️ Heard '{spoken}' → Mouse Click"))
                            last_voice = now

# ---------------- GUI ----------------
def update_status(msg):
    status_var.set(msg)
    root.update_idletasks()

root = tk.Tk()
root.title("🖱️ Clap & Voice Clicker")
root.geometry("420x200")

status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, font=("Arial", 12),
                        wraplength=380, justify="center")
status_label.pack(expand=True)

update_status("Initializing...")

# ---------------- Run Both ----------------
threading.Thread(target=listen_voice, daemon=True).start()

def start_clap_listener():
    with sd.InputStream(callback=clap_callback, channels=1,
                        blocksize=256, samplerate=44100):
        sd.sleep(-1)

threading.Thread(target=start_clap_listener, daemon=True).start()

root.mainloop()
