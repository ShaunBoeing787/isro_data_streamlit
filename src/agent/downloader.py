from bs4 import BeautifulSoup
from datetime import datetime
import os

from src.agent.issdc_client import ISSDCClient

DOWNLOAD_DIR = "downloads"


def download_solexs(date_str):
    """
    date_str format:
    YYYY-MM-DD

    Example:
    2026-06-14
    """

    client = ISSDCClient()

    if not client.login():
        raise Exception("Login failed")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # =====================================
    # Open SoLEXS browse page
    # =====================================

    url = (
        "https://pradan1.issdc.gov.in/"
        "al1/protected/browse.xhtml?id=solexs"
    )

    response = client.session.get(url)

    print("Browse Status:", response.status_code)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    # =====================================
    # Extract ViewState
    # =====================================

    view_state = soup.find(
        "input",
        {"name": "javax.faces.ViewState"}
    )["value"]

    print("ViewState:", view_state)

    # =====================================
    # Build date range
    # =====================================

    start_time = f"{date_str} 00:00:00"
    end_time = f"{date_str} 23:59:59"

    # =====================================
    # Filter payload
    # =====================================

    payload = {

        "filterForm": "filterForm",

        "filterForm:j_idt53": "VIEW",

        "filterForm:filterTable:0:attr":
            "ObservationTime;TIME_DURATION;label.Product_Details.Observation_Details.Time_Coordinates.start_date_time, label.Product_Details.Observation_Details.Time_Coordinates.stop_date_time",

        "filterForm:filterTable:0:opr":
            "TIME_DURATION,TimeDurationIn",

        "filterForm:filterTable:0:datetime1_input":
            start_time,

        "filterForm:filterTable:0:datetime2_input":
            end_time,

        "filterForm:filterButton":
            "Filter",

        "javax.faces.ViewState":
            view_state
    }

    # =====================================
    # Submit filter
    # =====================================

    filtered = client.session.post(
        url,
        data=payload
    )

    print("Filtered Status:", filtered.status_code)

    soup = BeautifulSoup(
        filtered.text,
        "html.parser"
    )

    target_date = datetime.strptime(
        date_str,
        "%Y-%m-%d"
    ).strftime("%Y%m%d")

    zip_links = []

    # =====================================
    # Extract ZIP URLs
    # =====================================

    for link in soup.find_all("a"):

        href = link.get("href")

        if not href:
            continue

        if ".zip" not in href:
            continue

        if target_date not in href:
            continue

        full_url = (
            "https://pradan1.issdc.gov.in"
            + href
        )

        zip_links.append(full_url)

    print("\nZIP FILES FOUND:")

    for z in zip_links:
        print(z)

    # =====================================
    # Download files
    # =====================================

    downloaded_files = []

    for file_url in zip_links:

        filename = (
            file_url
            .split("/")[-1]
            .split("?")[0]
        )

        save_path = os.path.join(
            DOWNLOAD_DIR,
            filename
        )

        print(f"\nDownloading {filename}")

        response = client.session.get(
            file_url,
            stream=True
        )

        with open(save_path, "wb") as f:

            for chunk in response.iter_content(
                chunk_size=8192
            ):
                if chunk:
                    f.write(chunk)

        print("Saved ->", save_path)

        downloaded_files.append(save_path)

    return downloaded_files


if __name__ == "__main__":

    files = download_solexs(
        "2026-06-14"
    )

    print("\nDownloaded Files:")

    for f in files:
        print(f)