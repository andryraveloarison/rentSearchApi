
from flask import jsonify
import src.utils.loadData as loadData
import src.utils.basicFunction as basicFunc
import re


allLocations = loadData.allLocations
allMaterials = loadData.allMaterials

def extract(textInput):

    text = textInput.replace('.', '')

    # Recherche de mots-clés potentiels dans le texte
    materials = []
    place = []
    budgets =""

    words = text.split()

    pattern = r'(\d+(?:\s*(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)))'

    dates = re.findall(pattern, text)

    budgetPattern = r'(\d+(?:\s*(?:euros|euro|€)))'

    budget_amounts = re.findall(budgetPattern, text)

    for budget in budget_amounts:

        if len(budget.split()) > 1:
            if not budgets:
                budgets = budget.split()[0 ] +"-"
            else:
                budgets += budget.split()[0]

        else:
            budget= budget.replace('€', '').replace('euros', '').replace('euro', '')
            if not budgets:
                budgets = budget +"-"
            else:
                budgets += budget


    for word in words:
        if word.upper() in [mat.upper() for mat in allMaterials]:
            materials.append(word)

        if word.upper() in [loc.upper() for loc in allLocations]:
            place.append(word)


    rep = basicFunc.generate_rep([materials, place, budgets ,dates])


    return jsonify({
        'text': text,
        'materials': materials,
        'place': place,
        'budget': budgets,
        'date' :dates,
        'reponse' :rep
    })

