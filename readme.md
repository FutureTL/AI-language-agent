- Step by step guide to follow:
1. setup the virtual environment.
- for that run the command in the terminal- python -m venv venv
- for windows: venv\Scripts\activate    -- this will activate the virtual environment

- We are testing whisper.cpp. We started with taking an audio file converting it to the right format which is WAV , 16KHz, monochannel as this is the required format for whister.cpp.
- We used ffmpeg that converts audio file formats.
- we fed this audio file to whisper.cpp and it produced correct response. For testing its accuracy I had added 'aaaa hmmm' sounds like we humans normally do while speaking. The observation is : 'hmm..' sound got completely removed while for the 'aaa...' sound 'an' got added as a word. 

- ------------Step 2-------
- Now we want to directly capture audio and produce the output using whisper without having to first manually generate an audio file.
- We are using sounddevice module for that.
- python -m pip install sounddevice
- ASIO stands for Audio Stream Input Output

- sounddevice module with pip (on Windows) will provide two PortAudio DLLs, with and without ASIO support. By default, the DLL without ASIO support is loaded. To load the DLL with ASIO support, the environment variable SD_ENABLE_ASIO has to be set before importing the sounddevice module, for example like this:

- import os
# Set environment variable before importing sounddevice. Value is not important.
- os.environ["SD_ENABLE_ASIO"] = "1"
-----------------some theory for better understanding -----------
- There is a concept of channels. Channel =1 means same sound is being perceived everywhere. Whisper.cpp requires channel=1.
- Stereo means channels=2 means there is a difference in left and right audio. Our ears also work on 2 channels. Music devices etc also operate on this. 
- For our use case where we have to capture the user input speech channel=1 is better. 

- Important idea- We want to auto detect at some sound is being send through the microphone to our application. We will detect this using the InputStream concept in sounddevice module. This will allow us to capture incoming sounds and we can capture it in the form of frames/chunks of speech signals. These signals are basically sound wave amplitudes.

- So the basic idea is we get these chunks, store then in an array,and when the user stops talking, we will have collected all the chunks in the array. We can customise it in a way so it can be sent to whisper.cpp for processing. 

- An important concept enters here: how do we know that the user has stoped talking. No speech signal will be detected through microphone right? True, but noise can also be falsely detected as speech in this case, and if we append it directly to our array we wont' know when to stop processing user input.

- For this we use VAD(Voice activity detection). The role of this system is to answer a simple question: is incoming signal a speech signal or not. It gives value -> 1 for voice detected and _. 0 for no voice detected.

- we need to add a VAD layer before we feed our audio into whisper.cpp

- We will be using WEBRTC VAD - real time algorithm that processes incoming audio to determine if it contains human speech or not.

- MIC -> indata -> convert format to int 16 as needed by webrtc vad -> vad check for speech chunk 


- We now use a wrapper pywhispercpp because our code is in python, and whisper.cpp is in C++. 

- This pywhispercpp will load a model into memory. This model can by tiny, small, large etc and it matters because it will determine how much time it takes, and hardware also. 

- Mic → VAD → numpy array → whisper

- full_audio → pass to whisper wrapper(pywhispercpp)