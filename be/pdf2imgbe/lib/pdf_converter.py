from lib.log import logger

import os
import asyncio
import pdf2image

from services.db import SQLClient
from lib.exception import ProcessException
from lib.model import Conversion
from lib.statics import EnvKey, ConversionStatus, IMAGE_FILENAME_FORMAT, IMAGE_FILE_EXTENSION


async def convert_pdf_to_images(sql_client: SQLClient, conversion: Conversion, file_content: bytes, output_path: str):
    """
    Convert a PDF file to images through the pdf2image library, register the conversion in the database, and save the images in the output path.

    Parameters
    ----------
    sql_client : SQLClient
        SQL client to interact with the database.
    id : str
        ID of the conversion.
    file_content : bytes
        Content of the PDF file.
    filename : str
        Name of the PDF file.
    output_path : str
        Path to save the images.

    Raises
    ------
    ProcessException
        If failed to convert the PDF to images or save the images.
    """

    logger.info(f"Converting PDF to images for ID: {conversion.id}")

    try:
        try:
            simulate_process_delay = int(os.getenv(EnvKey.SIMULATE_PROCESS_DELAY_KEY))
            if simulate_process_delay > 0:
                logger.info(f"Simulating process delay: {simulate_process_delay} seconds")
                await asyncio.sleep(simulate_process_delay)
            images = pdf2image.convert_from_bytes(file_content)
        except Exception as e:
            status = ConversionStatus.FAILED
            raise ProcessException(f"Failed to convert PDF to images: {e}", 500)
        try:
            os.makedirs(output_path)
            for i, image in enumerate(images):
                image.save(f"{output_path}/{IMAGE_FILENAME_FORMAT.format(i)}", IMAGE_FILE_EXTENSION)
        except Exception as e:
            status = ConversionStatus.FAILED
            raise ProcessException(f"Failed to save converted images: {e}", 500)
        status = ConversionStatus.COMPLETED
    finally:
        sql_client.conversion_update_status(conversion.id, status)

    logger.info(f"Conversion completed for ID: {conversion.id}")
