import os

# Set environment variable before importing sounddevice. Value is not important.
os.environ["SD_ENABLE_ASIO"] = "1"

import sounddevice as sd
import numpy as np
import webrtcvad
import collections

# ------------config -------------------
sample_rate = 16000
channels=1
frame_duration_ms = 30 
frame_size = int(sample_rate*frame_duration_ms/ 1000)

# 0-3(3-most aggressive)
vad_mode = 2   
silence_limit = 0.8

# --------------------------------------

vad = webrtcvad.VAD(vad_mode)

audio_buffer = []
silence_buffer = collections.deque(maxlen= int(silence_limit * 1000/frame_duration_ms))

recording = False

def float_to_pcm16(audio):
    audio = np.clip(audio, -1, 1)
    return (audio * 32767).astype(np.int16)

def callback(indata, frames, time, status):
    global recording

    if status:
        print(status)
    
     # convert float32 → int16
    pcm16 = float_to_pcm16(indata[:, 0])
    pcm_bytes = pcm16.tobytes()

    #webrtc vad check
    is_speech = vad.is_speech(pcm_bytes, sample_rate)

    # if speech is present 
    if is_speech:
        if not recording:
            recording = True 
            # recording turned on
        audio.buffer.append(pcm16)
        silence_buffer.clear()
    else:
        # no speech detected- this could be a small pause or actualy user has stopped talking
        if recording:
            silence_buffer.append(pcm16)

            # if long silence- we need to stop recording
            if len(silence_buffer) == silence_buffer.maxlen:
                print("speech ended")
                raise sd.CallbackStop()
            
            else:
                audio_buffer.append(pcm16)

with sd.InputStream(
    samplerate= sample_rate,
    channels = channels,
    blocksize = frame_size,
    callback = callback,
):
    try:
        while True:
            sd.sleep(100)
    except sd.CallbackStop:
        pass

#  --------------- final audio -------------------

if audio_buffer:
    full_audio = np.concatenate(audio_buffer)

    print("captured audio shape:", full_audio.shape)

    # Optional: normalize to float32 for later use
    full_audio = full_audio.astype(np.float32) / 32767

else:
    print("No speech detected")