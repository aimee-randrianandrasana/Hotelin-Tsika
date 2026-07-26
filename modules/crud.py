from PyQt5.QtWidgets import QMessageBox, QFileDialog
from db.config import DB_CLIENT, DB_ARCHIVE
from modules.form import current_form_data, validate_form
from modules.display import display_rows
from utils.helpers import get_selected_row_id
import pandas as pd


def add_client(window):
    data = current_form_data(window)
    if not validate_form(window, data):
        return

    cur = window.db.conn.cursor()
    query_check = """
        SELECT * FROM clients
        WHERE chambre = %s AND classe = %s
        AND (arriver <= %s AND depart >= %s)
    """
    cur.execute(query_check, (data["chambre"], data["classe"], data["depart"], data["arriver"]))
    existing = cur.fetchall()
    if existing:
        QMessageBox.warning(window, "Chambre occupee", f"La chambre {data["chambre"]} est deja reservee.")
        room_range = range(1, 21) if data["classe"].lower() == "vip" else range(1, 51)
        found = False
        for ch in room_range:
            cur.execute(query_check, (ch, data["classe"], data["depart"], data["arriver"]))
            if not cur.fetchall():
                data["chambre"] = ch
                found = True
                break
        if found:
            QMessageBox.information(window, "Suggestion", f"Chambre disponible {data["chambre"]} attribuee automatiquement.")
        else:
            QMessageBox.critical(window, "Complet", f"Desole, toutes les chambres {data["classe"]} sont occupees !")
            cur.close()
            return
    cur.close()

    confirm = QMessageBox.question(
        window,
        "Confirmer la reservation",
        f"Sejour de {data["sejour"]} jours en {data["classe"]}.\n"
        f"Chambre attribuee : {data["chambre"]}\n"
        f"Prix total : {data["prix_total"]} Ar\n\nConfirmer l ajout ?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    if confirm != QMessageBox.StandardButton.Yes:
        return

    window.db.insert(data)
    window.clear_form()
    display_rows(window, window.table, window.db.fetch_all(DB_CLIENT))
    display_rows(window, window.table_history, window.db.fetch_all(DB_ARCHIVE))
    QMessageBox.information(window, "Succes", "Client ajoute avec succes")


def update_client(window):
    selected = get_selected_row_id(window)
    if selected is None:
        QMessageBox.warning(window, "Attention", "Veuillez selectionner un client !")
        return
    data = current_form_data(window)
    if not validate_form(window, data):
        return
    window.db.update(selected, data)
    window.clear_form()
    display_rows(window, window.table, window.db.fetch_all(DB_CLIENT))
    display_rows(window, window.table_history, window.db.fetch_all(DB_ARCHIVE))
    QMessageBox.information(window, "Succes", "Client mis a jour avec succes")


def delete_client(window):
    selected = get_selected_row_id(window)
    if selected is None:
        QMessageBox.warning(window, "Attention", "Veuillez selectionner un client !")
        return
    confirm = QMessageBox.question(
        window, "Confirmer", "Supprimer ce client ?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    if confirm != QMessageBox.StandardButton.Yes:
        return
    client_data = window.db.fetch_by_id(DB_CLIENT, selected)
    if client_data:
        window.db.insert_archive(DB_ARCHIVE, client_data)
    window.db.delete(selected)
    window.clear_form()
    display_rows(window, window.table, window.db.fetch_all(DB_CLIENT))
    display_rows(window, window.table_history, window.db.fetch_all(DB_ARCHIVE))
    QMessageBox.information(window, "Succes", "Client supprime avec succes")


def delete_all_clients(window):
    confirm = QMessageBox.question(
        window, "Confirmer", "Supprimer tous les clients ?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    if confirm != QMessageBox.StandardButton.Yes:
        return
    all_clients = window.db.fetch_all(DB_CLIENT)
    for client in all_clients:
        window.db.insert_archive(DB_ARCHIVE, client)
    window.db.delete_all()
    window.clear_form()
    display_rows(window, window.table, window.db.fetch_all(DB_CLIENT))
    display_rows(window, window.table_history, window.db.fetch_all(DB_ARCHIVE))
    QMessageBox.information(window, "Succes", "Tous les clients supprimes et archives")


def delete_history(window):
    confirm = QMessageBox.question(
        window, "Confirmer", "Supprimer l historique ?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    if confirm != QMessageBox.StandardButton.Yes:
        return
    window.db.delete_all_history()
    window.clear_form()
    display_rows(window, window.table_history, window.db.fetch_all(DB_ARCHIVE))
    QMessageBox.information(window, "Succes", "Historique vide")


def export_csv(window):
    rows = window.db.fetch_all(DB_CLIENT)
    if not rows:
        QMessageBox.information(window, "Info", "Aucune donnee a exporter.")
        return
    path, _ = QFileDialog.getSaveFileName(window, "Exporter CSV", "", "Fichiers CSV (*.csv)")
    if not path:
        return
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False, encoding="utf-8")
    QMessageBox.information(window, "Succes", f"Exporte : {path}")


def export_csv_hist(window):
    rows = window.db.fetch_all(DB_ARCHIVE)
    if not rows:
        QMessageBox.information(window, "Info", "L historique est vide.")
        return
    path, _ = QFileDialog.getSaveFileName(window, "Exporter CSV", "", "Fichiers CSV (*.csv)")
    if not path:
        return
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False, encoding="utf-8")
    QMessageBox.information(window, "Succes", f"Exporte : {path}")
