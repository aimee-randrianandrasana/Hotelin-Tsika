# HotelManager

Desktop application for hotel management built with **PyQt5** and **MariaDB**.

## Features

- **Client management** — Register, update, delete, and archive hotel guests
- **Room allocation** — Automatic room assignment with availability checking
- **Employee management** — Recruit, promote, record absences, and process payments
- **Salary system** — Automatic salary calculation based on position and grade
- **History & archiving** — Deleted clients are archived for record-keeping
- **CSV export** — Export client and history data to CSV files
- **Search** — Real-time search with SQL queries across clients, history, and employees

## Tech Stack

| Layer | Technology |
|-------|-----------|
| GUI | PyQt5 (Qt5) |
| Database | MariaDB (via `mariadb` connector) |
| Data export | pandas |
| Config | python-dotenv |
| Tests | unittest |

## Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure database
cp .env.example .env
# Edit .env with your MariaDB credentials

# Run
python main.py
```

## Running Tests

```bash
python -m unittest discover -s tests -v
```

## Project Structure

```
HotelManager/
├── main.py                  # Application entry point
├── db/
│   ├── config.py            # Database config + salary constants
│   ├── connection.py        # Shared database connection
│   ├── database_clients.py  # Client CRUD + search operations
│   └── database_employees.py # Employee CRUD + search operations
├── ui/
│   ├── main_window.py       # Main window setup & event handling
│   ├── employee_manager.py  # Employee action handlers
│   ├── paiement.py          # Payment dialog
│   ├── recrutement.py       # Recruitment dialog
│   └── interface.ui         # Qt Designer UI definition
├── modules/
│   ├── crud.py              # Client add/update/delete logic
│   ├── display.py           # Table display & selection handlers
│   └── form.py              # Form data extraction & validation
├── utils/
│   ├── helpers.py           # Validation helpers
│   └── employee_utils.py    # Employee utility functions
├── tests/
│   ├── test_config.py       # Config & salary tests
│   ├── test_helpers.py      # Validation logic tests
│   └── test_employee_utils.py # Employee utils tests
├── .env.example             # Environment variable template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
└── README.md
```

## Database Schema

The application automatically creates the following tables:

- **`clients`** — Hotel guest reservations (name, CIN, room, dates, price)
- **`clients_archive`** — Archived (deleted) client records
- **`employees`** — Staff members (name, position, salary, grade, absences)

## Author

Randrianandrasana Jean Aime
