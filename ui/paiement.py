from PyQt5 import QtWidgets
from datetime import datetime
from utils.employee_utils import build_update_data


class PayerWindow(QtWidgets.QDialog):
    def __init__(self, main_window, emp):
        super().__init__(main_window)
        self.setWindowTitle("Paiement de salaire")
        self.setFixedSize(400, 300)
        self.emp = emp
        self.db1 = main_window.db1

        layout = QtWidgets.QVBoxLayout()

        salaire_base = emp["salaire"]
        absences = emp.get("nb_absences", 0)

        dernier_paiement = emp.get("dernier_paiement")
        if dernier_paiement:
            if isinstance(dernier_paiement, str):
                dernier = datetime.strptime(dernier_paiement, "%Y-%m-%d")
            else:
                dernier = dernier_paiement
        else:
            dernier = emp["date_embauche"]
            if isinstance(dernier, str):
                dernier = datetime.strptime(dernier, "%Y-%m-%d")

        today = datetime.today()
        nb_mois = (today.year - dernier.year) * 12 + (today.month - dernier.month)
        if nb_mois < 1:
            nb_mois = 1

        deduction_par_mois = int(salaire_base * 0.15 * (absences // 5))
        total_deduction = deduction_par_mois * nb_mois
        montant_total = salaire_base * nb_mois - total_deduction

        layout.addWidget(QtWidgets.QLabel(f"Nom : {emp['prenom']} {emp['nom']}"))
        layout.addWidget(QtWidgets.QLabel(f"Poste : {emp['poste']}"))
        layout.addWidget(QtWidgets.QLabel(f"Grade : {emp['grade']}"))
        layout.addWidget(QtWidgets.QLabel(f"Salaire mensuel : {salaire_base} Ar"))
        layout.addWidget(QtWidgets.QLabel(f"Absences : {absences}"))
        layout.addWidget(QtWidgets.QLabel(f"Retenue totale : {total_deduction} Ar"))
        layout.addWidget(QtWidgets.QLabel(f"Montant total ({nb_mois} mois) : {montant_total} Ar"))

        btn_payer = QtWidgets.QPushButton("Payer")
        btn_payer.clicked.connect(lambda: self.payer(nb_mois, montant_total))
        layout.addWidget(btn_payer)

        self.setLayout(layout)

    def payer(self, nb_mois, montant_total):
        today_str = datetime.today().strftime("%Y-%m-%d")
        update_data = build_update_data(
            self.emp,
            nb_absences=0,
            etat_paie=f"Paye {datetime.today().strftime('%Y-%m')}",
            dernier_paiement=today_str,
        )
        self.db1.update_employee(self.emp["id"], update_data)

        QtWidgets.QMessageBox.information(
            self,
            "Paiement effectue",
            f"Paiement pour {self.emp['prenom']} {self.emp['nom']} effectue ({nb_mois} mois).\n"
            f"Montant paye : {montant_total} Ar\n"
            f"Absences reinitialisees a 0.\n"
            f"Dernier paiement : {today_str}",
        )
        self.close()
