#!/usr/bin/env python
# -*- coding: utf-8 -*-

from request_info import request_message
from voice_utils import (convert_audio_to_text,
                         convert_text_to_audio,
                         audio_file)

from utils import user_requirement
import openai
import gradio as gr
import os
import whisper


openai.api_key = os.getenv("E_OPENAI_KEY")

message_from_box1 = " "
open_ai_output = " "

def chatgpt_api(input_text):
    messages = [
        {"role":"system","content":" "}
    ]
    if input_text:
        messages.append({
            "role":"user",
            "content":input_text
        })
        chat_completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",messages = messages
        )
        reply  = chat_completion.choices[0].messages.content
        return reply
    else:
        raise ValueError("Input must not be empty")

def get_api_wrappper(audio):
    print("get_api_wrappper functions is called")
    resut_text, audio_file = convert_audio_to_text(audio)
    get_user = user_requirement(resut_text)

    if not "Sorry, can we also have information about your" in get_user: 
        openai_output = chatgpt_api(get_user)


    if len(openai_output):
        translated = whisper.Whisper().translate(openai_output,"es")
        audio_file_spanish = convert_text_to_audio(translated,"es","openai_output.mp3")
    else:
        translated = whisper.Whisper().translate(get_user,"es")
        audio_file_spanish = convert_text_to_audio(translated,"es","openai_output.mp3")
        
    print("Seeeeeeee: ",[translated,openai_output,audio_file_spanish])

    return [translated,openai_output,audio_file_spanish]


def gradio_interface(): 
    output_1 = gr.Textbox(label = "Speech To Text(English)") 
    output_2 = gr.Textbox(label = "Api output")
    output_3 = gr.Audio(audio_file)
    inputs = ["mic"]

    gradio_launcher = gr.Interface(
        title = "ICare Web Interface",
        fn = get_api_wrappper, # Put the final functions here
        inputs = inputs,
        outputs = [
            output_1,output_2,output_3
        ],
        live = True)


    #if len(message_from_box1) == 0:

    #    if output_1.text:
    #        message_from_box1 = output_1.text
    #else:

    #    key,*values = user_requirement(message_from_box1)

    #    if key:
    #        openai_output = chatgpt_api(values[3])

    #        gradio_launcher = gr.Interface(
    #            title = "I-Care Web Interface",
    #            fn = get_api, # Put the final functions here
    #            inputs = [
    #                gr.inputs.Audio(source = "microphone", type = "filepath"),

    #                ],
    #            outputs = [
    #                output_1,output_2,output_3
    #            ],
    #            live = True)
    #    else:
    #        output_1.update(values[0])

    gradio_launcher.launch()

if __name__ == "__main__":
    gradio_interface()

