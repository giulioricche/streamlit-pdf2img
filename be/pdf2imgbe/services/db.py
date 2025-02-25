from lib.log import logger

import os
import typing as T
from psycopg2 import connect, OperationalError

from lib.statics import ConversionStatus
from lib.model import Conversion


class SQLClient:
    """
    SQL client to interact with the database.
    """

    _sql_connection: object
    TABLE_NAME = "conversion"

    def __init__(self):
        try:
            self._sql_connection = connect(
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
                host=os.environ["DB_SERVICE_HOST"],
                port=os.environ["DB_SERVICE_PORT"],
            )
            logger.info("Database connection established successfully.")
        except OperationalError as e:
            logger.info(f"Failed to connect to the database: {e}")

    def conversion_get_all(self) -> T.List[Conversion]:
        """
        Get all conversions from the database.

        Returns
        -------
        List[Conversion]
            List of all conversions.
        """

        logger.info("Fetching all conversions")
        with self._sql_connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self.TABLE_NAME}")
            conversions = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
            return [Conversion.from_dict(dict(zip(col_names, c))) for c in conversions]

    def conversion_create(self, conversion: Conversion):
        """
        Create a conversion record in the database.

        Parameters
        ----------
        conversion : Conversion
            Conversion to create.
        """

        logger.info(f"Creating conversion record for ID: {conversion.id}")
        with self._sql_connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {self.TABLE_NAME} (id, filename, status, start_date) VALUES (%s, %s, %s, %s)",
                (conversion.id, conversion.filename, conversion.status.value, conversion.start_date),
            )
            self._sql_connection.commit()

    def conversion_get_by_id(self, id: str) -> Conversion:
        """
        Get a conversion by its unique identifier.

        Parameters
        ----------
        id : str
            Unique identifier of the conversion.

        Returns
        -------
        Conversion
            Status of the conversion.
        """

        logger.info(f"Fetching conversion for ID: {id}")
        with self._sql_connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self.TABLE_NAME} WHERE id = %s", (id,))
            conversion = cursor.fetchone()
            col_names = [desc[0] for desc in cursor.description]
            return Conversion.from_dict(dict(zip(col_names, conversion)))

    def conversion_update_status(self, id: str, status: ConversionStatus):
        """
        Update the status of a conversion.

        Parameters
        ----------
        id : str
            Unique identifier of the conversion.
        status : ConversionStatus
            New status of the conversion.
        """

        logger.info(f"Updating status for ID: {id} to {status}")
        with self._sql_connection.cursor() as cursor:
            cursor.execute(f"UPDATE {self.TABLE_NAME} SET status = %s WHERE id = %s", (status.value, id))
            self._sql_connection.commit()
