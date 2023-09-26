# Imports
from glob import glob
import os
import cv2
import img2pdf

# Helper scripts
def automatic_brightness_and_contrast(image, clip_hist_percent=1):
    # Automatic brightness and contrast optimization with optional histogram clipping
    # cf. https://stackoverflow.com/a/56909036
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate grayscale histogram
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index - 1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= maximum / 100.0
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size - 1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)


if __name__ == "__main__":
    print("Running DSCC Pipeline - Step 2: Correcting Images")

    # Get files
    files = glob("data/images/*.jpg")
    print("==========================================")

    for file in files:
        image = cv2.imread(file)
        auto_result, alpha, beta = automatic_brightness_and_contrast(image, 1)
        cv2.imwrite(file.replace("images", "corrected_images"), auto_result)
        # TODO: Make file deletion optional
        os.remove(file)

    corrected_files = sorted(glob("data/corrected_images/*.jpg"))

    pdf_bases = sorted(
        list(
            (
                set(
                    [
                        file.replace("data/corrected_images/", "")
                        .replace(".jpg", "")
                        .rpartition("-")[0]
                        for file in corrected_files
                    ]
                )
            )
        )
    )

    for pdf_base in pdf_bases:
        corrected_file = f"data/corrected_pdfs/{pdf_base}.pdf"
        print(f"Writing corrected pdf to {corrected_file}...")
        files = sorted([file for file in corrected_files if pdf_base in file])

        with open(corrected_file, "wb") as f:
            f.write(img2pdf.convert(files))

        # TODO: Make file deletion optional
        for file in files:
            os.remove(file)

    print("Done!\n")
