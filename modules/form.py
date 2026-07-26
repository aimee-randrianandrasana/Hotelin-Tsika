from datetime import datetime, timedelta
from utils.helpers import validate_client_data
from db.config import PRIX_CHAMBRE


def current_form_data(window):
    sejour = int(window.le_sejour.text().strip() or 0)
    arriver = datetime.today().date()
    depart = arriver + timedelta(days=sejour)
    classe = window.cb_classe.currentText().lower()
    prix_total = sejour * PRIX_CHAMBRE.get(classe, 12_000)
    return {
        "nom": window.le_nom.text().strip().upper(),
        "prenom": window.le_prenom.text().strip().capitalize(),
        "cin": window.le_cin.text().strip(),
        "genre": window.cb_genre.currentText().strip(),
        "classe": window.cb_classe.currentText().strip(),
        "chambre": window.sb_chambre.value(),
        "travail": window.le_travail.text().strip().capitalize(),
        "adresse": window.le_adresse.text().strip().upper(),
        "tel": window.le_tel.text().strip(),
        "email": window.le_email.text().strip(),
        "sejour": sejour,
        "arriver": arriver.strftime("%Y-%m-%d"),
        "depart": depart.strftime("%Y-%m-%d"),
        "prix_total": prix_total,
    }


def validate_form(window, data):
    return validate_client_data(window, data)
