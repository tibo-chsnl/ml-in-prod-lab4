import unittest
from datetime import date, timedelta
from unittest.mock import patch
import os

from app import _build_postgres_uri
from models import User, Task

class TestUnit(unittest.TestCase):

    def test_task_is_overdue(self):
        past_date = date.today() - timedelta(days=1)
        task = Task(title="Test", due_date=past_date, is_completed=False)
        self.assertTrue(task.is_overdue())

        task.is_completed = True
        self.assertFalse(task.is_overdue())

        task.is_completed = False
        task.due_date = date.today()
        self.assertFalse(task.is_overdue())

        task.due_date = date.today() + timedelta(days=1)
        self.assertFalse(task.is_overdue())
        
        task.due_date = None
        self.assertFalse(task.is_overdue())

    def test_user_password_hashing(self):
        u = User(username="testuser")
        u.set_password("secret")
        
        self.assertNotEqual(u.password_hash, "secret")
        self.assertTrue(u.check_password("secret"))
        self.assertFalse(u.check_password("wrong"))

    @patch.dict(os.environ, {
        "POSTGRES_USER": "test_user",
        "POSTGRES_PASSWORD": "test_password",
        "POSTGRES_HOST": "test_host",
        "POSTGRES_PORT": "5432",
        "POSTGRES_DB": "test_db"
    }, clear=True)
    def test_build_postgres_uri(self):
        if "DATABASE_URL" in os.environ:
            del os.environ["DATABASE_URL"]
            
        uri = _build_postgres_uri()
        expected = "postgresql+psycopg2://test_user:test_password@test_host:5432/test_db"
        self.assertEqual(uri, expected)

    @patch.dict(os.environ, {"DATABASE_URL": "postgresql://custom:url@host:1234/db"})
    def test_build_postgres_uri_prefer_env_var(self):
        uri = _build_postgres_uri()
        self.assertEqual(uri, "postgresql://custom:url@host:1234/db")
