import streamlit as st

from src.agent.downloader import download_solexs
from src.agent.download_hel1os import download_hel1os
from src.agent.unzipper import extract_all

from src.readers.solex_reader import load_solexs
from src.readers.helios_reader import load_hel1os

from src.plots.plotter import build_dashboard


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="ISRO Solar Dashboard",
    layout="wide"
)

st.title("☀️ Aditya-L1 Solar Dashboard")


# ==========================================
# SESSION STATE
# ==========================================

if "fig" not in st.session_state:
    st.session_state.fig = None

if "solex_df" not in st.session_state:
    st.session_state.solex_df = None

if "hel_df" not in st.session_state:
    st.session_state.hel_df = None

if "date_str" not in st.session_state:
    st.session_state.date_str = None


# ==========================================
# DATE PICKER
# ==========================================

selected_date = st.date_input(
    "Select Observation Date"
)


# ==========================================
# FETCH BUTTON
# ==========================================

if st.button("Fetch Data"):

    progress = st.progress(0)

    status = st.empty()

    date_str = selected_date.strftime(
        "%Y-%m-%d"
    )

    # ---------------------
    # DOWNLOAD SOLEXS
    # ---------------------

    status.info(
        "Downloading SoLEXS..."
    )

    progress.progress(10)

    download_solexs(
        date_str
    )

    # ---------------------
    # DOWNLOAD HEL1OS
    # ---------------------

    status.info(
        "Downloading HEL1OS..."
    )

    progress.progress(35)

    download_hel1os(
        date_str
    )

    # ---------------------
    # EXTRACT FILES
    # ---------------------

    status.info(
        "Extracting files..."
    )

    progress.progress(60)

    extract_all()

    # ---------------------
    # LOAD DATA
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
    # BUILD PLOT
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

    # ---------------------
    # SAVE TO SESSION STATE
    # ---------------------

    st.session_state.fig = fig
    st.session_state.solex_df = solex_df
    st.session_state.hel_df = hel_df
    st.session_state.date_str = date_str


# ==========================================
# DISPLAY RESULTS
# ==========================================

if st.session_state.fig is not None:

    st.plotly_chart(
        st.session_state.fig,
        use_container_width=True
    )

    st.subheader("Download Data")

    solex_csv = (
        st.session_state.solex_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    hel_csv = (
        st.session_state.hel_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="📥 Download SoLEXS CSV",
            data=solex_csv,
            file_name=f"{st.session_state.date_str}_solexs.csv",
            mime="text/csv"
        )

    with col2:

        st.download_button(
            label="📥 Download HEL1OS CSV",
            data=hel_csv,
            file_name=f"{st.session_state.date_str}_hel1os.csv",
            mime="text/csv"
        )

    st.markdown("---")

    st.write(
        f"**SoLEXS Rows:** {len(st.session_state.solex_df)}"
    )

    st.write(
        f"**HEL1OS Rows:** {len(st.session_state.hel_df)}"
    )