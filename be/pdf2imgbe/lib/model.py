import typing as T
from datetime import datetime
from pydantic import BaseModel

from lib.statics import ConversionStatus


class Conversion(BaseModel):
    """
    Represents a conversion process.
    """

    id: str
    filename: str
    status: ConversionStatus
    start_date: datetime

    def from_dict(data: T.Dict[str, T.Any]):
        """
        Create a conversion from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary representation of the conversion.

        Returns
        -------
        Conversion
            Conversion object.
        """

        return Conversion(
            id=data["id"], filename=data["filename"], status=ConversionStatus(data["status"]), start_date=data["start_date"]
        )

    def to_dict(self):
        """
        Return the conversion as a dictionary.

        Returns
        -------
        dict
            Dictionary representation of the conversion.
        """

        return {"id": self.id, "filename": self.filename, "status": self.status.value, "start_date": self.start_date.isoformat()}


class ConversionResults(BaseModel):
    """
    Represents the results of a conversion process.
    """

    id: str
    images_bytes: T.List[str]

    def from_dict(data: T.Dict[str, T.Any]):
        """
        Create conversion results from a dictionary.

        Parameters
        ----------
        data : dict
            Dictionary representation of the conversion results.

        Returns
        -------
        ConversionResults
            Conversion results object.
        """

        return ConversionResults(id=data["id"], images_bytes=data["images_bytes"])

    def to_dict(self):
        """
        Return the conversion results as a dictionary.

        Returns
        -------
        dict
            Dictionary representation of the conversion results.
        """

        return {"id": self.id, "images_bytes": self.images_bytes}
