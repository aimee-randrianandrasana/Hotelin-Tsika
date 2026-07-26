from db.connection import get_connection
from db.config import DB_CLIENT, DB_ARCHIVE, DB_NAME

TABLE_KEYS = [
    "id", "nom", "prenom", "cin", "genre", "classe", "chambre", "travail",
    "adresse", "tel", "email", "sejour", "arriver", "depart", "prix_total",
]


class DatabaseClients:
    def __init__(self):
        self.conn = get_connection()
        self._ensure_tables()

    def _ensure_tables(self):
        cur = self.conn.cursor()
        cur.execute(f"USE `{DB_NAME}`;")
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS `{DB_CLIENT}` (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nom TEXT,
                prenom TEXT,
                cin TEXT, genre TEXT, classe TEXT, chambre INT,
                travail TEXT,
                adresse VARCHAR(50),
                tel TEXT, email VARCHAR(100),
                sejour INT,
                arriver DATE,
                depart DATE,
                prix_total INT DEFAULT 0
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        cur.execute(f"CREATE TABLE IF NOT EXISTS `{DB_ARCHIVE}` LIKE `{DB_CLIENT}`;")
        cur.close()

    def fetch_all(self, table=DB_CLIENT):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM `{table}` ORDER BY id;")
        rows = cur.fetchall()
        cur.close()
        return [dict(zip(TABLE_KEYS, row)) for row in rows]

    def search(self, text, table=DB_CLIENT):
        cur = self.conn.cursor()
        pattern = f"%{text}%"
        cur.execute(
            f"""SELECT * FROM `{table}` WHERE
                nom LIKE %s OR prenom LIKE %s OR cin LIKE %s OR
                classe LIKE %s OR adresse LIKE %s OR tel LIKE %s OR
                email LIKE %s OR travail LIKE %s
                ORDER BY id""",
            (pattern, pattern, pattern, pattern, pattern, pattern, pattern, pattern),
        )
        rows = cur.fetchall()
        cur.close()
        return [dict(zip(TABLE_KEYS, row)) for row in rows]

    def fetch_by_id(self, table, client_id):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM `{table}` WHERE id=%s", (client_id,))
        row = cur.fetchone()
        cur.close()
        if not row:
            return None
        return dict(zip(TABLE_KEYS, row))

    def insert(self, data):
        cur = self.conn.cursor()
        sql = f"""INSERT INTO `{DB_CLIENT}`
            (nom, prenom, cin, genre, classe, chambre, travail, adresse, tel, email, sejour, arriver, depart, prix_total)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cur.execute(sql, (
            data["nom"], data["prenom"], data["cin"], data["genre"],
            data["classe"], data["chambre"], data["travail"], data["adresse"],
            data["tel"], data["email"], data["sejour"], data["arriver"],
            data["depart"], data["prix_total"],
        ))
        cur.close()

    def update(self, client_id, data):
        cur = self.conn.cursor()
        sql = f"""UPDATE `{DB_CLIENT}` SET
            nom=%s, prenom=%s, cin=%s, genre=%s, classe=%s, chambre=%s,
            travail=%s, adresse=%s, tel=%s, email=%s, sejour=%s,
            arriver=%s, depart=%s, prix_total=%s
            WHERE id=%s"""
        cur.execute(sql, (
            data["nom"], data["prenom"], data["cin"], data["genre"], data["classe"], data["chambre"],
            data["travail"], data["adresse"], data["tel"], data["email"], data["sejour"],
            data["arriver"], data["depart"], data["prix_total"], client_id,
        ))
        cur.close()

    def delete(self, client_id):
        cur = self.conn.cursor()
        cur.execute(f"DELETE FROM `{DB_CLIENT}` WHERE id=%s", (client_id,))
        cur.close()

    def delete_all(self):
        cur = self.conn.cursor()
        cur.execute(f"TRUNCATE TABLE `{DB_CLIENT}`;")
        cur.close()

    def insert_archive(self, table, data):
        cur = self.conn.cursor()
        sql = f"""INSERT INTO `{table}`
            (nom, prenom, cin, genre, classe, chambre, travail, adresse, tel, email, sejour, arriver, depart, prix_total)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cur.execute(sql, (
            data.get("nom", ""), data.get("prenom", ""), data.get("cin", ""), data.get("genre", ""),
            data.get("classe", ""), data.get("chambre", 0), data.get("travail", ""), data.get("adresse", ""),
            data.get("tel", ""), data.get("email", ""), data.get("sejour", 0), data.get("arriver", None),
            data.get("depart", None), data.get("prix_total", 0),
        ))
        cur.close()

    def delete_all_history(self):
        cur = self.conn.cursor()
        cur.execute(f"TRUNCATE TABLE `{DB_ARCHIVE}`;")
        cur.close()
