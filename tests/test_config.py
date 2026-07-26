import sys
import unittest
from unittest.mock import MagicMock


mock_qtwidgets = MagicMock()
sys.modules["PyQt5"] = MagicMock()
sys.modules["PyQt5.QtWidgets"] = mock_qtwidgets
sys.modules["PyQt5.QtCore"] = MagicMock()

sys.modules["dotenv"] = MagicMock()
sys.modules["mariadb"] = MagicMock()
sys.modules["pandas"] = MagicMock()

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))


from utils.employee_utils import build_update_data
from db.config import SALAIRE_BASE, COEFF_GRADE, PRIX_CHAMBRE


class TestBuildUpdateData(unittest.TestCase):
    def setUp(self):
        self.emp = {
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

    def test_defaults_keep_original_values(self):
        result = build_update_data(self.emp)
        self.assertEqual(result["nom"], "DUPONT")
        self.assertEqual(result["salaire"], 400000)
        self.assertEqual(result["nb_absences"], 3)
        self.assertEqual(result["etat_paie"], "Unpaid")

    def test_overrides_applied(self):
        result = build_update_data(self.emp, salaire=500000, nb_absences=0, grade="Senior")
        self.assertEqual(result["salaire"], 500000)
        self.assertEqual(result["nb_absences"], 0)
        self.assertEqual(result["grade"], "Senior")

    def test_etat_paie_override(self):
        result = build_update_data(self.emp, etat_paie="Paid 2026-07")
        self.assertEqual(result["etat_paie"], "Paid 2026-07")

    def test_dernier_paiement_override(self):
        result = build_update_data(self.emp, dernier_paiement="2026-07-15")
        self.assertEqual(result["dernier_paiement"], "2026-07-15")


class TestSalaireBase(unittest.TestCase):
    def test_keys(self):
        expected = {"Receptionniste", "Serveur", "Directeur", "Maintenance", "Cuisinier"}
        self.assertEqual(set(SALAIRE_BASE.keys()), expected)

    def test_all_positive(self):
        for poste, salaire in SALAIRE_BASE.items():
            self.assertGreater(salaire, 0, f"Salaire for {poste} must be positive")


class TestCoeffGrade(unittest.TestCase):
    def test_keys(self):
        expected = {"Junior", "Intermediaire", "Senior", "Directeur"}
        self.assertEqual(set(COEFF_GRADE.keys()), expected)

    def test_values_ordered(self):
        self.assertEqual(COEFF_GRADE["Junior"], 1.0)
        self.assertEqual(COEFF_GRADE["Intermediaire"], 1.2)
        self.assertEqual(COEFF_GRADE["Senior"], 1.5)
        self.assertEqual(COEFF_GRADE["Directeur"], 2.0)


class TestPrixChambre(unittest.TestCase):
    def test_vip(self):
        self.assertEqual(PRIX_CHAMBRE["vip"], 20_000)

    def test_classic(self):
        self.assertEqual(PRIX_CHAMBRE["classic"], 12_000)


class TestSalaryCalculation(unittest.TestCase):
    def test_all_combinations_positive(self):
        for poste, base in SALAIRE_BASE.items():
            for grade, coeff in COEFF_GRADE.items():
                expected = int(base * coeff)
                self.assertGreater(expected, 0, f"Salary {poste}/{grade} must be positive")


if __name__ == "__main__":
    unittest.main()
