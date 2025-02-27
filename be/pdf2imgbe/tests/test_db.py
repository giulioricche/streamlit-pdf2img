import pytest

from pdf2imgbe.lib.model import Conversion
from pdf2imgbe.lib.statics import ConversionStatus


def test_conversion_get_all(sql_client, mock_sql_connection, sample_conversions):
    """Test conversion_get_all method returns all conversions correctly"""
    _, mock_cursor = mock_sql_connection
    mock_cursor.fetchall.return_value = [
        ("123", "test1.pdf", "RUNNING", sample_conversions[0]["start_date"]),
        ("456", "test2.pdf", "COMPLETED", sample_conversions[1]["start_date"]),
    ]
    mock_cursor.description = [
        ("id", None, None, None, None, None, None),
        ("filename", None, None, None, None, None, None),
        ("status", None, None, None, None, None, None),
        ("start_date", None, None, None, None, None, None),
    ]

    result = sql_client.conversion_get_all()
    mock_cursor.execute.assert_called_once_with("SELECT * FROM conversion")

    assert len(result) == 2
    assert all(isinstance(item, Conversion) for item in result)
    assert result[0].id == "123"
    assert result[0].filename == "test1.pdf"
    assert result[0].status == ConversionStatus.RUNNING
    assert result[1].id == "456"
    assert result[1].filename == "test2.pdf"
    assert result[1].status == ConversionStatus.COMPLETED


def test_conversion_get_by_id(sql_client, mock_sql_connection, mock_conversion):
    """Test conversion_get_by_id method returns the correct conversion"""
    _, mock_cursor = mock_sql_connection
    mock_cursor.fetchone.return_value = ("123", "test1.pdf", "RUNNING", mock_conversion["start_date"])
    mock_cursor.description = [
        ("id", None, None, None, None, None, None),
        ("filename", None, None, None, None, None, None),
        ("status", None, None, None, None, None, None),
        ("start_date", None, None, None, None, None, None),
    ]

    result = sql_client.conversion_get_by_id("123")
    mock_cursor.execute.assert_called_once_with("SELECT * FROM conversion WHERE id = %s", ("123",))

    assert isinstance(result, Conversion)
    assert result.id == "123"
    assert result.filename == "test1.pdf"
    assert result.status == ConversionStatus.RUNNING
    assert result.start_date == mock_conversion["start_date"]


def test_conversion_get_by_id_not_found(sql_client, mock_sql_connection):
    """Test error handling when conversion is not found"""
    _, mock_cursor = mock_sql_connection
    mock_cursor.fetchone.return_value = None

    with pytest.raises(Exception):
        sql_client.conversion_get_by_id("non_existent_id")
