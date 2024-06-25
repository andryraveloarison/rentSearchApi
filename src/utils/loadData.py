import whisper
import json
from dotenv import load_dotenv
import os

allLocationsPath = "data/locations.json"
allMaterialsPath = "data/materials.json"
allMaterialsTradPath = "data/materialsTrad.json"

# Chargement des clés d'API à partir des variables d'environnement
def load_api_keys():
    api_keys = {}
    for key in os.environ:

        if key.startswith('API_KEY_'):
            api_keys[os.getenv(key)] = f'{key}'  # Description basée sur le nom de la variable
    return api_keys

def loadLocations(allLocationsPath):
    with open(allLocationsPath, 'r', encoding='utf-8') as file:
        allLocations = json.load(file)
    return allLocations

def loadMaterials(allMaterialsPath):
    with open(allMaterialsPath, 'r', encoding='utf-8') as file:
        allMaterials = json.load(file)
    return allMaterials

def loadMaterialsTrad(allMaterialsTradPath):
    with open(allMaterialsTradPath, 'r', encoding='utf-8') as file:
        allMaterialsTrad = json.load(file)
    return allMaterialsTrad

model = whisper.load_model('small')
allLocations = loadLocations(allLocationsPath)
allMaterials = loadMaterials(allMaterialsPath)
allMaterialsTrad = loadMaterialsTrad(allMaterialsTradPath)
authorized_keys = load_api_keys()
