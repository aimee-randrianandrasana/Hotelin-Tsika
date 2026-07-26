from PyQt5.QtWidgets import QMessageBox, QInputDialog
from .paiement import PayerWindow
from utils.employee_utils import build_update_data
from db.config import COEFF_GRADE, SALAIRE_BASE


def get_selected_employee_id(main_window):
    row = main_window.tableWidget_employees.currentRow()
    if row < 0:
        QMessageBox.warning(main_window, "Selection", "Aucun employe selectionne.")
        return None
    emp_id_item = main_window.tableWidget_employees.item(row, 0)
    if not emp_id_item or not emp_id_item.text().isdigit():
        QMessageBox.warning(main_window, "Erreur", "Impossible de recuperer l'ID")
        return None
    return int(emp_id_item.text())


def mark_absence(main_window):
    emp_id = get_selected_employee_id(main_window)
    if not emp_id:
        return

    emp = main_window.db1.get_employee_by_id(emp_id)
    if not emp:
        QMessageBox.warning(main_window, "Erreur", "Employe introuvable")
        return

    nb_absences = emp.get("nb_absences", 0) + 1
    salaire = emp["salaire"]
    if nb_absences % 5 == 0:
        salaire = int(salaire * 0.85)

    update_data = build_update_data(emp, nb_absences=nb_absences, salaire=salaire)
    main_window.db1.update_employee(emp_id, update_data)
    main_window.load_employees()

    QMessageBox.information(
        main_window, "Absence enregistree",
        f"{emp['nom']} {emp['prenom']} a maintenant {nb_absences} absence(s).",
    )


def modify_grade(main_window):
    emp_id = get_selected_employee_id(main_window)
    if not emp_id:
        return

    emp = main_window.db1.get_employee_by_id(emp_id)
    if not emp:
        QMessageBox.warning(main_window, "Erreur", "Employe introuvable.")
        return

    grades = list(COEFF_GRADE.keys())
    new_grade, ok = QInputDialog.getItem(
        main_window, "Modifier le grade", "Nouveau grade :", grades, editable=False,
    )
    if not ok:
        return

    poste = emp["poste"]
    new_salaire = int(SALAIRE_BASE.get(poste, 0) * COEFF_GRADE.get(new_grade, 1.0))

    main_window.db1.update_employee(emp_id, build_update_data(emp, salaire=new_salaire, grade=new_grade))
    QMessageBox.information(
        main_window, "Succes",
        f"Grade mis a jour : {new_grade}\nNouveau salaire : {new_salaire} Ar",
    )
    main_window.load_employees()


def fire_employee(main_window):
    emp_id = get_selected_employee_id(main_window)
    if not emp_id:
        return

    reply = QMessageBox.question(
        main_window, "Confirmer",
        "Voulez-vous vraiment renvoyer cet employe ?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    if reply == QMessageBox.StandardButton.Yes:
        main_window.db1.delete_employee(emp_id)
        QMessageBox.information(main_window, "Employe renvoye", "Employe supprime avec succes.")
        main_window.load_employees()


def open_payment(main_window):
    emp_id = get_selected_employee_id(main_window)
    if not emp_id:
        return

    emp = main_window.db1.get_employee_by_id(emp_id)
    if not emp:
        QMessageBox.warning(main_window, "Erreur", "Employe introuvable")
        return

    dialog = PayerWindow(main_window, emp)
    dialog.exec()
    main_window.load_employees()
