from pdf2imgfe.lib.log import logger

import os
import base64
import requests
import typing as T
from http import HTTPStatus
from streamlit.runtime.uploaded_file_manager import UploadedFile

from pdf2imgfe.lib.exception import ProcessException
from pdf2imgfe.lib.statics import EnvKey, ConversionStatus


class ConvertService:
    """
    Service to interact with the conversion API provided by the backend.
    """

    __APP_CONVERSION_ENDPOINT: str
    __APP_CONVERSION_RESULTS_ENDPOINT: str
    __AMS_ALL_CONVERSIONS_ENDPOINT: str

    def __init__(self):
        BE_URL = f"http://{os.getenv(EnvKey.BE_HOST_KEY)}:{os.getenv(EnvKey.BE_PORT_KEY)}"
        self.__APP_CONVERSION_ENDPOINT = f"{BE_URL}/app/conversion"
        self.__APP_CONVERSION_RESULTS_ENDPOINT = f"{BE_URL}/app/conversion/results"
        self.__AMS_ALL_CONVERSIONS_ENDPOINT = f"{BE_URL}/ams/conversion-table"

    def convert_pdf_to_images(self, pdf_file: UploadedFile) -> str:
        """
        Convert a PDF file to images.

        Parameters
        ----------
        pdf_file : UploadedFile
            PDF file to convert.

        Returns
        -------
        str
            Conversion ID

        Raises
        ------
        ProcessException
            If failed to upload PDF for conversion
        """

        logger.info("Requesting PDF conversion")
        files = {"pdf_file": (pdf_file.name, pdf_file.getvalue(), pdf_file.type)}
        response = requests.post(self.__APP_CONVERSION_ENDPOINT, files=files)
        logger.info(f"Response: {response.status_code}, {response}")
        if response.status_code == HTTPStatus.OK:
            id = response.json().get("id")
            return id
        else:
            raise ProcessException("Failed to upload PDF for conversion", response.status_code)

    def check_conversion_status(self, id: str) -> ConversionStatus:
        """
        Check the status of a conversion.

        Parameters
        ----------
        id : str
            ID of the conversion.

        Returns
        -------
        ConversionStatus
            Status of the conversion

        Raises
        ------
        ProcessException
            If failed to check conversion status
        """

        logger.info("Requesting conversion status")
        response = requests.get(self.__APP_CONVERSION_ENDPOINT, params={"id": id})
        logger.info(f"Response: {response.status_code}, {response}")
        if response.status_code == HTTPStatus.OK:
            status = response.json().get("status")
            return ConversionStatus(status)
        else:
            raise ProcessException("Failed to check conversion status", response.status_code)

    def get_conversion_results(self, id: str) -> T.List[bytes]:
        """
        Get the conversion results.

        Parameters
        ----------
        id : str
            ID of the conversion.

        Returns
        -------
        List[bytes]
            Images as bytes

        Raises
        ------
        ProcessException
            If failed to get conversion results
        """

        logger.info("Requesting conversion results")
        response = requests.get(self.__APP_CONVERSION_RESULTS_ENDPOINT, params={"id": id})
        logger.info(f"Response: {response.status_code}, {response}")
        if response.status_code == HTTPStatus.OK:
            images_bytes = response.json().get("images_bytes")
            images = [base64.b64decode(i) for i in images_bytes]
            return images
        else:
            raise ProcessException("Failed to get conversion results", response.status_code)

    def get_all_conversions(self) -> T.List[T.Dict[str, str]]:
        """
        Get all conversions.

        Returns
        -------
        List[Dict[str, str]]
            List of all conversions

        Raises
        ------
        ProcessException
            If failed to get conversion
        """

        logger.info("Requesting all conversions")
        response = requests.get(self.__AMS_ALL_CONVERSIONS_ENDPOINT)
        logger.info(f"Response: {response.status_code}, {response}")
        if response.status_code == HTTPStatus.OK:
            return response.json()
        else:
            raise ProcessException("Failed to get conversion table", response.status_code)
