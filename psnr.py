from PIL import Image
import math
import numpy as np


def PSNR(testpic, out):
    original = np.array(testpic)
    compressed = np.array(out)
    mse = np.mean((original - compressed) ** 2)
    if (mse == 0):
        return 100
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr


def MSE(testpic, out):
    original = np.array(testpic)
    compressed = np.array(out)
    mse = np.mean((original - compressed) ** 2)
    if (mse == 0):
        return 100
    return mse


def RMSE(testpic, out):
    original = np.array(testpic)
    compressed = np.array(out)
    mse = np.mean((original - compressed) ** 2)
    if (mse == 0):
        return 100
    rmse = mse ** 0.5
    return rmse


def start_psnr():
    original_image = Image.open("im256.png").convert("RGB")
    stego_image = Image.open("res70.png").convert("RGB")
    print(f"PSNR: {PSNR(original_image, stego_image)}\n", f"MSE: {MSE(original_image, stego_image)}\n",
          f"RMSE: {RMSE(original_image, stego_image)}\n")
    pass


if __name__ == "__main__":
    start_psnr()
