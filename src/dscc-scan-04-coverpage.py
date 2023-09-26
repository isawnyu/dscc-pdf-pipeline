# Imports
import os
from glob import glob

import pandas as pd

import base64
from io import BytesIO

import pdfkit
from PyPDF2 import PdfFileMerger

# constants
# TODO: Update other pipeline scripts to use constants in this way
LOGO_FILEPATH = "img/logo.png"
LOGO_TEXT_FILEPATH = "img/logo.txt"
COVER_IN_FILEPATH = "data/resized_pdfs"
COVER_OUT_FILEPATH = "data/cover_pdfs"

# Helper scripts

# load logo from string; create string, if missing


def file_exists(filepath: str) -> bool:
    try:
        with open(filepath, "r") as f:
            return True
    except FileNotFoundError:
        return False


def get_logo():
    if file_exists(LOGO_TEXT_FILEPATH):
        with open(LOGO_TEXT_FILEPATH, "r") as f:
            img_string = f.read()
    else:

        def image_file_path_to_base64_string(filepath: str) -> str:
            # https://stackoverflow.com/a/57278276
            """
            Takes a filepath and converts the image saved there to its base64 encoding,
            then decodes that into a string.
            """
            with open(filepath, "rb") as f:
                return base64.b64encode(f.read()).decode()

        img_string = image_file_path_to_base64_string(LOGO_FILEPATH)

        with open("img/logo.txt", "w") as f:
            f.write(img_string)
    return img_string


def load_metadata():
    df = pd.read_csv(
        "data/metadata/metadata.tsv",
        sep="\t",
        header=0,
        index_col="filename",
    )
    return df


def get_body(author, title, date, publisher, place, filename, img_string):
    body = f"""
        <html>
          <head>
            <meta name="pdfkit-page-size" content="Letter"/>
            <meta name="pdfkit-orientation" content="Portrait"/>
            <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
          </head>

          <img src="data:image/png;base64,{ img_string }" width="960px">
          <p>This pdf is a file in the Digital South Caucasus Collection (DSCC), a collection in the Ancient World Digital Library hosted by the <a href="https://isaw.nyu.edu/library">Institute for the Study of the Ancient World Library</a> in partnership with the <a href="https://www.museum.ge/index.php?m=2">Georgian National Museum</a>.</p>
          <ul>
            <li>Author: {author}</li>
            <li>Title: {title}</li>
            <li>Publication Date: {date}</li>
            <li>Publisher: {publisher}</li>
            <li>Place of Publication: {place}</li>
            <li>Collection: Digital South Caucasus Collection</li>
            <li>Collection ID: {filename.replace('.pdf', '')}</li>
        </ul>

          <h2>About</h2>

            <p>The Digital South Caucasus Collection (DSCC) is a collection in the Ancient World Digital Library (AWDL), a project of the Library of the Institute for the Study of the Ancient World (ISAW) at New York University in cooperation with the Georgian National Museum. AWDL’s mission is to identify, collect, curate, and provide access to a broad range of scholarly materials relevant to the study of the ancient world. The ISAW library is responsible for curating the collection, clearing the rights as needed, preserving the digital copies in NYU’s Faculty Digital Archive, creating high-quality metadata in order to maximize discoverability, and making the works accessible to the general scholarly public.          
        """
    return body


def split_fields(text):
    text_list = text.split("|")
    split_text = " / ".join(text_list)
    return split_text


if __name__ == "__main__":
    print("Running DSCC Pipeline - Step 5: Make Coverpages")

    # Get files
    files = glob(f"{COVER_IN_FILEPATH}/*.pdf")

    print(f"Found {len(files)} files for coverpages")
    print("==========================================")

    logo = get_logo()
    df = load_metadata()

    for file in files:
        print(f"Adding coverpage to {file}...")
        metadata_row = df.loc[file.split("/")[-1]]
        author, title, date, publisher, place, filename = (
            split_fields(metadata_row["creator"]),
            split_fields(metadata_row["title"]),
            metadata_row["date"],
            metadata_row["publisher"],
            metadata_row["place"],
            metadata_row.name,
        )

        body = get_body(author, title, date, publisher, place, filename, logo)

        # create coverpage

        options = {
            "dpi": 300,
            "page-size": "Letter",
            "margin-top": "0.25in",
            "margin-right": "0.25in",
            "margin-bottom": "0.25in",
            "margin-left": "0.25in",
            "encoding": "UTF-8",
            "custom-header": [("Accept-Encoding", "gzip")],
            "no-outline": None,
        }

        coverpage = BytesIO(pdfkit.from_string(body, options=options))

        # merge coverpage and pdf
        merger = PdfFileMerger()

        pdf = f"{COVER_IN_FILEPATH}/{filename}"

        merger.append(coverpage)
        merger.append(pdf)

        # write merged pdf
        with open(f"{COVER_OUT_FILEPATH}/{filename}", "wb") as f:
            merger.write(f)

        os.remove(file)

    print("Done!\n")
