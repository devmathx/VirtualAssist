
import speech_recognition as sr
import playsound
from gtts import gTTS
from random import randint
import webbrowser
import pyttsx3
import os

class Virtual_assist():
    def __init__(self, assist_name, person):
        self.assist_name = assist_name
        self.person = person
        
        self.engine = pyttsx3.init()
        self.rec = sr.Recognizer()
        
        self.voice_data = ''
      
      
        
    def engine_speak(self, text): 
        # Fala da assistente virtual
        text = str(text)
        self.engine.say(text)
        self.engine.runAndWait()
     
     
        
    def record_audio(self, ask=''):
        # Captura de áudio
        with sr.Microphone(0) as source:
            self.rec.adjust_for_ambient_noise(source)
            if ask:
                print('Ouvindo...')
                self.engine_speak(ask)
            
            audio = self.rec.listen(source, 5, 5)
            print('Esperando por um comando.')
            
            try:
                self.voice_data = self.rec.recognize_google(audio, language='pt-BR')
            except sr.UnknownValueError:
                self.engine_speak(f'Desculpe {self.person}, eu não entendi o que você disse, poderia repetir?')
            except sr.RequestError:
                self.engine_speak('Desculpe, a conexão caiu.')
                
            print('>>', self.voice_data)
            self.voice_data = self.voice_data.lower()
            return self.voice_data.lower() 
    
    
    
    def engine_speak(self, audio_string):
        audio_string = str(audio_string)
        tts = gTTS(text=audio_string, lang='pt')
        audio_file = 'audio' + str(randint(1, 200)) + '.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        print(self.assist_name + ':', audio_string)
        os.remove(audio_file)
        
        
        
    def there_exist(self, terms):
        # Verificar se o termo existe
        for term in terms:
            if term in self.voice_data:
                return True
        
        
            
    def respond(self, voice_data):
        if self.there_exist(['bom dia', 'boa tarde', 'olá', 'oi']):
            greetings = [
                f'Olá {self.person}, como vai o seu dia?',
                f'Oi, o que você precisa?'
                f'Estou aqui, você precisa de algo?']
            self.engine_speak(greetings[randint(0, len(greetings)-1)])
        
        # Google
        if self.there_exist(['pesquise por']) and 'youtube' not in voice_data:
            search_term = voice_data.split('por')[-1]
            url = 'http://google.com/search?q=' + search_term
            webbrowser.get().open(url)
            self.engine_speak('Encontrei isso sobre ' + search_term + 'no google')
        
        # Youtube
        if self.there_exist(['pesquise no youtube por']):
            search_term = voice_data.split('por')[-1]
            url = 'http://www.youtube.com/results?search_query=' + search_term
            webbrowser.get().open(url)
            self.engine_speak('Encontrei isso sobre ' + search_term + 'no youtube')        


assistent = Virtual_assist('Alexa', 'Matheus')

while True:
    voice_data = assistent.record_audio('Ouvindo...')   
    assistent.respond(voice_data)
    
    if assistent.there_exist(['adeus', 'tchau', 'até mais', 'encerrar']):
        assistent.engine_speak('Tenha um bom dia!') 
        break
