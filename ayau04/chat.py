import os
from groq import Groq
import creds
import azure.cognitiveservices.speech as speechsdk
from loguru import logger

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Initialize the Groq client
groq_client = Groq(api_key=creds.GROQ_API_KEY)

def groq_completion(messages, model='llama-3.3-70b-versatile', temp=0.9, tokens=400):
    if not messages:
        return None
    response = groq_client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=temp,
        max_tokens=tokens
    )
    text = response.choices[0].message.content.strip()
    return text


def speak_text(text):
    speech_config = speechsdk.SpeechConfig(subscription=creds.SPEECH_KEY, region=creds.SPEECH_REGION)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name='en-GB-SoniaNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
   
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        logger.debug("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        logger.debug("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                logger.error("Error details: {}".format(cancellation_details.error_details))
                logger.error("Did you set the speech resource key and region values?")


    return text
    
    

