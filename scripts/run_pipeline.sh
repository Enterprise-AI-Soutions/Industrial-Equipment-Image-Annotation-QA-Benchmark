#!/bin/bash

set -e

echo ""
echo "Industrial Equipment Image Annotation QA Benchmark"

echo ""
echo "Validate"

python -m src.validate_annotations \
data/annotations/annotator_1.json

echo ""
echo "Agreement"

python -m src.agreement_analysis \
data/annotations/annotator_1.json \
data/annotations/annotator_2.json

echo ""
echo "Review Queue"

python -m src.create_review_queue \
data/annotations/annotator_1.json \
data/annotations/annotator_2.json \
reports/review_queue.csv

echo ""
echo "Run Tests"

python -m pytest -q

echo ""
echo "Pipeline completed successfully."
