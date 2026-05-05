- Step by step guide to follow:
1. setup the virtual environment.
- for that run the command in the terminal- python -m venv venv
- for windows: venv\Scripts\activate    -- this will activate the virtual environment

- We are testing whisper.cpp. We started with taking an audio file converting it to the right format which is WAV , 16KHz, monochannel as this is the required format for whister.cpp.
- We used ffmpeg that converts audio file formats.
- we fed this audio file to whisper.cpp and it produced correct response. For testing its accuracy I had added 'aaaa hmmm' sounds like we humans normally do while speaking. The observation is : 'hmm..' sound got completely removed while for the 'aaa...' sound 'an' got added as a word. 

- ------------Step 2----------------
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

- Observations: Pronounication errors are there, but they can be minimized by speaking clearly and loud. As for noise- I have a ceiling fan running in the background, yet it didn't add to any errors. While speaking I intentionally added "aaaaa.." and "hmm..' sounds, and they are ignored mostly. It was only in one case that I saw the word "and" added extra for the "aaa.." sound I had added. 

- -----------------STEP 3 - Interacting with an LLM ---------------------------------

- ADDING THE BRAIN LAYER: I am using Mistral model provided by Ollama. I downloaded Ollama and then did an - ollama launch mistral. 
- The idea is once the text by the user has been transcribed, we feed that into the llm, and generate a response, which is right now shown back to the user in text format. Soon, we will add another layer of text to speech system (TTS). 

- Observations: 
1. When I spoke in spanish, the errors in transcription increased significantly, is it was not able to recognise what I was speaking. Potential cause of this error could be that I am using tiny model from pywhispercpp which might now know that which langauge is being spoken( we will further investigate this to find out actual cause).
2. I has instructed the llm with the following system prompt:
- "You are a helpful spanish conversation partner and teacher. "
                            "You have to help in learning the language for a beginner. "
                            "Keep responses short and simple. "
- This was clearly not sufficient because even while having converstaions with the agent I told it multiple times that I dont understand much spanish, and I also told which spanish words I know, yet it produced results in spanish, rather I wanted it to mix spanish and english. Also, the mistakes in transcription could have resulted in model not understanding my requests correctly.( we need to further investigate).

- I switched to "small" model and it works better than "tiny". 4
- The prompt in the system role was also improved to make the ai answer more user friendly and to make sure it doesn't speak too much in spanish, as user is at beginner level. 

- --------------------------------STEP4 : Adding TTS(TEXT TO SPEECH) -------------------

- We have used a basic tts converter - pyttsx3. Its special feature is that it works offline. 
- But conversion is very basic and the voice sounds very robotic. It even says dot(.) for full stops that come. 

- 19 april 2026
- Today, I started a fresh with the agent. I observed that the answer it gave me is better. whisper was able to detect the language also as spanish. I will continue the conversation to see if it gets worse with time due to memory issue or remains same or improves.

- 2nd time transcription was perfect I said- hola. como estas? tiene manzanas- perfectly transcribed
- The llm layer takes a lot of time 15-20 secs and this time increases if audio input is more.
- the agent voice is robotic and it is pronouncing the spanish words as english words. this needs improvement. also in previous reply it told me to reply with estoy bein which means - i am well, and had said we will continue a conversation if I say this , but in the next reply it forgot about this and again started from:
- (
- AI speaking:   Hola! I'm glad to be your Spanish conversation partner. Let's start! What words or phrases do you already know? I'll respond using only the words and phrases you provide, and I'll explain new ones when necessary.

Here are a few common Spanish phrases:
- Hola (Hello)
- ¿Cómo estás? (How are you?)
- Estoy bien, gracias. (I'm fine, thank you.)
- Por favor (Please)
- Gracias (Thank you)
- Lo siento (I'm sorry)
- Sí (Yes)

- )

- ----------------------------------STEP 5- Building a continuous conversation loop-------------------

- adding while loop and put code in it and an exit statement so code will exist only when user says so

- interesting observation is that whisper cannot understand spanish and english today, it is detecting one language only and then does transcription based on it.because I started with spanish and later said some english words and it transacribed it completely in spanish

---------------------------------------Improving exisiting systems-------------------------------------
- We have now completed round one of working on the project. Now, going forward we will be experimenting with every layer, and see what tweaks help us improve the performance of our voice agent.

- The first layer is where we will again start with. I will first try medium level model of whisper.cpp and compare it with parakeet-v3 using NeMo library of Nvidia. This change will be in place of whisper.cpp which has its share of drawbacks as we know.

- Obversations with medium model: I spoke in combined engish and spanish, beginning with spanish, yet the model has given 94% english probability. Transcription is taking more time. Is it because of my laptop/cpu? 
- Medium is not really suitable to be run on laptop. It is slow. 
- Lets try quantized version of small. 
- small-q5_1 is just 181MB VS medium -> 1.3Gb
- small-q8_0 is 252Mb
- for my testing small , and quantized of it have been better than medium. Transcription is faster, accuracy- okaish- better judgement if we include metrics also, but that will be introduced later.

- I was downloading the dependences for running parakeet and guys it has been 30 mins almost and it is still running. My laptop will explode. If I dont push changes for next 5 days, consider i am gone and the laptop took me to heaven.
- I should accept it will not work on this laptop but I want to try it.
- I accepted my defeat that model was too heavy, even dependencies were not getting fully downloaded, so rather than getting stuck, I move to the trying small-q8_0, and then whisper faster.

- Right now, I will go with the small model, no quantized version of it because I feel I am purely speaking one language, it gives good transalation and is fast as well.

- Now I will experiment with other models from ollama and compare their responses and response time with each other. 

- One impt thing is, when we pull these models in ollama, they are getting stored in our stoarge(disk), so if we don't need and we should remove otherwise storage will get filled. To remove any model use:
- ollama rm mistral

- Lets now work with Qwen.

-----------------------MEMORY MANAGEMENT---------------

- Started with Structured memory

- JSON in-built python module
- json.load(f) that will load a json file f as python dictionary.

- Till now our system is not updating when user gives input- we are not modifying the structuredmemory yet. But going forward, we need to parse the incoming user input and fill required details in memory.


-  My initial observation with the model is that it seems that the prompt that we have written might not be working very properly because even though I mentioned that I know only a few words in Spanish and I mentioned those words also like hola, Como Estas, Aqui, Parque, Banco, Bano.

👉 The model clearly does not understand that I am unable to have a proper conversation in Spanish and is repeating back in Spanish which obviously a user who has no knowledge of the language cannot understand. So our first demo I think is leaning more towards the failure side. 

- What we have implemented in memory right now is a structured memory and we have a prompt that takes the user input also and if I look at my structured memory.json file it's updated at the data field is getting updated but the other fields that are supposed to take weak words or profile or the level or the language that the user is speaking in these fields are not getting updated.