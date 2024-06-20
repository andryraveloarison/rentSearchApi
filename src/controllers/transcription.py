import src.utils.loadData as loadData
import os
from flask import Flask, request, jsonify
import src.controllers.extraction as extraction

model = loadData.model

def transcribe(file_stream):

    file_size = len(file_stream.getvalue())

    # Sauvegarder temporairement le fichier audio
    filename = 'temp_audio.wav'

    with open(filename, 'wb') as f_out:
        f_out.write(file_stream.getvalue())

    print("transcription....")

    result = model.transcribe(filename, fp16=False)
    
    print("transcription finished")
    print(result['text'])
    # Supprimer le fichier audio temporaire
    os.remove(filename)
    
    return extraction.extract(result['text'])
