import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "hotel_app")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "hotel_db")

DB_CLIENT = "clients"
DB_ARCHIVE = "clients_archive"
DB_EMPLOYEE = "employees"

SALAIRE_BASE = {
    "Receptionniste": 400_000,
    "Serveur": 350_000,
    "Directeur": 800_000,
    "Maintenance": 300_000,
    "Cuisinier": 500_000,
}

COEFF_GRADE = {
    "Junior": 1.0,
    "Intermediaire": 1.2,
    "Senior": 1.5,
    "Directeur": 2.0,
}

PRIX_CHAMBRE = {
    "vip": 20_000,
    "classic": 12_000,
}
