from flask import Flask, request, jsonify
import json
import re
from flask_cors import cross_origin
import os  # Ajouté ici pour corriger l'erreur "os not defined"
import speech_recognition as sr
import io



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



locations = loadLocations(locationsPath)
materials = loadMaterials(materialsPath)


@app.route('/', methods=['POST'])
@cross_origin()  # Autorise les requêtes CORS pour cette route
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

    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.record(source)  # read the entire audio file                  
        print("Transcription: " + r.recognize_google(audio))

    print("transcription finished")

    # Supprimer le fichier audio temporaire
    #os.remove(filename)
    print("transcription_segments")

    return jsonify({"message": "transcription"})



if __name__ == '__main__':
    app.run(debug=True)




