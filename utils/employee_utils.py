def build_update_data(emp, nb_absences=None, salaire=None, grade=None, etat_paie=None, dernier_paiement=None):
    return {
        "nom": emp["nom"],
        "prenom": emp["prenom"],
        "cin": emp["cin"],
        "poste": emp["poste"],
        "salaire": salaire if salaire is not None else emp["salaire"],
        "date_embauche": emp["date_embauche"],
        "adresse": emp["adresse"],
        "tel": emp["tel"],
        "email": emp["email"],
        "nb_absences": nb_absences if nb_absences is not None else emp.get("nb_absences", 0),
        "etat_paie": etat_paie if etat_paie is not None else emp.get("etat_paie", "Unpaid"),
        "grade": grade if grade is not None else emp.get("grade", "Junior"),
        "dernier_paiement": dernier_paiement if dernier_paiement is not None else emp.get("dernier_paiement"),
    }
