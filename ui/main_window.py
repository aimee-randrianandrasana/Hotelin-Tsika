from pathlib import Path
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPalette, QColor

from db.database_clients import DatabaseClients
from db.database_employees import DatabaseEmployees
from modules.crud import add_client, update_client, delete_client, delete_all_clients
from modules.crud import export_csv, delete_history, export_csv_hist
from modules.display import display_rows, on_table_select, on_table_select_history, on_table_select_employees
from db.config import DB_CLIENT, DB_ARCHIVE, DB_EMPLOYEE
from .recrutement import RecruitmentWindow
from .employee_manager import modify_grade, mark_absence, fire_employee, open_payment

STYLE = """
/* ── Global (Bleu tres sombre) ── */
QMainWindow, QDialog {
    background-color: #0a1628;
    color: #c8d6e5;
    font-family: 'Segoe UI', 'Noto Sans', sans-serif;
    font-size: 13px;
}

/* ── Labels ── */
QLabel {
    color: #8899aa;
    font-size: 13px;
}

/* ── LineEdits / SpinBox ── */
QLineEdit, QSpinBox, QDateEdit {
    background-color: #111d32;
    color: #c8d6e5;
    border: 1px solid #1c2d44;
    border-radius: 6px;
    padding: 7px 12px;
    font-size: 13px;
    selection-background-color: #2a4060;
}
QLineEdit:focus, QSpinBox:focus, QDateEdit:focus {
    border: 1px solid #3a5a80;
}

/* ── ComboBox ── */
QComboBox {
    background-color: #111d32;
    color: #c8d6e5;
    border: 1px solid #1c2d44;
    border-radius: 6px;
    padding: 7px 12px;
    font-size: 13px;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox QAbstractItemView {
    background-color: #111d32;
    color: #c8d6e5;
    selection-background-color: #1c2d44;
    border: 1px solid #2a4060;
}

/* ── Tables ── */
QTableWidget {
    background-color: #0a1628;
    alternate-background-color: #0e1f36;
    color: #c8d6e5;
    gridline-color: #111d32;
    border: 1px solid #152540;
    border-radius: 6px;
    font-size: 13px;
    selection-background-color: #1c2d44;
    selection-color: #ffffff;
}
QTableWidget::item {
    padding: 5px 10px;
}
QTableWidget::item:selected {
    background-color: #2a4060;
    color: #ffffff;
}
QHeaderView::section {
    background-color: #111d32;
    color: #6a8aaa;
    border: none;
    border-bottom: 1px solid #1c2d44;
    padding: 8px 10px;
    font-weight: bold;
    font-size: 13px;
}

/* ── Buttons (default) ── */
QPushButton {
    background-color: #111d32;
    color: #8899aa;
    border: 1px solid #1c2d44;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #1c2d44;
    color: #c8d6e5;
}
QPushButton:pressed {
    background-color: #2a4060;
}

/* ── Ajouter / Exporter (vert doux) ── */
QPushButton#btn_add, QPushButton#btn_export, QPushButton#btn_export_history {
    background-color: #0e2a1e;
    color: #6aaa7a;
    border: 1px solid #1a4a30;
}
QPushButton#btn_add:hover, QPushButton#btn_export:hover, QPushButton#btn_export_history:hover {
    background-color: #1a4a30;
    color: #c8d6e5;
}

/* ── Supprimer / Renvoyer (rouge doux) ── */
QPushButton#btn_delete, QPushButton#btn_delete_all, QPushButton#btn_delete_history, QPushButton#btn_renvoyer {
    background-color: #2a1218;
    color: #aa6a6a;
    border: 1px solid #4a1a2a;
}
QPushButton#btn_delete:hover, QPushButton#btn_delete_all:hover, QPushButton#btn_delete_history:hover, QPushButton#btn_renvoyer:hover {
    background-color: #4a1a2a;
    color: #c8d6e5;
}

/* ── Modifier / Mettre a jour (bleu doux) ── */
QPushButton#btn_update, QPushButton#btn_modifier_grade {
    background-color: #0e1a2e;
    color: #6a8aba;
    border: 1px solid #1a3050;
}
QPushButton#btn_update:hover, QPushButton#btn_modifier_grade:hover {
    background-color: #1a3050;
    color: #c8d6e5;
}

/* ── Payer salaire (mauve doux) ── */
QPushButton#btn_payer {
    background-color: #1a1428;
    color: #8a7aaa;
    border: 1px solid #302050;
}
QPushButton#btn_payer:hover {
    background-color: #302050;
    color: #c8d6e5;
}

/* ── Presence (jaune doux) ── */
QPushButton#btn_presence {
    background-color: #282410;
    color: #aa9a5a;
    border: 1px solid #4a4020;
}
QPushButton#btn_presence:hover {
    background-color: #4a4020;
    color: #c8d6e5;
}

/* ── Recruter (teal doux) ── */
QPushButton#btn_add_emp {
    background-color: #0e2020;
    color: #6aaa9a;
    border: 1px solid #1a4040;
}
QPushButton#btn_add_emp:hover {
    background-color: #1a4040;
    color: #c8d6e5;
}

/* ── Annuler (outline doux) ── */
QPushButton#btn_cancel {
    background: transparent;
    color: #4a6a8a;
    border: 1px solid #4a6a8a;
}
QPushButton#btn_cancel:hover {
    background-color: #4a6a8a;
    color: #0a1628;
}

/* ── Navigation ── */
QPushButton#btn_home, QPushButton#btn_home_2, QPushButton#btn_history, QPushButton#btn_employer {
    background-color: #111d32;
    color: #5a7a9a;
    border: 1px solid #1c2d44;
    border-radius: 8px;
    padding: 10px 22px;
    font-size: 14px;
    font-weight: bold;
}
QPushButton#btn_home:hover, QPushButton#btn_home_2:hover, QPushButton#btn_history:hover, QPushButton#btn_employer:hover {
    background-color: #1c2d44;
    color: #7a9aba;
    border: 1px solid #2a4060;
}

/* ── Scrollbar ── */
QScrollBar:vertical {
    background: #0a1628;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #1c2d44;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #2a4060;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* ── Stacked Widget ── */
QStackedWidget {
    background: transparent;
}

/* ── Info labels clients (bleu clair doux) ── */
QLabel#affichage_1, QLabel#affichage_2, QLabel#affichage_3,
QLabel#affichage_4, QLabel#affichage_5, QLabel#affichage_6,
QLabel#affichage_7, QLabel#affichage_8, QLabel#affichage_9,
QLabel#affichage_10, QLabel#affichage_11, QLabel#affichage_12,
QLabel#affichage_13 {
    color: #7a9aba;
    font-weight: bold;
    font-size: 14px;
}

/* ── Info labels historique (corail doux) ── */
QLabel#affichage_h1, QLabel#affichage_h2, QLabel#affichage_h3,
QLabel#affichage_h4, QLabel#affichage_h5, QLabel#affichage_h6,
QLabel#affichage_h7, QLabel#affichage_h8, QLabel#affichage_h9,
QLabel#affichage_h10, QLabel#affichage_h11, QLabel#affichage_h12,
QLabel#affichage_h13 {
    color: #aa8080;
    font-weight: bold;
    font-size: 14px;
}

/* ── Info labels employes (lavande doux) ── */
QLabel#info_1, QLabel#info_2, QLabel#info_3, QLabel#info_4,
QLabel#info_5, QLabel#info_6, QLabel#info_7, QLabel#info_8,
QLabel#info_9, QLabel#info_10, QLabel#info_11, QLabel#info_12,
QLabel#info_13, QLabel#info_14 {
    color: #8a7aaa;
    font-weight: bold;
    font-size: 14px;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = Path(__file__).resolve().parent / "interface.ui"
        uic.loadUi(str(ui_path), self)

        self.setStyleSheet(STYLE)

        # ---------------- DATABASE ----------------
        self.db = DatabaseClients()
        self.db1 = DatabaseEmployees()

        # ---------------- TABLES ----------------
        self.table = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.table_history = self.findChild(QtWidgets.QTableWidget, "tableWidget_history")
        self.tableWidget_employees = self.findChild(QtWidgets.QTableWidget, "tableWidget_employees")

        tables = []
        if self.table:
            tables.append(self.table)
        if self.table_history:
            tables.append(self.table_history)

        for t in tables:
            t.setColumnCount(15)
            t.setHorizontalHeaderLabels([
                "", "Nom", "Prenom", "CIN", "Genre", "Classe", "Chambre",
                "Profession", "Adresse", "Telephone", "Email", "Nuit(s)", "Arrivee", "Depart", "Recette",
            ])
            t.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            t.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
            t.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.SingleSelection)
            t.setColumnHidden(0, True)

        if self.tableWidget_employees:
            self.tableWidget_employees.setColumnCount(14)
            self.tableWidget_employees.setHorizontalHeaderLabels([
                "", "Nom", "Prenom", "CIN", "Poste", "Salaire",
                "Embauche le", "Adresse", "Telephone", "Email", "Absences", "Statut paie", "Grade", "Dernier paiement",
            ])
            self.tableWidget_employees.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
            self.tableWidget_employees.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
            self.tableWidget_employees.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.SingleSelection)
            self.tableWidget_employees.setColumnHidden(0, True)

        # ---------------- TABLE CLICK ----------------
        if self.table:
            self.table.cellClicked.connect(lambda r, c: on_table_select(self, r, c))
        if self.table_history:
            self.table_history.cellClicked.connect(lambda r, c: on_table_select_history(self, r, c))
        if self.tableWidget_employees:
            self.tableWidget_employees.cellClicked.connect(lambda row, col: on_table_select_employees(self, row, col))

        # ---------------- CLIENT FORM ----------------
        self.le_nom = self.findChild(QtWidgets.QLineEdit, "le_nom")
        self.le_prenom = self.findChild(QtWidgets.QLineEdit, "le_prenom")
        self.le_cin = self.findChild(QtWidgets.QLineEdit, "le_cin")
        self.cb_genre = self.findChild(QtWidgets.QComboBox, "cb_genre")
        self.cb_classe = self.findChild(QtWidgets.QComboBox, "cb_classe")
        self.sb_chambre = self.findChild(QtWidgets.QSpinBox, "sb_chambre")
        self.le_travail = self.findChild(QtWidgets.QLineEdit, "le_travail")
        self.le_adresse = self.findChild(QtWidgets.QLineEdit, "le_adresse")
        self.le_tel = self.findChild(QtWidgets.QLineEdit, "le_tel")
        self.le_email = self.findChild(QtWidgets.QLineEdit, "le_email")
        self.le_sejour = self.findChild(QtWidgets.QLineEdit, "le_sejour")

        # ---------------- SEARCH ----------------
        self.lineEdit_4 = self.findChild(QtWidgets.QLineEdit, "lineEdit_4")
        self.lineEdit_recherche_history = self.findChild(QtWidgets.QLineEdit, "lineEdit_recherche_history")
        self.recherche_emp = self.findChild(QtWidgets.QLineEdit, "recherche_emp")
        self.lineEdit_4.textChanged.connect(self.search_clients)
        self.lineEdit_recherche_history.textChanged.connect(self.search_history)
        self.recherche_emp.textChanged.connect(self.search_employees)

        # ---------------- CLIENT BUTTONS ----------------
        self.btn_add = self.findChild(QtWidgets.QPushButton, "btn_add")
        self.btn_update = self.findChild(QtWidgets.QPushButton, "btn_update")
        self.btn_delete = self.findChild(QtWidgets.QPushButton, "btn_delete")
        self.btn_delete_all = self.findChild(QtWidgets.QPushButton, "btn_delete_all")
        self.btn_cancel = self.findChild(QtWidgets.QPushButton, "btn_cancel")
        self.btn_exit = self.findChild(QtWidgets.QPushButton, "btn_exit")

        self.btn_add.clicked.connect(lambda: add_client(self))
        self.btn_update.clicked.connect(lambda: update_client(self))
        self.btn_delete.clicked.connect(lambda: delete_client(self))
        self.btn_delete_all.clicked.connect(lambda: delete_all_clients(self))
        if self.btn_cancel:
            self.btn_cancel.clicked.connect(self.clear_form)
        if self.btn_exit:
            self.btn_exit.clicked.connect(self.close)

        # ---------------- IMPORT/EXPORT BUTTONS ----------------
        self.btn_export = self.findChild(QtWidgets.QPushButton, "btn_export")
        self.btn_export_history = self.findChild(QtWidgets.QPushButton, "btn_export_history")
        self.btn_delete_history = self.findChild(QtWidgets.QPushButton, "btn_delete_history")
        self.btn_add_emp = self.findChild(QtWidgets.QPushButton, "btn_add_emp")
        self.btn_modifier_grade = self.findChild(QtWidgets.QPushButton, "btn_modifier_grade")
        self.btn_presence = self.findChild(QtWidgets.QPushButton, "btn_presence")
        self.btn_renvoyer = self.findChild(QtWidgets.QPushButton, "btn_renvoyer")
        self.btn_payer = self.findChild(QtWidgets.QPushButton, "btn_payer")

        self.btn_export.clicked.connect(lambda: export_csv(self))
        self.btn_export_history.clicked.connect(lambda: export_csv_hist(self))
        self.btn_delete_history.clicked.connect(lambda: delete_history(self))
        self.btn_add_emp.clicked.connect(self.open_recruitment_window)
        if self.btn_modifier_grade:
            self.btn_modifier_grade.clicked.connect(lambda: modify_grade(self))
        if self.btn_renvoyer:
            self.btn_renvoyer.clicked.connect(lambda: fire_employee(self))
        if self.btn_presence:
            self.btn_presence.clicked.connect(lambda: mark_absence(self))
        if self.btn_payer:
            self.btn_payer.clicked.connect(lambda: open_payment(self))

        # ---------------- NAVIGATION ----------------
        self.stackedWidget = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
        self.btn_history = self.findChild(QtWidgets.QPushButton, "btn_history")
        self.btn_employer = self.findChild(QtWidgets.QPushButton, "btn_employer")
        self.btn_home = self.findChild(QtWidgets.QPushButton, "btn_home")
        self.btn_home_2 = self.findChild(QtWidgets.QPushButton, "btn_home_2")
        self.btn_history.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btn_employer.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.btn_home.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btn_home_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        # ---------------- LOAD DATA ----------------
        self.load_clients()
        self.load_history()
        self.load_employees()

    def load_clients(self):
        rows = self.db.fetch_all(DB_CLIENT)
        display_rows(self, self.table, rows)

    def load_history(self):
        rows = self.db.fetch_all(DB_ARCHIVE)
        display_rows(self, self.table_history, rows)

    def load_employees(self):
        table = self.tableWidget_employees
        if not table:
            return
        rows = self.db1.fetch_all_employees()
        display_rows(self, table, rows)
        if hasattr(self, "nb_employer"):
            self.nb_employer.setText(f"{len(rows)} employee(s)")

    # ---------------- FORM ----------------
    def clear_form(self):
        for w in [self.le_nom, self.le_prenom, self.le_cin, self.le_travail, self.le_adresse, self.le_tel, self.le_email, self.le_sejour]:
            if w:
                w.clear()
        if self.cb_genre:
            self.cb_genre.setCurrentIndex(0)
        if self.cb_classe:
            self.cb_classe.setCurrentIndex(0)
        if self.sb_chambre:
            self.sb_chambre.setValue(1)
        for i in range(1, 14):
            attr = f"affichage_{i}"
            if hasattr(self, attr):
                getattr(self, attr).setText("................")
            attr_h = f"affichage_h{i}"
            if hasattr(self, attr_h):
                getattr(self, attr_h).setText("................")

    # ---------------- SEARCH ----------------
    def search_clients(self, text):
        rows = self.db.search(text.strip()) if text.strip() else self.db.fetch_all(DB_CLIENT)
        display_rows(self, self.table, rows)

    def search_history(self, text):
        rows = self.db.search(text.strip(), DB_ARCHIVE) if text.strip() else self.db.fetch_all(DB_ARCHIVE)
        display_rows(self, self.table_history, rows)

    def search_employees(self, text):
        rows = self.db1.search_employees(text.strip()) if text.strip() else self.db1.fetch_all_employees()
        display_rows(self, self.tableWidget_employees, rows)

    # ---------------- RECRUITMENT WINDOW ----------------
    def open_recruitment_window(self):
        dialog = RecruitmentWindow(self)
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            self.load_employees()
