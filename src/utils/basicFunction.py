
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
