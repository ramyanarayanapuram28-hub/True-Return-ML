# TRUE-RETURN — ML-Based Product Image Verification

## Overview

TRUE-RETURN is a product-return verification project designed to help identify potentially suspicious returns by comparing original product images with returned product images.

This repository contains the Machine Learning (ML) image-verification prototype developed for TRUE-RETURN.

The system uses a pretrained DINOv2 vision model to extract image embeddings and cosine similarity to compare product images. It then applies a configurable similarity threshold to produce a `MATCH` or `SUSPICIOUS` result.

> **Project status:** Initial working prototype. Real-world fraud-detection accuracy has not yet been established.

## Problem Statement

A returned product may look similar to the original product but may not be the same physical item. Manual visual inspection can be time-consuming.

TRUE-RETURN explores using computer vision to compare product images and flag returns that may require further inspection.

## Technologies Used

- **Python** — Main programming language
- **PyTorch** — Executes the pretrained neural network
- **Hugging Face Transformers** — Loads the DINOv2 model
- **DINOv2 Base** — Extracts visual representations from images
- **OpenCV** — Computer-vision and image-processing support
- **Pillow** — Image loading and processing
- **NumPy** — Numerical operations on image embeddings
- **CSV** — Stores verification history

## How It Works

1. Load original product images and returned product images.
2. Prepare the images for the vision model.
3. Generate the full image and multiple central crops.
4. Extract image embeddings using pretrained DINOv2.
5. Average the crop embeddings to obtain an image representation.
6. Compare returned-image embeddings with original-image embeddings using cosine similarity.
7. Identify the best-matching original image for each returned image.
8. Apply the configured similarity threshold to classify the result.
9. Save verification details to a CSV history file.

## Decision Logic

The current configured threshold is `0.70`.

- **MATCH:** At least one original reference image reaches or exceeds the threshold.
- **SUSPICIOUS:** No original reference image reaches the threshold.

The similarity percentage is a transformed similarity score, not the probability that a product is genuine. Visual similarity does not guarantee physical product identity.

## Project Structure

```text
TRUE-RETURN/
├── README.md
├── .gitignore
└── vision-service/
    ├── app.py
    ├── image_matching.py
    ├── requirements.txt
    └── test_images/
        ├── original/
        └── returned/
```

The test-image folders are optional and should contain only images that are permitted to be shared.

## Setup and Installation

### Prerequisites

- Python 3.11 recommended
- Internet access for the initial model download, unless the model is already cached
- Git (for repository operations)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/TRUE-RETURN-ML.git
cd TRUE-RETURN-ML
```

Replace `YOUR-USERNAME` with the GitHub username that owns the repository.

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use:

```powershell
.\venv\Scripts\python.exe -m pip install -r .\vision-service\requirements.txt
```

### 3. Install dependencies

```powershell
python -m pip install -r .\vision-service\requirements.txt
```

PyTorch installation requirements can vary by operating system and CPU/GPU configuration.

### 4. Run the local test

From the repository root, with the dependencies installed:

```powershell
python .\vision-service\app.py
```

The script expects original and returned sample images in the configured test-image folders.

The first run may download the pretrained DINOv2 model. Model loading and inference time depend on the computer and available hardware.

## Verification History

The local prototype records verification details in:

`vision-service/verification_history.csv`

The history includes:

- Timestamp
- Returned photo
- Best-matching original
- Similarity percentage
- Verification result
- Reason for the result

This is basic prototype logging, not a production database.

## Training and Evaluation Status

This version uses pretrained DINOv2 weights for feature extraction. The model has not been fine-tuned on a TRUE-RETURN-specific labelled dataset, and no dedicated fraud-classification model has been trained.

The prototype has been tested with sample images to verify the execution and logging workflow. A representative labelled dataset is still needed to measure real-world performance.

## Limitations

- Visually similar products may be different physical items.
- Lighting, camera angle, background and image quality can affect similarity scores.
- The threshold is provisional and requires evaluation on labelled examples.
- The current local script is not yet a production web API.
- CSV logging is suitable for a prototype but not a replacement for production-grade storage.

## Future Improvements

- Build a labelled dataset of same-item and different-item image pairs.
- Evaluate precision, recall, false matches and missed matches.
- Calibrate the similarity threshold using validation data.
- Evaluate multiple-view capture and unique product identifiers.
- Explore fine-tuning or metric learning if sufficient labelled data becomes available.
- Expose the verification module through an API for website integration.
- Add robust history storage and human review for suspicious or uncertain cases.

## Contribution

This repository contains the ML image-verification prototype, including pretrained-model-based feature extraction, image similarity comparison, threshold-based decision logic and CSV verification history.

## Disclaimer

This is an experimental prototype intended for educational and project-development purposes. A `MATCH` result does not prove that two images depict the same physical product, and a `SUSPICIOUS` result does not by itself prove fraud.
