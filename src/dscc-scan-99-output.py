# Imports
import os
from glob import glob

# Helper scripts
def get_output_filename(input_filename):
    return input_filename.replace("/metadata_pdfs/", "/output/")


if __name__ == "__main__":
    print("Running DSCC Pipeline - Step 8: Preparing output file")

    # Get files
    files = glob("data/metadata_pdfs/*.pdf")

    print(f"Found {len(files)} files to output")
    print("==========================================")

    for file in files:
        print(file)
        # move file to output folder
        cmd = f"mv {file} {get_output_filename(file)}"
        os.system(cmd)

    print("Done!\n")
