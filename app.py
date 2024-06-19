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

allLocationsPath = "data/locations.json"
allMaterialsPath = "data/materials.json"

#processor = WhisperProcessor.from_pretrained("openai/whisper-small")
#model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")

def loadLocations(allLocationsPath):
    with open(allLocationsPath, 'r', encoding='utf-8') as file:
        allLocations = json.load(file)
    return allLocations 

def loadMaterials(allMaterialsPath):
    with open(allMaterialsPath, 'r', encoding='utf-8') as file:
        allMaterials = json.load(file)
    return allMaterials


def generate_rep(datas):
    # Liste de mots-clés potentiels
    keywords = ["le materiel", "le lieu", "les budgets", "les dates"]
    
    # Construction de la chaîne rep en fonction des listes materials, place, et budget_amount
    rep = ""
    i=0
    for data in datas:
        if not data:
            if not rep:
                rep="Veuillez préciser "+keywords[i]
            else:
                rep += ", "+keywords[i]
        i+=1

    if ',' in rep:
        repBefore, repAfter = rep.rsplit(',', 1)
        # Concatène les deux reps avec "et" entre elles
        rep = repBefore + ' et' + repAfter

    return rep


allLocations = loadLocations(allLocationsPath)
allMaterials = loadMaterials(allMaterialsPath)

model = whisper.load_model('small')

@app.route('/', methods=['POST'])
@cross_origin()
#def classify(textInput):
def classify():

    text = request.json['text']

    #text = textInput.replace('.', '')

    
    # Recherche de mots-clés potentiels dans le texte
    materials = []
    place = []
    budget_amount= []
        
    words = text.split()

    pattern = r'(\d+\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre))'

    dates = re.findall(pattern, text)

    budgetPattern = r'(\d+(?:\s*(?:euros|euro|€)))'

    budget_amounts = re.findall(budgetPattern, text)

    for budget in budget_amounts:

        if len(budget.split()) > 1:
            budget_amount.append(int(budget.split()[0]))
        else:
            budget= budget.replace('€', '').replace('euros', '').replace('euro', '')
            budget_amount.append(int(budget))

    

    for word in words:
        if word.upper() in [mat.upper() for mat in allMaterials]:
            materials.append(word)

        if word.upper() in [loc.upper() for loc in allLocations]:
            place.append(word)   


    rep = generate_rep([materials, place, budget_amount,dates])


    return jsonify({
        'text': text,
        'materials': materials,
        'place': place,
        'budget': budget_amount,
        'date':dates,
        'reponse':rep
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




