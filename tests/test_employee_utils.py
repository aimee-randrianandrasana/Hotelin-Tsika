from utils.employee_utils import build_update_data


def test_build_update_data_defaults():
    emp = {
        "nom": "DUPONT",
        "prenom": "Jean",
        "cin": "123456789012",
        "poste": "Receptionist",
        "salaire": 400000,
        "date_embauche": "2024-01-15",
        "adresse": "123 rue Test",
        "tel": "0123456789",
        "email": "test@test.com",
        "nb_absences": 3,
        "etat_paie": "Unpaid",
        "grade": "Junior",
        "dernier_paiement": None,
    }
    result = build_update_data(emp)
    assert result["nom"] == "DUPONT"
    assert result["salaire"] == 400000
    assert result["nb_absences"] == 3
    assert result["etat_paie"] == "Unpaid"


def test_build_update_data_overrides():
    emp = {
        "nom": "DUPONT",
        "prenom": "Jean",
        "cin": "123456789012",
        "poste": "Receptionist",
        "salaire": 400000,
        "date_embauche": "2024-01-15",
        "adresse": "123 rue Test",
        "tel": "0123456789",
        "email": "test@test.com",
        "nb_absences": 3,
        "etat_paie": "Unpaid",
        "grade": "Junior",
        "dernier_paiement": None,
    }
    result = build_update_data(emp, salaire=500000, nb_absences=0, grade="Senior")
    assert result["salaire"] == 500000
    assert result["nb_absences"] == 0
    assert result["grade"] == "Senior"
    assert result["etat_paie"] == "Unpaid"
