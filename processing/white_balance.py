import cv2
import numpy as np

class WhiteBalance:
    """Stretches R, G, and B channels independently to restore color depth."""
    def __init__(self, percent=2):
        self.percent = percent

    def apply(self, image):
        # Ensure we are working with uint8
        img = image.astype(np.uint8)
        out_channels = []
        half_percent = self.percent / 200.0
        
        for channel in cv2.split(img):
            # Find the intensity thresholds
            flat = channel.flatten()
            flat.sort()
            low_val = flat[int(len(flat) * half_percent)]
            high_val = flat[int(len(flat) * (1 - half_percent))]
            
            # Stretch the channel and clip
            stretched = cv2.normalize(channel, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            out_channels.append(np.clip(stretched, 0, 255))
            
        return cv2.merge(out_channels)
