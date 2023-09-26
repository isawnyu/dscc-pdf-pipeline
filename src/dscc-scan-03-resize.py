import os
from glob import glob
from PyPDF2 import PdfFileReader, PdfFileWriter

# constants
TEST_MODE = True
QUERY = (612, 792)

# Helper scripts
def get_output_filename(input_filename):
    return input_filename.replace("/ocr_pdfs/", "/resized_pdfs/")


def scale(query, pdf):
    # https://github.com/py-pdf/pypdf/issues/406#issue-306182228
    # for pdf in pdfs:
    w, h = query
    reader = PdfFileReader(pdf)
    writer = PdfFileWriter()

    for i in range(reader.numPages):
        page_object = reader.getPage(i)
        page_object.scaleTo(float(w), float(h))
        writer.addPage(page_object)

    return writer


if __name__ == "__main__":
    print("Running DSCC Pipeline - Step 4: Resize PDFs")

    # Get files
    files = glob("data/ocr_pdfs/*.pdf")

    print(f"Found {len(files)} files to resize")
    print("==========================================")

    for file in files:
        print(f"Performing resize on {file}...")

        scaled_pdf_writer = scale(QUERY, file)

        with open(f"{get_output_filename(file)}", "wb") as f:
            scaled_pdf_writer.write(f)

        # TODO: Make file deletion optional
        os.remove(file)

    print("Done!\n")
