import cv2
import numpy as np

class StableSeaThru:
    def __init__(self, omega=0.85, t0=0.2):
        self.omega = omega
        self.t0 = t0

    def estimate_backscatter(self, img):
        B = []
        for c in range(3):
            channel = img[:, :, c]
            flat = channel.flatten()

            threshold = np.percentile(flat, 99)
            bright_pixels = flat[flat >= threshold]

            B.append(np.mean(bright_pixels))

        return np.array(B)

    def estimate_transmission(self, img):
        min_channel = np.min(img, axis=2)
        t = 1 - self.omega * min_channel
        t = cv2.GaussianBlur(t, (15, 15), 0)
        return np.clip(t, self.t0, 1)

    def apply(self, image):
        img = image.astype(np.float32) / 255.0

        B = self.estimate_backscatter(img)
        t = self.estimate_transmission(img)

        J = np.zeros_like(img)
        for c in range(3):
            J[:, :, c] = (img[:, :, c] - B[c]) / t + B[c]

        J = np.clip(J, 0, 1)

        return (J * 255).astype(np.uint8)