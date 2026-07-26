from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from utils.helpers import validate_employee_data
from db.config import SALAIRE_BASE, COEFF_GRADE


class RecruitmentWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recrutement d'employe")
        self.setFixedSize(400, 450)
        self.db1 = parent.db1
        self.parent_window = parent

        layout = QtWidgets.QVBoxLayout()

        self.le_nom = QtWidgets.QLineEdit()
        self.le_nom.setPlaceholderText("Nom")
        self.le_prenom = QtWidgets.QLineEdit()
        self.le_prenom.setPlaceholderText("Prenom")
        self.le_cin = QtWidgets.QLineEdit()
        self.le_cin.setPlaceholderText("CIN")
        self.cb_poste = QtWidgets.QComboBox()
        self.cb_poste.addItems(list(SALAIRE_BASE.keys()))
        self.cb_grade = QtWidgets.QComboBox()
        self.cb_grade.addItems(list(COEFF_GRADE.keys()))
        self.date_embauche = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.date_embauche.setCalendarPopup(True)
        self.le_adresse = QtWidgets.QLineEdit()
        self.le_adresse.setPlaceholderText("Adresse")
        self.le_tel = QtWidgets.QLineEdit()
        self.le_tel.setPlaceholderText("Telephone")
        self.le_email = QtWidgets.QLineEdit()
        self.le_email.setPlaceholderText("Email")
        self.cb_etat_paie = QtWidgets.QComboBox()
        self.cb_etat_paie.addItems(["Paye", "Impaye"])

        for w in [
            self.le_nom, self.le_prenom, self.le_cin, self.cb_poste,
            self.cb_grade, self.date_embauche, self.le_adresse,
            self.le_tel, self.le_email, self.cb_etat_paie,
        ]:
            layout.addWidget(w)

        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_save = QtWidgets.QPushButton("Recruter")
        self.btn_cancel = QtWidgets.QPushButton("Annuler")
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_save.clicked.connect(self.save_employee)
        self.btn_cancel.clicked.connect(self.close)

    def save_employee(self):
        if not validate_employee_data(self):
            return

        poste = self.cb_poste.currentText()
        grade = self.cb_grade.currentText()
        salaire = int(SALAIRE_BASE[poste] * COEFF_GRADE[grade])

        data = {
            "nom": self.le_nom.text().strip().upper(),
            "prenom": self.le_prenom.text().strip().capitalize(),
            "cin": self.le_cin.text().strip(),
            "poste": poste,
            "grade": grade,
            "date_embauche": self.date_embauche.date().toString("yyyy-MM-dd"),
            "adresse": self.le_adresse.text().strip(),
            "tel": self.le_tel.text().strip(),
            "email": self.le_email.text().strip(),
            "nb_absences": 0,
            "etat_paie": self.cb_etat_paie.currentText(),
            "salaire": salaire,
        }

        self.db1.insert_employee(data)
        QMessageBox.information(self, "Succes", f"Employe {data['nom']} recrute avec succes.")
        if self.parent_window:
            self.parent_window.load_employees()
        self.close()
