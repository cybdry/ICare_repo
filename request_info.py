#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import user_requirement
import whisper
from voice_utils import convert_audio_to_text,convert_text_to_audio


base_message = " " 


def request_message(message,box):
    return_value,*values = user_requirement(message)
    if return_value:
        return values[0]
    else:
        question_to_ask = values[1]

        # Translate the question into spanish
        question_to_ask_spanish = whisper.Whisper().translate(question_to_ask,"es")
        # Then convert it to voice
        voice_question = convert_text_to_audio(question_to_ask_spanish,"audio_1_file.mp3")

        # load the voice into gradio audio output

        # wait until user input new audio and this is very critical
        # We can also check if the second audio is not equal to first one
        # get the audio and convert it into spanish text
        # convert the text spanish to english
        # append the new text to old one

        base_message  += message +"\n"
        # call this function recursivly until it return or 
        # we can the set the maximum recursive call as parameter like request_message(message,max_call = max_call -1)
        # Number and return the final message if max_call = 0
        return request_message(base_message)


