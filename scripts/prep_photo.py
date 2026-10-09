from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_PHOTO = BASE_DIR / "source-photo.png"
OUTPUT_PHOTO = BASE_DIR / "source-prepped.png"


def main():
    if not INPUT_PHOTO.exists():
        raise FileNotFoundError(f"Photo not found: {INPUT_PHOTO}")

    print("Removing background...")
    image = Image.open(INPUT_PHOTO).convert("RGBA")
    foreground = remove(image)

    print("Improving contrast...")
    image_array = np.array(foreground)
    rgb = image_array[:, :, :3]
    alpha = image_array[:, :, 3]

    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    lightness, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )
    lightness = clahe.apply(lightness)

    improved_lab = cv2.merge((lightness, a_channel, b_channel))
    improved_rgb = cv2.cvtColor(improved_lab, cv2.COLOR_LAB2RGB)

    print("Creating white background...")
    alpha_float = alpha[:, :, None].astype(np.float32) / 255.0
    white_background = np.full_like(improved_rgb, 255)

    result = (
        improved_rgb.astype(np.float32) * alpha_float
        + white_background.astype(np.float32) * (1 - alpha_float)
    ).clip(0, 255).astype(np.uint8)

    Image.fromarray(result).save(OUTPUT_PHOTO)
    print(f"Prepared photo saved to: {OUTPUT_PHOTO}")


if __name__ == "__main__":
    main()
