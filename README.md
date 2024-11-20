# Global Description

This is a SpeechBrain-based Automatic Speech Recognition (ASR) model for Tunisian Arabic.

---

# Pipeline Description

This ASR system is composed of multiple linked components:

### Acoustic Model
- **Model**: A pretrained `wavlm-large` model ([Microsoft WavLM Large](https://huggingface.co/microsoft/wavlm-large)) is combined with two fully connected layers and fine-tuned on a Tunisian Arabic dataset.
- **Decoder**: CTC (Connectionist Temporal Classification) greedy decoder.
- **Input Data**: Single-channel recordings resampled at 16 kHz (audio resampled from 8 kHz should work as well).

### Language Model
- **KenLM**: A 4-gram language model trained on the provided dataset's transcripts.
- **Integration**: Combines with the acoustic model to refine the transcription output.

---

# Data Formatting and Cleaning

### Preprocessing Pipeline
- **Audio Formatting**: 
  - Converts all audio files to a consistent format (16-bit PCM WAV) at 16 kHz.
  - Tools used: `sox` and custom Python scripts for batch processing.

- **Text Normalization**:
  - Removes unwanted characters and harmonizes variations in Tunisian Arabic text.
  - Normalizes diacritics and handles punctuation inconsistencies.

- **Data Augmentation**:
  - Adds slight noise or pitch shifts to audio for robustness.
  - Ensures the model generalizes to varied acoustic environments.

### Cleaning Steps
- **Outlier Removal**: Filters out audio files with excessive noise or too short durations.
- **Foreign Word Handling**: While the system struggles with foreign words, such segments in the training data are annotated to improve future versions.
- **Alignment Check**: Verifies that text transcriptions align correctly with the audio.

### Relevant Files
- `add_duration.py`: Script for adding duration to the csv.
- `add_ids.py`: Script for adding ids of recordings to the csv.
- `add_rate.py`: Script for adding wav sample rates of the recordings to the csv.
- `add_transcriptions.py`: Script for adding transcriptions manually to the csv (Recordings must be ordered by numbered names).

---

# Limitations

1. **Not enough data samples**: Due to the complexity of the unstructured dataset that we had to create, collect, clean and process. This model is not yet able to fully transcribe seamlessly. 
---
# Referencing Salah Zaiem (PhD Candidate): zaiemsalah@gmail.com for his amazing work on this matter.
# Referencing SpeechBrain

This work has no published paper yet and may never have one. If you use this model in an academic setting, please cite the original SpeechBrain paper:

```bibtex
@misc{SB2021,
    author = {Ravanelli, Mirco and Parcollet, Titouan and Rouhe, Aku and Plantinga, Peter and Rastorgueva, Elena and Lugosch, Loren and Dawalatabad, Nauman and Ju-Chieh, Chou and Heba, Abdel and Grondin, Francois and Aris, William and Liao, Chien-Feng and Cornell, Samuele and Yeh, Sung-Lin and Na, Hwidong and Gao, Yan and Fu, Szu-Wei and Subakan, Cem and De Mori, Renato and Bengio, Yoshua },
    title = {SpeechBrain},
    year = {2021},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\\url{https://github.com/speechbrain/speechbrain}},
}

