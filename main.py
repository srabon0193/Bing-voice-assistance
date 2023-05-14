import openai
import asyncio
import re
import pyttsx3
import whisper
# import boto3
# import pydub
# from pydub import playback
# import speech_recognition as sr
from EdgeGPT import Chatbot, ConversationStyle

# Initialize the OpenAI API
openai.api_key = "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"

#Create a recognizer object and wake word variables
# recognizer =  sr.Recognizer()
engine = pyttsx3.init()
BING_WAKE_WORD = "bing"
GPT_WAKE_WORD = "gpt"

def get_wake_word(phrase):
    if BING_WAKE_WORD in phrase.lower():
        return BING_WAKE_WORD
    elif GPT_WAKE_WORD in phrase.lower():
        return GPT_WAKE_WORD
    else:
        return None
    
# def synthesize_speech(text, output_filename):
#     polly = boto3.client('polly', region_name='us-west-2')
#     response = polly.synthesize_speech(
#         Text=text,
#         OutputFormat='mp3',
#         VoiceId='Salli',
#         Engine='neural'
#     )

#     with open(output_filename, 'wb') as f:
#         f.write(response['AudioStream'].read())

# def play_audio(file):
#     sound = pydub.AudioSegment.from_file(file,format='mp3')
#     playback.play(sound)
def speak(text):
    engine.say(text)
    
    voices = engine.getProperty('voices')       #getting details of current voice
                                                #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[0].id)
    engine.runAndWait()

async def main():
    while True:
        prompt_input = input("Say something: ")
        wake_word = get_wake_word(prompt_input)

        if wake_word is None:
            print("Not a wake word. Try again...")
            continue

        if wake_word == BING_WAKE_WORD:
            bot = Chatbot(cookie_path='cookies.json')
            response = await bot.ask(prompt=prompt_input, conversation_style=ConversationStyle.precise)
            # Select only the bot response from the response dictionary
            for message in response["item"]["messages"]:
                if message["author"] == "bot":
                    bot_response = message["text"]
            # Remove [^#^] citations in response
            bot_response = re.sub('\[\^\d+\^\]', '', bot_response)

            bot = Chatbot(cookie_path='cookies.json')
            response = await bot.ask(prompt=prompt_input, conversation_style=ConversationStyle.creative)
            for message in response["item"]["messages"]:
                if message["author"] == "bot":
                    bot_response=message["text"]
            # Remove [^*^] citations in response
            bot_response=re.sub('\[\^\d+\^\]','',bot_response)

        else:
            # Send prompt to GPT-3.5-turbo API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content":
                    "You are a helpful assistant."},
                    {"role": "user", "content": prompt_input},
                ],
                temperature=0.5,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                n=1,
                stop=["\nUser:"],
            )

            bot_response = response["choices"][0]["message"]["content"]

        print("Bot's response:",bot_response)
        speak(bot_response)


        # with sr.Microphone() as source:
        #     recognizer.adjust_for_ambient_noise(source)
        #     print("waiting for wake words 'ok bing' or 'ok chat'...")
        #     while True:
        #         audio = recognizer.listen(source)
        #         try:
        #             with open("audio.wav","wb") as f:
        #                 f.write(audio.get_wav_data())
        #                 #Use the preloaded tiny model
        #                 model = whisper.load_model("tiny")
        #                 result = model.transcribe("audio.wav")
        #                 phrase = result["text"]
        #                 print(f"You said: {phrase}")

        #                 wake_word = get_wake_word(phrase)
        #                 if wake_word is not None:
        #                     break
        #                 else:
        #                     print("Not a wake word. Try again...")
        #         except Exception as e:
        #             print("Error transcribing audio: {0}".format(e))
        #             continue

        #     print("Speak a prompt...")
        #     synthesize_speech('What can I help you with?', 'response.mp3')
        #     play_audio('response.mp3')
        #     audio = recognizer.listen(source)

        #     try:
        #         with open("audio_prompt.wav", "wb") as f:
        #             f.write(audio.get_wav_data())
        #         model = whisper.load_model("base")
        #         result = model.transcribe("audio_prompt.wav")
        #         user_input = result["text"]
        #         print(f"You said: {user_input}")
        #     except Exception as e:
        #         print("Error transcribing audio: {0}".format(e))
        #         continue

        #     if wake_word == BING_WAKE_WORD:
        #         bot = Chatbot(cookie_path='cookies.json')
        #         response = await bot.ask(prompt=user_input, conversation_style=ConversationStyle.precise)
        #         # Select only the bot response from the response dictionary
        #         for message in response["item"]["messages"]:
        #             if message["author"] == "bot":
        #                 bot_response = message["text"]
        #         # Remove [^#^] citations in response
        #         bot_response = re.sub('\[\^\d+\^\]', '', bot_response)

        #         bot = Chatbot(cookiepath='cookies.json')
        #         response = await bot.ask(prompt=user_input, conversation_style=ConversationStyle.creative)
        #         for message in response["item"]["messages"]:
        #             if message["author"] == "bot":
        #                 bot_response=message["text"]
        # # Remove [^*^] citations in response
        #         bot_response=re.sub('\[\^\d+\^\]','',bot_response)

        #     else:
        #         # Send prompt to GPT-3.5-turbo API
        #         response = openai.ChatCompletion.create(
        #             model="gpt-3.5-turbo",
        #             messages=[
        #                 {"role": "system", "content":
        #                 "You are a helpful assistant."},
        #                 {"role": "user", "content": user_input},
        #             ],
        #             temperature=0.5,
        #             max_tokens=150,
        #             top_p=1,
        #             frequency_penalty=0,
        #             presence_penalty=0,
        #             n=1,
        #             stop=["\nUser:"],
        #         )

        #         bot_response = response["choices"][0]["message"]["content"]

        # print("Bot's response:",bot_response)
        # synthesize_speech(bot_response, 'response.mp3')
        # play_audio('response.mp3')
        # # await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
