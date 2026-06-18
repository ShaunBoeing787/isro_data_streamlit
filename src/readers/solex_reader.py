from pathlib import Path
from astropy.io import fits
import pandas as pd
import numpy as np


def find_solexs_lc_file(date_str):

    date_compact = date_str.replace("-", "")

    for file in Path("data").rglob("*.lc.gz"):

        if date_compact in str(file):
            return file

    raise FileNotFoundError(
        f"No SoLEXS file found for {date_str}"
    )


def load_solexs(date_str):

    lc_file = find_solexs_lc_file(date_str)

    print(
        f"Loading SoLEXS: {lc_file}"
    )

    hdul = fits.open(lc_file)

    data = hdul[1].data

    df = pd.DataFrame({
        "time": np.array(
            data["TIME"],
            dtype=np.float64
        ),
        "counts": np.array(
            data["COUNTS"],
            dtype=np.float64
        )
    })

    df = df.dropna()

    df["datetime"] = pd.to_datetime(
        df["time"],
        unit="s",
        utc=True
    )

    return df