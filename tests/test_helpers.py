import sys
import unittest
from unittest.mock import MagicMock


mock_qtwidgets = MagicMock()
sys.modules["PyQt5"] = MagicMock()
sys.modules["PyQt5.QtWidgets"] = mock_qtwidgets
sys.modules["PyQt5.QtCore"] = MagicMock()
sys.modules["dotenv"] = MagicMock()
sys.modules["mariadb"] = MagicMock()
sys.modules["pandas"] = MagicMock()

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))


from utils.helpers import validate_client_data, validate_employee_data


def _make_window():
    return object()


class _FakeWidget:
    def __init__(self, text):
        self._text = text
    def text(self):
        return self._text
    def strip(self):
        return self._text.strip()


def _make_form(cin="123456789012", prenom="Jean", tel="", email=""):
    class F:
        pass
    f = F()
    f.le_cin = _FakeWidget(cin)
    f.le_prenom = _FakeWidget(prenom)
    f.le_tel = _FakeWidget(tel)
    f.le_email = _FakeWidget(email)
    return f


class TestValidateClientData(unittest.TestCase):
    def test_valid_data(self):
        data = {"prenom": "Jean", "cin": "123456789012", "tel": "0123456789", "email": "jean@test.com"}
        self.assertTrue(validate_client_data(_make_window(), data))

    def test_missing_prenom(self):
        data = {"prenom": "", "cin": "123456789012", "tel": "0123456789"}
        self.assertFalse(validate_client_data(_make_window(), data))

    def test_missing_cin(self):
        data = {"prenom": "Jean", "cin": "", "tel": "0123456789"}
        self.assertFalse(validate_client_data(_make_window(), data))

    def test_invalid_tel_length(self):
        data = {"prenom": "Jean", "cin": "123456789012", "tel": "123"}
        self.assertFalse(validate_client_data(_make_window(), data))

    def test_invalid_tel_non_digit(self):
        data = {"prenom": "Jean", "cin": "123456789012", "tel": "abcdefghij"}
        self.assertFalse(validate_client_data(_make_window(), data))

    def test_invalid_cin_length(self):
        data = {"prenom": "Jean", "cin": "12345", "tel": "0123456789"}
        self.assertFalse(validate_client_data(_make_window(), data))

    def test_invalid_email(self):
        data = {"prenom": "Jean", "cin": "123456789012", "tel": "0123456789", "email": "notanemail"}
        self.assertFalse(validate_client_data(_make_window(), data))

    def test_empty_email_ok(self):
        data = {"prenom": "Jean", "cin": "123456789012", "tel": "0123456789", "email": ""}
        self.assertTrue(validate_client_data(_make_window(), data))

    def test_various_valid_emails(self):
        for email in ["test@test.com", "a.b@c.fr", "user+tag@domain.org"]:
            data = {"prenom": "Jean", "cin": "123456789012", "tel": "0123456789", "email": email}
            self.assertTrue(validate_client_data(_make_window(), data), f"Email {email} should be valid")


class TestValidateEmployeeData(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(validate_employee_data(_make_form()))

    def test_missing_prenom(self):
        self.assertFalse(validate_employee_data(_make_form(prenom="")))

    def test_missing_cin(self):
        self.assertFalse(validate_employee_data(_make_form(cin="")))

    def test_invalid_cin_length(self):
        self.assertFalse(validate_employee_data(_make_form(cin="12345")))

    def test_invalid_tel_length(self):
        self.assertFalse(validate_employee_data(_make_form(tel="123")))

    def test_invalid_email(self):
        self.assertFalse(validate_employee_data(_make_form(email="bad")))

    def test_empty_tel_ok(self):
        self.assertTrue(validate_employee_data(_make_form(tel="")))


if __name__ == "__main__":
    unittest.main()
