import sounddevice as sd
import numpy as np
import webrtcvad
import collections
from pywhispercpp.model import Model

from llmbrain import LLMBrain
from tts import speak

# ---------------- CONFIG ----------------
SAMPLE_RATE = 16000
CHANNELS = 1
FRAME_DURATION_MS = 30
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)

VAD_MODE = 2
SILENCE_LIMIT_SEC = 1.2

# ---------------------------------------

vad = webrtcvad.Vad(VAD_MODE)
model = Model("small")  # use tiny for faster testing
llmbrain = LLMBrain()

def float_to_pcm16(audio):
    audio = np.clip(audio, -1, 1)
    return (audio * 32767).astype(np.int16)

while True:

    audio_buffer = []
    silence_buffer = collections.deque(
        maxlen=int(SILENCE_LIMIT_SEC * 1000 / FRAME_DURATION_MS)
    )

    recording = False
    stop_recording = False  # 🔥 NEW FLAG




    def callback(indata, frames, time, status):
        global recording, stop_recording

        if status:
            print("⚠️", status)

        pcm16 = float_to_pcm16(indata[:, 0])
        pcm_bytes = pcm16.tobytes()

        is_speech = vad.is_speech(pcm_bytes, SAMPLE_RATE)

        if is_speech:
            if not recording:
                print("🟢 Speech started")
                recording = True

            audio_buffer.append(pcm16)
            silence_buffer.clear()

        else:
            if recording:
                silence_buffer.append(pcm16)

                if len(silence_buffer) == silence_buffer.maxlen:
                    print("🔴 Speech ended")
                    stop_recording = True  # 🔥 STOP via flag
                else:
                    audio_buffer.append(pcm16)


    print("🎤 Listening... Speak something")

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        blocksize=FRAME_SIZE,
        callback=callback,
    ):
        while not stop_recording:
            sd.sleep(100)

    print("✅ Exited audio stream")

    # ---------------- PROCESS AUDIO ----------------

    print("📦 Audio buffer length:", len(audio_buffer))

    if not audio_buffer:
            print("⚠️ No speech detected, try again.")
            continue
    full_audio = np.concatenate(audio_buffer)

    print("📦 Raw audio shape:", full_audio.shape)

    full_audio = full_audio.astype(np.float32) / 32767

    print("🧠 Transcribing...")

    segments = model.transcribe(full_audio, language= "auto")
    user_text = " ".join([seg.text for seg in segments])

    print("\n📝 Transcription:")
    for seg in segments:
        print("👉", seg.text)
    
     # -------- EXIT CONDITION --------
    if "exit" in user_text.lower():
        print("👋 Exiting...")
        break

    # feed this user input to the brain llm model
    response = llmbrain.generate_response(user_text)
    print("AI response: ", response)
    speak(response)

