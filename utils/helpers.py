import re
from PyQt5.QtWidgets import QMessageBox


def validate_client_data(window, data):
    if not data.get("prenom") or not data.get("cin"):
        QMessageBox.warning(window, "Erreur", "Le prenom et le CIN sont obligatoires !")
        return False

    tel = str(data.get("tel", ""))
    if not (tel.isdigit() and len(tel) == 10):
        QMessageBox.warning(window, "Erreur", "Le telephone doit contenir exactement 10 chiffres !")
        return False

    cin = str(data.get("cin", ""))
    if not (cin.isdigit() and len(cin) == 12):
        QMessageBox.warning(window, "Erreur", "Le CIN doit contenir exactement 12 chiffres !")
        return False

    email = data.get("email", "").strip()
    if email:
        email_regex = r"^[\w.+-]+@[\w.-]+\.\w+$"
        if not re.match(email_regex, email):
            QMessageBox.warning(window, "Erreur", "Adresse email invalide !")
            return False

    return True


def validate_employee_data(self):
    cin = self.le_cin.text().strip()
    prenom = self.le_prenom.text().strip()

    if not prenom or not cin:
        QMessageBox.warning(self, "Erreur", "Le prenom et le CIN sont obligatoires.")
        return False

    if not (cin.isdigit() and len(cin) == 12):
        QMessageBox.warning(self, "Erreur", "Le CIN doit contenir exactement 12 chiffres.")
        return False

    tel = self.le_tel.text().strip()
    if tel and (not tel.isdigit() or len(tel) != 10):
        QMessageBox.warning(self, "Erreur", "Le telephone doit contenir exactement 10 chiffres.")
        return False

    email = self.le_email.text().strip()
    if email:
        email_regex = r"^[\w.+-]+@[\w.-]+\.\w+$"
        if not re.match(email_regex, email):
            QMessageBox.warning(self, "Erreur", "Adresse email invalide.")
            return False

    return True


def get_selected_row_id(self):
    selected_rows = self.table.selectionModel().selectedRows()
    if not selected_rows:
        return None
    row = selected_rows[0].row()
    try:
        item = self.table.item(row, 0)
        if item is None:
            return None
        return int(item.text())
    except (ValueError, AttributeError):
        return None
