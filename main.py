import openai
import pyttsx3
import speech_recognition as sr


openai.api_key = 'YOUR API KEY'

engine = pyttsx3.init()


def speech_to_text(file_name):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_name) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            print('Skipping Unknown Error')


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        temperature=0.2,
        n=1,
        stream=False,
        stop=None
    )
    return response.choices[0].text


def text_to_speech(response):
    engine.say(response)
    engine.runAndWait()


def main():
    while True:
        print('Say "Hi, Nova" to start your Prompt')
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == 'hi nova' or transcription.lower() == 'nova':
                    file_name = 'input.wav'
                    print('Ask GPT-3 whatever you desire...')
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1.2
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(file_name, 'wb') as file:
                            file.write(audio.get_wav_data())

                    text = speech_to_text(file_name)

                    if text:
                        print(f'Prompt: {text}')

                    response = generate_response(text)
                    print(f'Response: {response}')

                    text_to_speech(response)

            except Exception as e:
                print(f'An Error: {e}')


if __name__ == "__main__":
    main()
