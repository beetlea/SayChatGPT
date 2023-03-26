import os
import openai
from vosk import Model, KaldiRecognizer
import os
import pyaudio
from googletrans import Translator
import pyttsx3 
import time
translator = Translator()

openai.organization = "organiztion id"
openai.api_key = "token"
openai.Model.list()


model = Model(r"vosk-model-small-ru-0.22") # полный путь к модели
rec = KaldiRecognizer(model, 44100)
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16, 
    channels=1, 
    rate=44100, 
    input=True, 
    frames_per_buffer=4000
)
stream.start_stream()


def generate_gpt3_response(user_text, print_output=False):
    """
    Query OpenAI GPT-3 for the specific key and get back a response
    :type user_text: str the user's text to query for
    :type print_output: boolean whether or not to print the raw output JSON
    """
    completions = openai.Completion.create(
        engine='text-davinci-003',  # Determines the quality, speed, and cost.
        temperature=0.5,            # Level of creativity in the response
        prompt=user_text,           # What the user typed in
        max_tokens=100,             # Maximum tokens in the prompt AND response
        n=1,                        # The number of completions to generate
        stop=None,                  # An optional setting to control response generation
    )

    # Displaying the output can be helpful if things go wrong
    if print_output:
        print(completions)

    # Return the first choice's text
    return completions.choices[0].text


tts = pyttsx3.init() 
voices = tts.getProperty('voices') 
tts.setProperty('voice', 'ru') 

for voice in voices: 
    if voice.name == 'Aleksandr': 
        tts.setProperty('voice', voice.id) 
        


def print_models():
    models = openai.Model.list()

    for model in models.data:
        print(model.id)
        
    
if __name__ == '__main__':
    print("start")
    while True:
        #input("Жду нажатия")
        print("Говорите я вас слушаю")
        while True:
            data = stream.read(4000)
            if rec.AcceptWaveform(data):
                prompt = rec.Result()
                print(prompt)
                if prompt.find("слушай") != -1:
                    time.sleep(1)
                    tts.say("Говори. Слушаю внимательно")
                    tts.runAndWait()
                    break
        #print("ВВедите свой вопрос")
        #prompt = input()
        
        while True:
            data = stream.read(4000)
            if rec.AcceptWaveform(data):
                prompt = rec.Result()
                break
        begin = prompt.find(":")
        prompt = prompt[begin:-2]
        print(prompt)
        trans = translator.translate(prompt, dest="en")
        response = generate_gpt3_response(trans.text)
        print(response)
        trans = translator.translate(response, dest="ru")
        print(trans.text)
        tts.say(trans.text) 
        tts.runAndWait()

        