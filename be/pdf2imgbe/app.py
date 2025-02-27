from pdf2imgbe.lib.log import logger

import os
import re
import base64
import uvicorn
import typing as T
from uuid import uuid4
from http import HTTPStatus
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks

from pdf2imgbe.services.db import SQLClient
from pdf2imgbe.lib.pdf_converter import convert_pdf_to_images
from pdf2imgbe.lib.model import Conversion, ConversionResults
from pdf2imgbe.lib.statics import RESULTS_FOLDER, IMAGE_FILENAME_FORMAT, ConversionStatus


# Initialize the app
app = FastAPI(
    title="PDF2IMG-be",
    description="PDF to Image Converter Backend. This API allows you to convert PDF files to images, check the status of the conversion process, and retrieve the converted images.",
    version="0.0.1",
)
sql_client = SQLClient()
if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)


@app.get("/ams/health", tags=["AMS"], description="Health check endpoint.")
def health_check() -> T.Dict[str, str]:
    """
    Health check endpoint.

    Returns
    -------
    dict
        Status of the application.
    """

    logger.info("Recevied request: health_check")
    return {"status": "ok"}


@app.get("/ams/conversion-table", tags=["AMS"], description="Retrieve the conversion table from the database.")
async def get_conversions() -> T.List[Conversion]:
    """
    Retrieve the conversion table from the database.

    Returns
    -------
    conversions : list
        List of conversions.
    """

    logger.info("Recevied request: get_conversions")
    conversions = sql_client.conversion_get_all()
    return conversions


@app.post("/app/conversion", tags=["APP"], description="Convert a PDF file to images.")
async def post_conversion(
    background_tasks: BackgroundTasks, pdf_file: T.Annotated[UploadFile, File(description="The PDF file read as UploadFile")]
) -> Conversion:
    """
    Convert a PDF file to images.

    Parameters
    ----------
    background_tasks : BackgroundTasks
        Background tasks to handle the conversion process.
    pdf_file : UploadFile
        PDF file to convert.

    Returns
    -------
    conversion : Conversion
        Conversion representation.

    Raises
    ------
    HTTPException
        If the file is missing or not a PDF file.
    """

    logger.info("Recevied request: post_conversion")
    if not pdf_file or pdf_file.content_type != "application/pdf":
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Invalid file type. Only PDF files are accepted.")

    id = str(uuid4())
    file_content = await pdf_file.read()
    output_path = f"{RESULTS_FOLDER}/{id}"
    conversion = Conversion(id=id, filename=pdf_file.filename, status=ConversionStatus.RUNNING, start_date=datetime.now())

    sql_client.conversion_create(conversion)
    background_tasks.add_task(convert_pdf_to_images, sql_client, conversion, file_content, output_path)

    return conversion


@app.get("/app/conversion", tags=["APP"], description="Get the conversion with the provided ID.")
async def get_conversion(id: str) -> Conversion:
    """
    Get the conversion with the provided ID.

    Parameters
    ----------
    id : str
        ID of the conversion.

    Returns
    -------
    conversion : Conversion
        Conversion representation.

    Raises
    ------
    HTTPException
        If the ID is missing or not found.
    """

    logger.info("Recevied request: get_conversion")
    if not id:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Missing ID.")
    conversion = sql_client.conversion_get_by_id(id)
    if conversion is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="ID not found.")
    return conversion


@app.get("/app/conversion/results", tags=["APP"], description="Retrieve the converted images.")
async def get_conversion_results(id: str) -> ConversionResults:
    """
    Retrieve the converted images.

    Parameters
    ----------
    id : str
        ID of the conversion.

    Returns
    -------
    conversion_results : ConversionResults
        Conversion results representation

    Raises
    ------
    HTTPException
        If the ID is missing, not found, or the conversion is not completed yet.
    """

    logger.info("Recevied request: get_conversion_results")
    if not id:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Missing ID.")
    conversion = sql_client.conversion_get_by_id(id)
    if conversion is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="ID not found.")
    if conversion.status != ConversionStatus.COMPLETED:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Conversion is not completed yet.")

    images_folder_path = f"{RESULTS_FOLDER}/{id}/"
    ordered_images_paths = sorted(  # Sort the images by their page number contained in the filename
        os.listdir(images_folder_path), key=lambda x: int(re.match(IMAGE_FILENAME_FORMAT.replace("{}", r"(\d+)"), x).group(1))
    )
    images_bytes = []
    for filename in ordered_images_paths:
        with open(images_folder_path + filename, "rb") as f:
            images_bytes.append(base64.b64encode(f.read()).decode("utf-8"))
    conversion_results = ConversionResults(id=id, images_bytes=images_bytes)
    return conversion_results


if __name__ == "__main__":
    uvicorn.run(app)
