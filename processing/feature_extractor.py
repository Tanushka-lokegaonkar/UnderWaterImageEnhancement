import cv2
import numpy as np
from metrics.entropy import calculate_entropy

def get_color_means(image):
    b = np.mean(image[:, :, 0])
    g = np.mean(image[:, :, 1])
    r = np.mean(image[:, :, 2])

    return r, g, b


def get_brightness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return np.mean(gray)


def get_contrast(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray.std()


def get_entropy_value(image):
    return calculate_entropy(image)


def get_color_ratios(r, g, b):
    epsilon = 1e-5
    ratios = {
        'blue_red_ratio': b / (r + epsilon),
        'green_red_ratio': g / (r + epsilon)
    }
    return ratios


def normalize_features(features):
    normalized = {}

    normalized['r'] = features['r'] / 255.0
    normalized['g'] = features['g'] / 255.0
    normalized['b'] = features['b'] / 255.0

    normalized['brightness'] = features['brightness'] / 255.0
    normalized['contrast'] = features['contrast'] / 128.0

    normalized['entropy'] = features['entropy'] / 8.0

    normalized['blue_red_ratio'] = features['blue_red_ratio']
    normalized['green_red_ratio'] = features['green_red_ratio']

    return normalized


def extract_features(image, normalize=True, debug=False):
    if image is None:
        raise ValueError("Invalid image input. Image is None.")

    features = {}

    r, g, b = get_color_means(image)
    features['r'] = r
    features['g'] = g
    features['b'] = b

    features['brightness'] = get_brightness(image)

    features['contrast'] = get_contrast(image)

    features['entropy'] = get_entropy_value(image)

    ratios = get_color_ratios(r, g, b)
    features.update(ratios)

    if normalize:
        features = normalize_features(features)

    if debug:
        print("\n[Feature Extraction Debug]")
        for key, value in features.items():
            print(f"{key}: {value:.4f}")

    return features