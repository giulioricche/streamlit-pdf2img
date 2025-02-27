from pdf2imgfe.lib.log import logger

import typing as T
import pandas as pd
import streamlit as st
from streamlit_modal import Modal


def _onclik_modal_db_table(value):
    """
    Handle the click event on the modal.

    Parameters
    ----------
    value : bool
        Open or close the modal.
    """

    st.session_state.modal_db_table_open = value


def load(get_all_conversions: T.Callable):
    """
    Load the database modal.

    Parameters
    ----------
    get_all_conversions : Callable
        Function to get all conversions from the database.
    """

    db_table_modal = Modal(title="Conversions Table", max_width=800, padding=20, key="modal_db_table")

    if (
        st.button(
            label="🔎",
            on_click=_onclik_modal_db_table,
            args=(True,),
            help="See all conversions that have been processed",
        )
        or st.session_state.modal_db_table_open
    ):
        logger.info("Rendering db modal")
        with db_table_modal.container():
            st.markdown("The following table shows all the conversions that have been processed.")
            with st.spinner("Retrieving data..."):
                conversions = pd.DataFrame(get_all_conversions())
            st.dataframe(conversions, hide_index=True, height=220, use_container_width=True)
            st.button("Ok", on_click=_onclik_modal_db_table, args=(False,), type="primary")
        st.write(  # Remove default close button and set the position of the modal
            """
                <style>
                    div[key="modal_db_table"] button[kind="secondary"] {
                        display: none;
                    }
                    div[key="modal_db_table"] {
                        left: 2rem !important;
                        top: 1rem !important;
                    }
                    [data-testid='stHorizontalBlock'] {
                        align-items: center !important;
                    }
                </style>
            """,
            unsafe_allow_html=True,
        )
