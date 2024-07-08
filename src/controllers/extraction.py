from flask import jsonify
import src.utils.loadData as loadData
import src.utils.basicFunction as basicFunc
import re

allLocations = loadData.allLocations
allMaterials = loadData.allMaterials
allLocationsTrad = loadData.allMaterialsTrad

def extract(textInput):

    text = textInput.replace('.', '')

    # Expression régulière pour trouver "ou" suivi d'un nombre qui pourrait être une date
    pattern = r"(ou)\s(\d{1,2})"

    # Fonction de remplacement qui remplace "ou" par "aout" uniquement si le nombre suit
    replacement_function = lambda match: f"{match.group(1)}aout" if int(match.group(2)) <= 31 else match.group(0)

    # Remplacer les occurrences selon la fonction de remplacement
    texte_modifié = re.sub(pattern, replacement_function, text)

    print(texte_modifié)


    # Recherche de mots-clés potentiels dans le texte
    materials = []
    places = []
    material = ""
    place = ""
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
            material = word
            materials.append(word)

        if word.upper() in [loc.upper() for loc in allLocations]:
            place = word
            places.append(word)

    rep = basicFunc.generate_rep([materials, places])
    
    return jsonify({
        'text': text,
        'material': material,
        'place': place,
        'budget': budgets,
        'reponse' :rep
    })


    #AVEC LES DATES
    """
    rep = basicFunc.generate_rep([materials, place, budgets ,dates])
    

    return jsonify({
        'text': text,
        'materials': materials,
        'place': place,
        'budget': budgets,
        'date' :dates,
        'reponse' :rep
    })
    """
