from enum import Enum, auto
import os
import sys
import torch
import logging
import kenlm
import speechbrain as sb
from speechbrain.utils.distributed import run_on_main
from hyperpyyaml import load_hyperpyyaml
from pathlib import Path
import torchaudio.transforms as T
import torchaudio
import numpy as np
import gradio as gr
import langdetect
from pyctcdecode import build_ctcdecoder
torch.cuda.empty_cache()
print(torch.cuda.memory_stats())

hparams_file, run_opts, overrides = sb.parse_arguments(
    ["wavlm_partly_frozen.yaml"])
# print(torch.cuda.get_device_properties(0).total_memory)
# If distributed_launch=True then
# create ddp_group with the right communication protocol
sb.utils.distributed.ddp_init_group(run_opts)
print(torch.cuda.is_available())
print(torch.cuda.current_device())
# Replace "cuda:0" with the appropriate GPU identifier
torch.cuda.set_device("cuda:0")

with open(hparams_file, encoding="utf-8") as fin:
    hparams = load_hyperpyyaml(fin, overrides)

# Create experiment directory
sb.create_experiment_directory(
    experiment_directory=hparams["output_folder"],
    hyperparams_to_save=hparams_file,
    overrides=overrides,
)


def read_labels_file(labels_file):
    with open(labels_file, "r", encoding="utf-8") as lf:
        lines = lf.read().splitlines()
        division = "==="
        numbers = {}
        for line in lines:
            if division in line:
                break
            string, number = line.split("=>")
            number = int(number)
            string = string[1:-2]
            numbers[number] = string
        return [numbers[x] for x in range(len(numbers))]


labels = read_labels_file(os.path.join(
    hparams["save_folder"], "label_encoder.txt"))
print(labels)
labels = [""] + labels[1:]
print(len(labels))


# Dataset prep (parsing Librispeech)

resampler_8000 = T.Resample(8000, 16000, dtype=torch.float)
resampler_44100 = T.Resample(44100, 16000, dtype=torch.float)
resampler_48000 = T.Resample(48000, 16000, dtype=torch.float)


resamplers_val = {
    '8000': resampler_8000,
    '44100': resampler_44100,
    '48000': resampler_48000
}


def detect_language(segment):
    detected_language = "tn"
    return detected_language


kenlm_models = {
    "tn": "tunisian.arpa"
}


def segment_audio(audio):
    # Divide the audio into segments
    sr = 16000
    segment_duration = 5  # seconds
    num_samples = audio.size(0)
    samples_per_segment = int(segment_duration * sr)
    segments = []
    for start in range(0, num_samples, samples_per_segment):
        end = min(start + samples_per_segment, num_samples)
        segment = audio[start:end]
        segments.append(segment)
    return segments


class ASR(sb.Brain):
    def treat_wav(self, sig):
        transcriptions_with_languages = []
        torch.cuda.empty_cache()
        for segment in sig:  # Each segment is an audio tensor
            language = detect_language(segment)
            if language in kenlm_models:
                kenlm_model_path = kenlm_models[language]
                decoder = build_ctcdecoder(
                    labels,
                    kenlm_model_path=kenlm_model_path,
                    alpha=0.5,
                    beta=1,
                )

                # Process the segment
                feats = self.modules.wav2vec2(segment.to(self.device))
                x = self.modules.enc(feats)
                logits = self.modules.ctc_lin(x)
                p_ctc = self.hparams.log_softmax(logits)

                # Decode and add to transcriptions_with_languages
                segment_transcription = ""
                for logs in p_ctc:
                    text = decoder.decode(logs.detach().cpu().numpy())
                    segment_transcription += text + " "

                transcriptions_with_languages.append(
                    (segment_transcription, language))

                # Release GPU memory
                del segment, feats, x, logits, p_ctc
                torch.cuda.empty_cache()

        return transcriptions_with_languages


label_encoder = sb.dataio.encoder.CTCTextEncoder()


# We dynamicaly add the tokenizer to our brain class.
# NB: This tokenizer corresponds to the one used for the LM!!

run_opts["device"] = "cpu"
asr_brain = ASR(
    modules=hparams["modules"],
    hparams=hparams,
    run_opts=run_opts,
    checkpointer=hparams["checkpointer"],
)
description = """ this is a speechbrain-ASR model. /n
This model is not capable of treating other languages or dialects other than tunisian dialect, Despite the fact that tunisian dialect uses french and english on regular basis.
"""
title = "Focus Tunisian ASR testing"


asr_brain.device = "cpu"
asr_brain.modules.to("cpu")
asr_brain.tokenizer = label_encoder


asr_brain.on_evaluate_start()
asr_brain.modules.eval()


def treat_wav_file(file_mic, file_upload, resamplers=resamplers_val, asr=asr_brain, device="cpu"):
    torch.cuda.empty_cache()
    if (file_mic is not None) and (file_upload is not None):
        warn_output = "WARNING: You've uploaded an audio file and used the microphone. The recorded file from the microphone will be used and the uploaded audio will be discarded.\n"
        wav = file_mic
    elif (file_mic is None) and (file_upload is None):
        return "ERROR: You have to either use the microphone or upload an audio file"
    elif file_mic is not None:
        wav = file_mic
    else:
        wav = file_upload
    print('here aaa')
    sig, sr = torchaudio.load(wav)
    tensor_wav = sig.to(device)
    resampled = resamplers_val[str(sr)](tensor_wav)
    segments = segment_audio(resampled)
    transcriptions_with_languages = []
    for segment in segments:
        torch.cuda.empty_cache()
        transcriptions_with_languages.extend(asr_brain.treat_wav([segment]))

    recognized_sentence = ""
    for transcription, language in transcriptions_with_languages:
        recognized_sentence += transcription
    with open("output.txt", "w", encoding='utf-8') as f:
        f.write(recognized_sentence)
    return recognized_sentence


gr.Interface(
    fn=treat_wav_file,
    title=title,
    description=description,
    inputs=[
        gr.inputs.Audio(source="upload", type='filepath', optional=True)],
    outputs="text").launch()
