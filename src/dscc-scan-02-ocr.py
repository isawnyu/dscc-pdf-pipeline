# following https://python.plainenglish.io/convert-scanned-files-to-searchable-pdf-using-python-and-pytesseract-3ee31ee6f01f

from glob import glob
import os
import pytesseract
from pdf2image import convert_from_path
import PyPDF2
from PyPDF2 import PdfReader
import io
from tqdm import tqdm

# constants
TEST_MODE = True

# Helper scripts
def get_output_filename(input_filename):
    return input_filename.replace(".pdf", "").replace(
        "/corrected_pdfs/", "/ocr_images/"
    )


if __name__ == "__main__":
    print("Running DSCC Pipeline - Step 3: OCR PDFs")

    # Get files
    files = glob("data/corrected_pdfs/*.pdf")

    print(f"Found {len(files)} files to OCR")
    print("==========================================")

    for file in files:
        print(f"Performing OCR on {file}...")
        cmd = f"pdfimages -j {file} {get_output_filename(file)}"
        os.system(cmd)

        pdf_writer = PyPDF2.PdfFileWriter()

        images = sorted(glob(f"{get_output_filename(file)}-*.jpg"))
        run_images = images

        if TEST_MODE:
            run_images = images[:5]
            print("TESTING MODE: Only 5 pages will be OCRd")

        for image in tqdm(run_images):
            page = pytesseract.image_to_pdf_or_hocr(
                image, lang="kat+rus", extension="pdf"
            )
            pdf = PyPDF2.PdfFileReader(io.BytesIO(page))
            pdf_writer.addPage(pdf.getPage(0))

        # export the searchable PDF to searchable.pdf
        with open(f"{file.replace('/corrected_pdfs/', '/ocr_pdfs/')}", "wb") as f:
            pdf_writer.write(f)

        # TODO: Make file deletion optional
        os.remove(file)

        # Delete images
        for image in images:
            os.remove(image)

    print("Done!\n")
