import cv2
import numpy as np

class CLAHEEnhancer:
    def __init__(self, clip_limit=2.0):
        self.clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8,8))

    def apply(self, image):
        # Convert to LAB - Ensure image is uint8 first to avoid the CV_64F error
        img_uint8 = np.clip(image, 0, 255).astype(np.uint8)
        lab = cv2.cvtColor(img_uint8, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE ONLY to the L (Lightness) channel
        cl = self.clahe.apply(l)
        
        limg = cv2.merge((cl, a, b))
        return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
