import cv2
from processing.feature_extractor import extract_features

# Load test image
image = cv2.imread("test.jpg")   # place image in same root folder

# Extract features
features = extract_features(image, debug=True)

print("\nFinal Features Dictionary:")
print(features)