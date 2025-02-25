import io
import zipfile
import typing as T


def zip_images(images: T.List[bytes], filename_format: str) -> bytes:
    """
    Zip the images into a single ZIP archive.

    Parameters
    ----------
    images : List[bytes]
        List of images to zip.
    filename_format : str
        Format of the filename for each image.

    Returns
    -------
    bytes
        ZIP archive containing the images.
    """

    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as file_zip:
        for i, image in enumerate(images):
            file_zip.writestr(filename_format.format(i + 1), image)
    zip_buf.seek(0)
    return zip_buf.read()
