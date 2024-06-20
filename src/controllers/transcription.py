import src.utils.loadData as loadData
import os
import io
from flask import Flask, request, jsonify
import src.controllers.extraction as extraction

model = loadData.model

def transcribe(audio_file):
    # Récupérer le fichier audio de la requête

    if 'audio' not in audio_file.files:
        return jsonify({"message": "No audio file part"}), 400

    audio_file = request.files['audio']
    file_type = audio_file.content_type

    file_stream = io.BytesIO(audio_file.read())
    file_size = len(file_stream.getvalue())
    
    print(f"Type de fichier: {file_type}")
    print(f"Taille du fichier: {file_size} octets")

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
    print("transcription_segments")
    return extraction.extract(result['text'])
