import streamlit as st
import pandas as pd
from src.agent.downloader import download_solexs
from src.agent.download_hel1os import download_hel1os

from src.agent.unzipper import extract_all

from src.readers.solex_reader import load_solexs
from src.readers.helios_reader import load_hel1os

from src.plots.plotter import build_dashboard


st.set_page_config(
    page_title="ISRO Solar Dashboard",
    layout="wide"
)

st.title("☀️ Aditya-L1 Solar Dashboard")

selected_date = st.date_input(
    "Select Observation Date"
)

if st.button("Fetch Data"):

    progress = st.progress(0)

    status = st.empty()

    date_str = selected_date.strftime(
        "%Y-%m-%d"
    )

    # ---------------------
    # Download SoLEXS
    # ---------------------

    status.info(
        "Downloading SoLEXS..."
    )

    progress.progress(10)

    download_solexs(
        date_str
    )

    # ---------------------
    # Download HEL1OS
    # ---------------------

    status.info(
        "Downloading HEL1OS..."
    )

    progress.progress(35)

    download_hel1os(
        date_str
    )

    # ---------------------
    # Extract
    # ---------------------

    status.info(
        "Extracting files..."
    )

    progress.progress(60)

    extract_all()

    # ---------------------
    # Read FITS
    # ---------------------

    status.info(
        "Reading FITS files..."
    )

    progress.progress(80)

    solex_df = load_solexs(
        date_str
    )

    hel_df = load_hel1os(
        date_str
    )
    
    # ---------------------
    # Plot
    # ---------------------

    status.info(
        "Building Dashboard..."
    )

    progress.progress(95)

    fig = build_dashboard(
        solex_df,
        hel_df
    )

    progress.progress(100)

    status.success(
        "Completed"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Download Data")

    solex_csv = solex_df.to_csv(
    index=False
    ).encode("utf-8")
    
    hel_csv = hel_df.to_csv(
    index=False
    ).encode("utf-8")

    with st.sidebar:
        
        st.header("Downloads")


        st.download_button(
        label="📥 Download SoLEXS Time Series",
        data=solex_csv,
        file_name=f"{date_str}_solexs.csv",
        mime="text/csv"
)

   

        st.download_button(
        label="📥 Download HEL1OS Time Series",
        data=hel_csv,
        file_name=f"{date_str}_hel1os.csv",
        mime="text/csv"
)
   

    st.write(
        f"SoLEXS Rows: {len(solex_df)}"
    )

    st.write(
        f"HEL1OS Rows: {len(hel_df)}"
    )