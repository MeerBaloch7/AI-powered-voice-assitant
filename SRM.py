import speech_recognition as sr
import whisper
import numpy as np

# speech recognition module 

class SpeechRecognitionModule:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.model = whisper.load_model('base.en')

    def recognize_speech(self):
        try:
            print("Listening...")
            with sr.Microphone() as source:

                self.recognizer.adjust_for_ambient_noise(source,duration=1)

                audio = self.recognizer.listen(source,timeout=5, phrase_time_limit=10)

        except OSError as e:
            print(f"Error: microphone not found or not accessible. {e}")

            return None

        return self.TranscribeAudio(audio)


    def TranscribeAudio(self, audio):
        try:
            raw = audio.get_raw_data()

            # converting it into numpy arrays

            audio_np = np.frombuffer(raw, dtype = np.int16)

            # converting into 32 bit
            audio_np = audio_np.astype(np.float32) / 32768

            result = self.model.transcribe(audio_np, language ='en' , fp16 = False)

            text = result['text'].strip()

            print(" recognized text:", text)

            return text
        except Exception as e:
            print("whisper error", e)
            return None




''' # google api recognition

        try:
            print(" speech recognition started wait....")
            #text = self.recognizer.recognize_google(audio)
            print("recognized: \n", text)

            return text

        except sr.UnknownValueError:
            print(" google could not understand the speech")
        except sr.RequestError:
            print(" internet unavailable")
            '''



'''# CMU Sphinx recognization

        try: 
            print (" trying offline recognition ")
            text = self.recognizer.recognize_sphinx(audio)
            print(" recognized :\n", text)
            return text
        except sr.UnknownValueError:
            print('could not understnd offline')
        except sr.RequestError as e:
            print("sphinx Error:", e)

        print("Speech Recognition failed......")
'''




if __name__ == "__main__":

    srm = SpeechRecognitionModule()

    result = srm.recognize_speech()

    if result:
        print("\nFinal Text:", result)
    else:
        print("\nNo speech recognized.")       
