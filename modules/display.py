from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


def display_rows(window, table, rows):
    if table is None:
        return

    table.setSortingEnabled(False)
    table.setRowCount(0)

    total_recette = 0

    for r_idx, row in enumerate(rows):
        table.insertRow(r_idx)
        for c_idx, key in enumerate(row.keys()):
            value = row.get(key, "")
            item = QTableWidgetItem(str(value) if value is not None else "")
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(r_idx, c_idx, item)

        if "prix_total" in row:
            prix_total = row.get("prix_total", 0)
            total_recette += prix_total

    table.setSortingEnabled(True)

    if hasattr(window, "table") and table == window.table:
        if hasattr(window, "affichage_compte"):
            window.affichage_compte.setText(f"{len(rows)} client(s)")
        if hasattr(window, "affichage_recette"):
            window.affichage_recette.setText(f"{total_recette} Ariary")
    if hasattr(window, "table") and table == window.tableWidget_history:
        if hasattr(window, "nb_historique"):
            window.nb_historique.setText(f"{len(rows)} personne(s)")


def display_rows_employees(table, rows):
    if table is None:
        return

    table.setSortingEnabled(False)
    table.setRowCount(0)

    for r_idx, row in enumerate(rows):
        table.insertRow(r_idx)
        for c_idx, key in enumerate(row.keys()):
            value = row.get(key, "")
            item = QTableWidgetItem(str(value) if value is not None else "")
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(r_idx, c_idx, item)

    table.setSortingEnabled(True)


def on_table_select(window, row, col):
    def get(c):
        item = window.table.item(row, c)
        return item.text() if item else ""

    window.le_nom.setText(get(1))
    window.le_prenom.setText(get(2))
    window.le_cin.setText(get(3))
    window.cb_genre.setCurrentText(get(4))
    window.cb_classe.setCurrentText(get(5))
    window.sb_chambre.setValue(int(get(6) or 1))
    window.le_travail.setText(get(7))
    window.le_adresse.setText(get(8))
    window.le_tel.setText(get(9))
    window.le_email.setText(get(10))
    window.le_sejour.setText(get(11))

    values = [get(1) + " " + get(2), get(3), get(5), get(11), get(8), get(12), get(13), get(7), get(6), get(9)]
    for i, val in enumerate(values, 1):
        attr = f"affichage_{i}"
        if hasattr(window, attr):
            getattr(window, attr).setText(val)


def on_table_select_history(window, row, col):
    def get(c):
        return window.table_history.item(row, c).text() if window.table_history.item(row, c) else ""

    values = [get(6), get(1), get(2), get(4), get(7), get(3), get(5), get(8), get(9), get(10), get(11), get(12), get(13)]
    for i, val in enumerate(values, 1):
        attr = f"affichage_h{i}"
        if hasattr(window, attr):
            getattr(window, attr).setText(val)


def on_table_select_employees(window, row, col):
    def get(c):
        item = window.tableWidget_employees.item(row, c)
        return item.text() if item else ""

    label_keys = [
        "info_1", "info_2", "info_3", "info_4",
        "info_5", "info_6", "info_7", "info_8",
        "info_9", "info_10", "info_11", "info_12", "info_13", "info_14",
    ]

    for i, key in enumerate(label_keys):
        if hasattr(window, key):
            getattr(window, key).setText(get(i))
