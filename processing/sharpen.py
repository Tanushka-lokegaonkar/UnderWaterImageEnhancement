import cv2
import numpy as np

class Sharpen:
    """
    Adaptive Unsharp Masking for better edge enhancement
    """

    def __init__(self, strength=1.8):
        self.strength = strength

    def apply(self, image):
        # Step 1: Mild Gaussian blur
        blurred = cv2.GaussianBlur(image, (5, 5), 1.0)

        # Step 2: Extract details
        detail = cv2.subtract(image, blurred)

        # Step 3: Add amplified details back
        sharpened = cv2.add(image, self.strength * detail)

        # Clip to valid range
        sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)

        return sharpened