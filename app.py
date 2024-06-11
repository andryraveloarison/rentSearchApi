from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

locationsPath = "data/locations.json"
materialsPath = "data/materials.json"


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



if __name__ == '__main__':
    app.run(debug=True)




