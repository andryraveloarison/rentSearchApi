from flask import Blueprint, request, jsonify

import src.utils.loadData as loadData
import src.utils.basicFunction as basicFunc
from flask import Flask, request, jsonify
import re
from flask_cors import cross_origin
import os  # Ajouté ici pour corriger l'erreur "os not defined"
import io

bp = Blueprint('api_bp', __name__)

allLocations = loadData.allLocations
allMaterials = loadData.allMaterials
model = loadData.model

@bp.route('/', methods=['POST'])
@cross_origin()
#def classify(textInput):
def classify():

    text = request.json['text']
    #text = textInput.replace('.', '')

    
    # Recherche de mots-clés potentiels dans le texte
    materials = []
    place = []
    budgets=""
        
    words = text.split()

    pattern = r'(\d+(?:\s*(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)))'

    dates = re.findall(pattern, text)

    budgetPattern = r'(\d+(?:\s*(?:euros|euro|€)))'

    budget_amounts = re.findall(budgetPattern, text)

    for budget in budget_amounts:

        if len(budget.split()) > 1:
            if not budgets:
                budgets=budget.split()[0]+"-"
            else:
                budgets+=budget.split()[0]
            
        else:
            budget= budget.replace('€', '').replace('euros', '').replace('euro', '')
            if not budgets:
                budgets=budget+"-"
            else:
                budgets+=budget


    for word in words:
        if word.upper() in [mat.upper() for mat in allMaterials]:
            materials.append(word)

        if word.upper() in [loc.upper() for loc in allLocations]:
            place.append(word)   


    rep = basicFunc.generate_rep([materials, place, budgets,dates])


    return jsonify({
        'text': text,
        'materials': materials,
        'place': place,
        'budget': budgets,
        'date':dates,
        'reponse':rep
    })


@bp.route('/transcribe', methods=['POST'])
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



