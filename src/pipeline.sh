#!/bin/bash

python src/dscc-scan-00-make_images.py
python src/dscc-scan-01-correction.py
python src/dscc-scan-02-ocr.py
python src/dscc-scan-03-resize.py
python src/dscc-scan-04-coverpage.py
python src/dscc-scan-05-prepublish.py
python src/dscc-scan-06-metadata.py
python src/dscc-scan-99-output.py
