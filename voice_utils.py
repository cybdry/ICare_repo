#!/usr/bin/env python
# -*- coding: utf-8 -*-

import whisper
from gtts import gTTS


model = whisper.load_model("base")
audio_file = "openai_output.mp3"
language = "es"


def convert_audio_to_text(audio_voice):
    print("convert_audio_to_text called")

    audio = whisper.load_audio(audio_voice)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)

    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)
    result_text = result.text

    audio_obj = gTTS(text=result_text,
                     lang=language)
    audio_obj.save(audio_file)
    return result_text, audio_file


def convert_text_to_audio(text_t, language_t, audio_file):
    audio_obj = gTTS(text=text_t,
                     lang=language_t)
    audio_obj.save(audio_file)
    return audio_file
