# Imports
import os
import pandas as pd
from glob import glob

# Constant

USE_CACHE = True
REQUIRE_METADATA = True

# Helper scripts
def get_output_filename(input_filename):
    return input_filename.replace(".pdf", "").replace("/input/", "/images/")


def load_metadata():
    df = pd.read_csv(
        "data/metadata/metadata.tsv",
        sep="\t",
        header=0,
        index_col="filename",
    )
    return df


if __name__ == "__main__":
    print("Running DSCC Pipeline - Step 1: Make Images")

    # Get files
    files = glob("data/input/*.pdf")
    basename_files = [os.path.basename(file) for file in files]

    if USE_CACHE:
        cached_files = [os.path.basename(file) for file in glob("data/output/*.pdf")]

        files = [file for file in files if os.path.basename(file) not in cached_files]
        if cached_files:
            print(f"Skipping {len(cached_files)} files already imaged:")
            for file in cached_files:
                print(f"\t{file}")
            print()

    if REQUIRE_METADATA:
        df = load_metadata()
        files = [file for file in files if os.path.basename(file) in df.index]
        excluded_files = [file for file in basename_files if file not in df.index]
        if excluded_files:
            print(f"Skipping {len(excluded_files)} files without metadata:")
            for file in excluded_files:
                print(f"\t{file}")
            print()

    print(f"Found {len(files)} files to image")
    print("==========================================")

    if len(files) == 0:
        print("No files to image. Exiting...")
        exit()

    for file in files:
        print(f"Imaging {file}...")
        cmd = f"pdfimages -j {file} {get_output_filename(file)}"
        os.system(cmd)

    # TODO: Move input file to processed folder
    print("Done!\n")
