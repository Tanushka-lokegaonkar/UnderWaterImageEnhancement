import cv2

class Sharpen:
    def apply(self, image):
        # Using a stronger unsharp mask approach
        gaussian_blur = cv2.GaussianBlur(image, (9, 9), 10.0)
        return cv2.addWeighted(image, 1.5, gaussian_blur, -0.5, 0)
