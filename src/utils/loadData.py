
import whisper
import json

allLocationsPath = "data/locations.json"
allMaterialsPath = "data/materials.json"

def loadLocations(allLocationsPath):
    with open(allLocationsPath, 'r', encoding='utf-8') as file:
        allLocations = json.load(file)
    return allLocations

def loadMaterials(allMaterialsPath):
    with open(allMaterialsPath, 'r', encoding='utf-8') as file:
        allMaterials = json.load(file)
    return allMaterials


model = whisper.load_model('small')
allLocations = loadLocations(allLocationsPath)
allMaterials = loadMaterials(allMaterialsPath)