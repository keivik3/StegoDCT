# StegoDCT

A Python project for image watermarking using Discrete Cosine Transform (DCT), with tools for embedding binary watermarks into images, extracting watermarks, and measuring image quality and transmission errors.

## Overview

This repository implements a DCT-based watermarking algorithm to embed and extract binary watermark images into/from cover images. It leverages block-wise DCT transformations to modify frequency coefficients subtly, ensuring robust watermark embedding with minimal visual distortion.

Additionally, it provides utilities to:

- Calculate Bit Error Rate (BER) to evaluate watermark extraction accuracy.
- Compute standard image quality metrics such as PSNR (Peak Signal-to-Noise Ratio), MSE (Mean Squared Error), and RMSE (Root Mean Squared Error).
- Run a serial communication test script to simulate transmission and calculate BER.

## Files

- **dct_watermarking.py** – Main script containing DCT-based watermark embedding and extraction functions, image preparation, and helper methods.
- **ber.py** – Script for computing Bit Error Rate over serial communication.
- **psnr.py** – Script to calculate PSNR, MSE, and RMSE between original and watermarked images.

## Getting Started

### Requirements

- Python 3.x
- Pillow (PIL) for image processing
- NumPy for numerical operations

Install dependencies using pip:

```
pip install Pillow numpy
```

### Usage

1. To embed a watermark image into a cover image:
```
from PIL import Image
import dct_watermarking

cover_image = Image.open("cover_image.png")
watermark = Image.open("watermark.png")

watermarked_matrix = dct_watermarking.insert(cover_image, watermark)
dct_watermarking.photo(cover_image, watermarked_matrix)
cover_image.save("watermarked_result.png")
```

2. To extract the watermark from a watermarked image:

```
watermarked_image = Image.open("watermarked_result.png")
extracted_binary = dct_watermarking.extract(watermarked_image)
dct_watermarking.bin_photo(extracted_binary, watermark)
```

3. To calculate quality metrics:

```
python psnr.py
```

4. To measure BER (Bit Error Rate):

```
python ber.py
```

## About the Algorithm

The watermarking scheme works by dividing the cover image into 8x8 blocks, performing DCT on each block, and modifying particular coefficients based on the watermark bits. The inverse DCT reconstructs the image with embedded watermark with minimal distortion.

## License

This project is open source and available under the MIT License.

## Author

Created by keivik3

