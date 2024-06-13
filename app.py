from flask import Flask, request, jsonify
import json
import re
from flask_cors import cross_origin
import os  # Ajouté ici pour corriger l'erreur "os not defined"
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import Audio, load_dataset
#import speech_recognition as sr

app = Flask(__name__)

locationsPath = "data/locations.json"
materialsPath = "data/materials.json"

processor = WhisperProcessor.from_pretrained("openai/whisper-medium")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium")



def loadLocations(locationsPath):
    with open(locationsPath, 'r', encoding='utf-8') as file:
        locations = json.load(file)
    return locations 

def loadMaterials(materialsPath):
    with open(materialsPath, 'r', encoding='utf-8') as file:
        materials = json.load(file)
    return materials



locations = loadLocations(locationsPath)
materials = loadMaterials(materialsPath)


@app.route('/', methods=['POST'])
def classify():
    
    text = request.json['text']

    # Recherche de mots-clés potentiels dans le texte
    instruments = []
    lieu = []
    budget_amount= []

    words = text.split()

    for word in words:
        if word.upper() in [mat.upper() for mat in materials]:
            instruments.append(word)

        if word.upper() in [loc.upper() for loc in locations]:
            lieu.append(word)   

        match = re.search(r'(entre\s*\d+-\d*(?:euro|€)\set\s*\d+-\d*(?:euro|€))|(?:\d+(?:\.\d+)?(?:euro|€))', word)
        if match:
            budget_amount.append(float(match.group(0).replace('€', '').replace('$', '').replace('euro','')))

    return jsonify({
        'instrument': instruments,
        'lieu': lieu,
        'budget': budget_amount
    })


@app.route('/transcribe', methods=['POST'])
@cross_origin()  # Autorise les requêtes CORS pour cette route
def transcribe_file():
    print("test")
    # Récupérer le fichier audio de la requête
    audio_file = request.files['audio']

    # Sauvegarder temporairement le fichier audio
    filename = 'temp_audio.wav'
    audio_file.save(filename)
    # Charger l'audio avec librosa
    y, sr = librosa.load(filename, sr=None)

    # Préparer l'audio pour le modèle Whisper
    input_features = processor(y, sampling_rate=sr, return_tensors="pt").input_features

    # Générer les IDs de tokens
    forced_decoder_ids = processor.get_decoder_prompt_ids(language="french", task="transcribe")
    predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)

    # Déchiffrer les IDs de tokens en texte
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

    # Supprimer le fichier audio temporaire
    os.remove(filename)

    return jsonify({"message": transcription})



if __name__ == '__main__':
    app.run(debug=True)




