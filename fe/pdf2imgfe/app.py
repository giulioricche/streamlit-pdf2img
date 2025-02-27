from pdf2imgfe.lib.log import logger

import asyncio
import streamlit as st

from app_components import db_modal

from pdf2imgfe.services.convert import ConvertService
from pdf2imgfe.lib.io import zip_images
from pdf2imgfe.lib.exception import ProcessException
from pdf2imgfe.lib.statics import ConversionStatus, IMAGE_FILENAME_FORMAT, IMAGE_FILE_EXTENSION

# Initialize the app
st.set_page_config(page_title="PDF to Image Converter", page_icon="🧞‍♂️", layout="wide")
st.write(
    "<style>[data-testid='stHorizontalBlock'] button[kind='primary'] {margin-top: 30px; margin-bottom: 0;}</style>",
    unsafe_allow_html=True,
)  # Align buttons at top of the block
st.write("<style>div.block-container{padding-top:3rem;}</style>", unsafe_allow_html=True)  # Reduce padding at top of the page


def __heading_section(convert_service: ConvertService) -> st.delta_generator.DeltaGenerator:
    """
    Render the heading section of the app, containing the title, the description, and the database modal.

    Parameters
    ----------
    convert_service : ConvertService
        Service to get all conversions.

    Returns
    -------
    st.delta_generator.DeltaGenerator
        Main section of the app.
    """

    _, main_section = st.columns([0.08, 0.92])
    main_section.title("PDF to Image Converter")
    main_section.markdown("<br>", unsafe_allow_html=True)
    _, main_section, side_section = st.columns([0.08, 0.82, 0.1])
    main_section.markdown(
        "Upload a PDF file to convert it to images. Start the conversion process to generate an image for each page of the PDF. 📄"
    )
    with side_section:
        db_modal.load(convert_service.get_all_conversions)
    return main_section


def __input_section():
    """
    Render the input section of the app, containing the file uploader and the submit button.
    """

    def __file_uploader_on_change():
        st.session_state.conversion_completed = False
        st.session_state.conversion_id = None

    def __button_submit_on_click():
        st.session_state.conversion_started = True

    col1, _, col2 = st.columns([0.75, 0.05, 0.2])
    st.session_state.uploaded_file = col1.file_uploader("Upload a PDF file", type="pdf", on_change=__file_uploader_on_change)
    col2.button(
        "Start conversion",
        disabled=st.session_state.uploaded_file is None,
        use_container_width=True,
        type="primary",
        on_click=__button_submit_on_click,
    )


async def __processing_section(convert_service: ConvertService):
    """
    Render the processing section of the app, containing the spinner and the conversion status message, and manage the
    conversion process.

    Parameters
    ----------
    convert_service : ConvertService
        Service to convert PDF to images.
    """

    message_component = st.empty()
    try:
        st.session_state.conversion_id = convert_service.convert_pdf_to_images(st.session_state.uploaded_file)
        logger.info(f"Started conversion ID: {st.session_state.conversion_id}")
        message_component.info("Conversion process started! Checking completion status... ⏳")
        while True:
            status = convert_service.check_conversion_status(st.session_state.conversion_id)
            logger.info(f"Conversion status for ID {st.session_state.conversion_id}: {status}")
            if status == ConversionStatus.COMPLETED:
                message_component.success("Conversion completed! ✅")
                st.session_state.conversion_completed = True
                break
            elif status == ConversionStatus.FAILED:
                message_component.error("Conversion failed. Please try again.")
                break
            else:
                logger.info(f"Conversion status: {status}; waiting to be completed")
                await asyncio.sleep(2)
    except ProcessException as e:
        logger.error(f"Failed to upload PDF: {e}")
        message_component.error("Failed to upload PDF. Please try again.")


def __output_section(convert_service: ConvertService, id: str, filename: str):
    """
    Render the output section of the app, containing the conversion results and the download button.

    Parameters
    ----------
    convert_service : ConvertService
        Service to get the conversion results.
    id : str
        Unique identifier of the conversion.
    """

    @st.cache_data
    def __zip_images(id, images):
        logger.info(f"Zipping images for ID: {id}")
        return zip_images(images, IMAGE_FILENAME_FORMAT)

    images = convert_service.get_conversion_results(st.session_state.conversion_id)
    col1, col2 = st.columns([0.8, 0.2])
    col1.markdown("### Conversion Results")
    with st.container(border=True):
        cols = st.columns(5)
        for i, image_data in enumerate(images):
            cols[i % 5].image(image_data, use_container_width=True, caption=f"Page {i+1}", output_format=IMAGE_FILE_EXTENSION)
        col2.download_button(
            "Download Images as ZIP",
            __zip_images(id, images),
            f"{filename}_images.zip",
            use_container_width=True,
            type="secondary",
        )


def __restart_section():
    """
    Render the restart section of the app, containing the button to perform another conversion and reset the conversion
    state.
    """

    def __reset_conversion_state():
        st.session_state.uploaded_file = None
        st.session_state.conversion_started = False
        st.session_state.conversion_completed = False
        st.session_state.conversion_id = None
        logger.info("Reset conversion state for new conversion")

    st.columns([0.8, 0.2])[1].button(
        "Perform another conversion", use_container_width=True, type="primary", on_click=__reset_conversion_state
    )


def main():
    # Initialize session state variables
    if "modal_db_table_open" not in st.session_state:
        st.session_state.modal_db_table_open = False
    if "conversion_id" not in st.session_state:
        st.session_state.conversion_id = None
    if "conversion_started" not in st.session_state:
        st.session_state.conversion_started = False
    if "conversion_completed" not in st.session_state:
        st.session_state.conversion_completed = False

    convert_service = ConvertService()
    main_section = __heading_section(convert_service)
    main_section.markdown("<br>", unsafe_allow_html=True)
    with main_section:

        if not st.session_state.conversion_started and not st.session_state.conversion_completed:
            logger.info("Rendering input section")
            __input_section()
            st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.conversion_started and not st.session_state.conversion_completed:
            logger.info("Rendering processing section")
            with st.spinner(f'Processing file named "{st.session_state.uploaded_file.name}"'):
                st.markdown("<br>", unsafe_allow_html=True)
                asyncio.run(__processing_section(convert_service))

        if st.session_state.conversion_completed:
            logger.info("Rendering output section")
            st.divider()
            __output_section(convert_service, st.session_state.conversion_id, st.session_state.uploaded_file.name)
            __restart_section()


if __name__ == "__main__":
    main()
