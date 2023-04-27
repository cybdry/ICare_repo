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
from googletrans import Translator


openai.api_key = "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"

message_from_box1 = " "
open_ai_output = " "

translator = Translator()


def chatgpt_api(input_text):
    messages = [
        {"role": "system", "content": " "}
    ]
    if input_text:
        messages.append({
            "role": "user",
            "content": input_text
        })
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat_completion.choices[0].message.content
        return reply
    else:
        raise ValueError("Input must not be empty")


def get_api_wrappper(audio):
    print("get_api_wrappper functions is called")
    resut_text, audio_file = convert_audio_to_text(audio)
    key, *get_user = user_requirement(resut_text)
    print("Get user", get_user)
    global open_ai_output

    if key:
        open_ai_output = chatgpt_api(get_user[0])

        translated = translator.translate(
            open_ai_output, src="en", dest="es").text
        audio_file_spanish = convert_text_to_audio(
            translated, "es", "openai_output.mp3")

    else:
        print("English: ", get_user[0])
        translated = translator.translate(
            get_user[1], src="en", dest="es").text
        print("Translated text: ", translated)

        audio_file_spanish = convert_text_to_audio(
            translated, "es", "openai_output.mp3")

    return [translated, open_ai_output, audio_file_spanish]


def gradio_interface():
    output_1 = gr.Textbox(label="Speech To Text(English)")
    output_2 = gr.Textbox(label="Api output")
    output_3 = gr.Audio(audio_file)

    gradio_launcher = gr.Interface(
        title="ICare Web Interface",
        fn=get_api_wrappper,  # Put the final functions here
        inputs=gr.inputs.Audio(source="microphone", type="filepath"),
        outputs=[
            output_1, output_2, output_3
        ],
        live=True)

    gradio_launcher.launch()


if __name__ == "__main__":
    gradio_interface()
