---
title: Tunisian Asr
emoji: 🐠
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 3.16.1
app_file: app.py
pinned: false
license: cc-by-nc-3.0
---
# Global description 

This is a speechbrain-based Automatic Speech Recognition (ASR) model for Tunisian arabic. It outputs tunisian transcriptions in arabic language. Since the language is unwritten, the transcriptions may vary. This model is the work of Salah Zaiem, PhD candidate, contact : zaiemsalah@gmail.com


# Pipeline description
This ASR system is composed of 2 different but linked blocks:
- Acoustic model (wavlm-large + CTC). A pretrained wavlm-larhe model (https://huggingface.co/microsoft/wavlm-large) is combined with two DNN layers and finetuned on a tunisian arabic dataset.
- KenLM based 4-gram language model, learned on the training data.
The obtained final acoustic representation is given to the CTC greedy decoder.
The system is trained with single channel recordings resampled at  16 khz. (The model should be good with audio resampled from 8khz)

#Limitations 
Due to the nature of the available training data, the model may encounter issues when dealing with foreign words. So while it is common for Tunisian speakers to use (mainly french) foreign words, these will lead to more errors, we are working on improving this in further models. 

Run is done on CPU to keep it free in this space. This leads to quite long running times on long sequences. If for your project or research, you want to transcribe long sequences, feel free to drop an email here : zaiemsalah@gmail.com 

# Referencing SpeechBrain

This work has no published paper yet, and may never have. If you use it in an academic setting, please cite the original SpeechBrain paper : 
```
@misc{SB2021,
    author = {Ravanelli, Mirco and Parcollet, Titouan and Rouhe, Aku and Plantinga, Peter and Rastorgueva, Elena and Lugosch, Loren and Dawalatabad, Nauman and Ju-Chieh, Chou and Heba, Abdel and Grondin, Francois and Aris, William and Liao, Chien-Feng and Cornell, Samuele and Yeh, Sung-Lin and Na, Hwidong and Gao, Yan and Fu, Szu-Wei and Subakan, Cem and De Mori, Renato and Bengio, Yoshua },
    title = {SpeechBrain},
    year = {2021},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\\\\url{https://github.com/speechbrain/speechbrain}},
  }
```


