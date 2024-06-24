import whisper
import json

allLocationsPath = "data/locations.json"
allMaterialsPath = "data/materials.json"
allMaterialsTradPath = "data/materialsTrad.json"

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