#!/bin/bash
# S3: HistData-zips (data/long_m1) → M5 (data/long_m5) → bevroren ORB-test (PREREG_S3.md). Uitvoer: results/s3/S3_output.txt
set -e
cd "$(dirname "$0")"
mkdir -p results/s3
ls data/long_m1/*.zip >/dev/null
sha256sum data/long_m1/*.zip > results/s3/CHECKSUMS_long_m1.sha256
.venv/bin/python s3_histdata.py data/long_m1 data/long_m5 | tee results/s3/S3_parser.txt
.venv/bin/python s3_run.py data/long_m5 | tee results/s3/S3_output.txt
