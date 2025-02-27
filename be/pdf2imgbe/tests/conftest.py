import os
from dotenv import load_dotenv

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env.local"))
load_dotenv(dotenv_path, override=True)

import pytest
import datetime
from unittest.mock import patch, MagicMock
from pdf2imgbe.services.db import SQLClient


@pytest.fixture
def mock_sql_connection():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    return mock_conn, mock_cursor


@pytest.fixture
def sql_client(mock_sql_connection):
    mock_conn, _ = mock_sql_connection
    with patch("pdf2imgbe.services.db.connect", return_value=mock_conn):
        client = SQLClient()
        return client


@pytest.fixture
def sample_conversions():
    now = datetime.datetime.now()
    return [
        {"id": "123", "filename": "test1.pdf", "status": "RUNNING", "start_date": now},
        {"id": "456", "filename": "test2.pdf", "status": "COMPLETED", "start_date": now},
    ]


@pytest.fixture
def mock_conversion():
    now = datetime.datetime.now()
    return {"id": "123", "filename": "test1.pdf", "status": "RUNNING", "start_date": now}
