from db.connection import get_connection
from db.config import DB_EMPLOYEE, DB_NAME, SALAIRE_BASE, COEFF_GRADE

TABLE_KEYS = [
    "id", "nom", "prenom", "cin", "poste", "salaire", "date_embauche",
    "adresse", "tel", "email", "nb_absences", "etat_paie", "grade", "dernier_paiement",
]


class DatabaseEmployees:
    def __init__(self):
        self.conn = get_connection()
        self._ensure_tables()

    def _ensure_tables(self):
        cur = self.conn.cursor()
        cur.execute(f"USE `{DB_NAME}`;")
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS `{DB_EMPLOYEE}` (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(50),
                prenom VARCHAR(50),
                cin VARCHAR(20),
                poste VARCHAR(50),
                salaire INT,
                date_embauche DATE,
                adresse VARCHAR(100),
                tel VARCHAR(20),
                email VARCHAR(100),
                nb_absences INT DEFAULT 0,
                etat_paie VARCHAR(20) DEFAULT 'Unpaid',
                grade VARCHAR(20) DEFAULT 'Junior',
                dernier_paiement DATE DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        cur.close()

    def fetch_all_employees(self):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM `{DB_EMPLOYEE}` ORDER BY id;")
        rows = cur.fetchall()
        cur.close()
        return [dict(zip(TABLE_KEYS, row)) for row in rows]

    def search_employees(self, text):
        cur = self.conn.cursor()
        pattern = f"%{text}%"
        cur.execute(
            f"""SELECT * FROM `{DB_EMPLOYEE}` WHERE
                nom LIKE %s OR prenom LIKE %s OR cin LIKE %s OR
                poste LIKE %s OR grade LIKE %s OR etat_paie LIKE %s OR
                adresse LIKE %s OR tel LIKE %s OR email LIKE %s
                ORDER BY id""",
            (pattern, pattern, pattern, pattern, pattern, pattern, pattern, pattern, pattern),
        )
        rows = cur.fetchall()
        cur.close()
        return [dict(zip(TABLE_KEYS, row)) for row in rows]

    def get_employee_by_id(self, emp_id):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * FROM `{DB_EMPLOYEE}` WHERE id=%s", (emp_id,))
        row = cur.fetchone()
        cur.close()
        if not row:
            return None
        return dict(zip(TABLE_KEYS, row))

    def insert_employee(self, data):
        cur = self.conn.cursor()
        poste = data.get("poste", "Receptionist")
        grade = data.get("grade", "Junior")
        salaire = int(SALAIRE_BASE.get(poste, 0) * COEFF_GRADE.get(grade, 1.0))
        sql = f"""
            INSERT INTO `{DB_EMPLOYEE}`
            (nom, prenom, cin, poste, grade, date_embauche, adresse, tel, email, nb_absences, salaire, etat_paie)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cur.execute(sql, (
            data["nom"], data["prenom"], data["cin"], poste, grade,
            data["date_embauche"], data.get("adresse", ""), data.get("tel", ""), data.get("email", ""),
            data.get("nb_absences", 0), salaire, data.get("etat_paie", "Unpaid"),
        ))
        cur.close()

    def update_employee(self, emp_id, data):
        cur = self.conn.cursor()
        sql = f"""
            UPDATE `{DB_EMPLOYEE}` SET
            nom=%s, prenom=%s, cin=%s, poste=%s, salaire=%s, date_embauche=%s,
            adresse=%s, tel=%s, email=%s, nb_absences=%s, etat_paie=%s, grade=%s, dernier_paiement=%s
            WHERE id=%s
        """
        cur.execute(sql, (
            data["nom"], data["prenom"], data["cin"], data["poste"], data["salaire"],
            data["date_embauche"], data["adresse"], data["tel"], data["email"],
            data.get("nb_absences", 0), data.get("etat_paie", "Unpaid"), data.get("grade", "Junior"),
            data.get("dernier_paiement"), emp_id,
        ))
        cur.close()

    def delete_employee(self, emp_id):
        cur = self.conn.cursor()
        cur.execute(f"DELETE FROM `{DB_EMPLOYEE}` WHERE id=%s", (emp_id,))
        cur.close()
