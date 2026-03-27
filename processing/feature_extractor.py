import cv2
import numpy as np
from metrics.entropy import calculate_entropy


def extract_features(image, debug=False):
    """
    Extract normalized image features for decision engine

    Features:
    - r, g, b (mean channel intensities)
    - brightness
    - contrast
    - entropy
    """

    # -----------------------------
    # Safety Checks
    # -----------------------------
    if image is None:
        raise ValueError("Invalid image: None")

    if not isinstance(image, np.ndarray):
        raise TypeError("Input must be a numpy array")

    # -----------------------------
    # Convert to grayscale
    # -----------------------------
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # -----------------------------
    # Color Features (BGR → r,g,b)
    # -----------------------------
    b_mean, g_mean, r_mean = cv2.mean(image)[:3]

    r = r_mean / 255.0
    g = g_mean / 255.0
    b = b_mean / 255.0

    # -----------------------------
    # Brightness
    # -----------------------------
    brightness = np.mean(gray) / 255.0

    # -----------------------------
    # Contrast (std deviation)
    # -----------------------------
    contrast = np.std(gray) / 128.0

    # -----------------------------
    # Entropy (normalized)
    # -----------------------------
    entropy = calculate_entropy(image) / 8.0

    # -----------------------------
    # Additional Useful Feature (OPTIONAL but helpful)
    # -----------------------------
    blue_red_ratio = b / (r + 1e-5)

    # -----------------------------
    # Final Feature Dictionary
    # -----------------------------
    features = {
        "r": r,
        "g": g,
        "b": b,
        "brightness": brightness,
        "contrast": contrast,
        "entropy": entropy,
        "blue_red_ratio": blue_red_ratio
    }

    # -----------------------------
    # Debug Print
    # -----------------------------
    if debug:
        print("\n[Feature Extraction]")
        for key, value in features.items():
            print(f"{key}: {value:.4f}")

    return features