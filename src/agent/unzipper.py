import zipfile
from pathlib import Path


def extract_zip(zip_path):

    zip_path = Path(zip_path)

    filename = zip_path.stem

    extract_folder = Path("data") / filename

    extract_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    print(f"\nExtracting {zip_path.name}")

    with zipfile.ZipFile(zip_path, "r") as zip_ref:

        zip_ref.extractall(extract_folder)

    print(
        f"Extracted -> {extract_folder}"
    )

    return extract_folder


def extract_all(download_folder="downloads"):

    download_folder = Path(download_folder)

    extracted = []

    for zip_file in download_folder.glob("*.zip"):

        extracted.append(
            extract_zip(zip_file)
        )

    return extracted


if __name__ == "__main__":

    folders = extract_all()

    print("\nExtracted Folders:")

    for f in folders:
        print(f)