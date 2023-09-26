# Imports
import os
from glob import glob
import pandas as pd
from pdfrw import PdfReader, PdfWriter, PdfDict


def load_metadata():
    df = pd.read_csv(
        "data/metadata/metadata.tsv",
        sep="\t",
        header=0,
        index_col="filename",
    )
    return df


if __name__ == "__main__":
    print("Running DSCC Pipeline - Step 7: Embed metadata")

    # Get files
    files = glob("data/cover_pdfs/*.pdf")

    print(f"Found {len(files)} files to embed metadata")
    print("==========================================")

    df = load_metadata()

    for file in files:
        print(f"Embedding metadata in {file}...")
        pdf_reader = PdfReader(file)
        metadata_title = df.loc[file.split("/")[-1], "item_title"]
        metadata = PdfDict(
            Author="Institute for the Study of the Ancient World; Georgian National Museum",
            Subject="Digital South Caucasus Collection",
            Title=metadata_title,
        )
        pdf_reader.Info.update(metadata)
        metadata_pdf = f"{file.replace('/cover_pdfs/', '/metadata_pdfs/')}"
        PdfWriter().write(metadata_pdf, pdf_reader)
        # TODO: Make file deletion optional
        os.remove(file)

    print("Done!\n")
