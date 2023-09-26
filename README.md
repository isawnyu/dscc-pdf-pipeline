# DSCC PDF Pipeline
Python-based pipeline to prepare scanned PDFs in the DSCC collection for publication

## Pipeline description
Image correction -> OCR -> PDF resizing -> Coverpage addition -> Metadata embedding -> Final pdf output

## Usage

- Place pdf in `data/input`
- Add metadata to `data/metadata.csv`
- `sh src/pipeline.sh`

Written by [Patrick J. Burns](https://isaw.nyu.edu/people/staff/patrick-burns), [ISAW Library](https://isaw.nyu.edu/library); 2022-2023.
