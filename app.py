from flask import Flask, request, jsonify
import json
import re
from flask_cors import cross_origin
import os  # Ajouté ici pour corriger l'erreur "os not defined"
import io
from pydub import AudioSegment
import whisper



#import speech_recognition as sr

app = Flask(__name__)

locationsPath = "data/locations.json"
materialsPath = "data/materials.json"

#processor = WhisperProcessor.from_pretrained("openai/whisper-small")
#model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")

def loadLocations(locationsPath):
    with open(locationsPath, 'r', encoding='utf-8') as file:
        locations = json.load(file)
    return locations 

def loadMaterials(materialsPath):
    with open(materialsPath, 'r', encoding='utf-8') as file:
        materials = json.load(file)
    return materials


months_abbr = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']

locations = loadLocations(locationsPath)
materials = loadMaterials(materialsPath)

model = whisper.load_model('small')

@cross_origin()  # Autorise les requêtes CORS pour cette route
def classify(textInput):
    
    text = textInput.replace('.', '')

    # Recherche de mots-clés potentiels dans le texte
    instruments = []
    lieu = []
    budget_amount= []
    words = text.split()

    pattern = r'(\d+\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre))'

    matches = re.findall(pattern, text)
    budgetPattern = r'(\d+\s+(?:euros|euro|€))'

    budget_amounts = re.findall(budgetPattern, text)

    for budget in budget_amounts:
        budget_amount.append(int(budget.split()[0]))
    

    for word in words:
        if word.upper() in [mat.upper() for mat in materials]:
            instruments.append(word)

        if word.upper() in [loc.upper() for loc in locations]:
            lieu.append(word)   

    return jsonify({
        'text': text,
        'instrument': instruments,
        'lieu': lieu,
        'budget': budget_amount,
        'date':matches
    })


@app.route('/transcribe', methods=['POST'])
@cross_origin()  # Autorise les requêtes CORS pour cette route
def transcribe_file():
    # Récupérer le fichier audio de la requête

    if 'audio' not in request.files:
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

    
    return classify(result['text'])



if __name__ == '__main__':
    app.run(debug=True)




