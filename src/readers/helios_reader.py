from pathlib import Path
from astropy.io import fits
import pandas as pd
import numpy as np


def load_hel1os(date_str):

    date_compact = date_str.replace("-", "")

    all_dfs = []

    for file in Path("data").rglob("lightcurve_czt1.fits"):

        if date_compact not in str(file):
            continue

        print(f"Loading HEL1OS: {file}")

        hdul = fits.open(file)

        # Full Band 18–160 keV
        ext = 5

        data = hdul[ext].data

        df = pd.DataFrame({
            "datetime": pd.to_datetime(
                list(data["ISOT"])
            ),
            "counts": np.array(
                data["CTR"],
                dtype=np.float64
            ),
            "error": np.array(
                data["STAT_ERR"],
                dtype=np.float64
            )
        })

        df = df.dropna()

        all_dfs.append(df)

    if len(all_dfs) == 0:
        raise FileNotFoundError(
            f"No HEL1OS data found for {date_str}"
        )

    final_df = pd.concat(all_dfs)

    final_df = final_df.sort_values(
        "datetime"
    )

    final_df = final_df.reset_index(
        drop=True
    )

    return final_df