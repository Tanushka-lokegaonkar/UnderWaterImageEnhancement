import pennylane as qml
from pennylane import numpy as np
import cv2

class QuantumEnhancer:
    def __init__(self):
        # Light quantum circuit
        self.dev = qml.device("default.qubit", wires=4)

        # Predefined learned weights (instead of random every patch)
        self.weights = np.random.rand(1, 4, 3)

        @qml.qnode(self.dev)
        def q_feature(inputs):
            # Encode 4 global image features (not patches!)
            for i in range(4):
                qml.RY(inputs[i] * np.pi, wires=i)

            # One small entangling layer
            qml.StronglyEntanglingLayers(self.weights, wires=range(4))

            # Return 1 qubit output → a global weighting factor
            return qml.expval(qml.PauliZ(3))

        self.q_feature = q_feature

    def extract_features(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Normalize feature values between 0–1
        b = np.mean(gray) / 255
        c = np.std(gray) / 255
        r_mean = image[:, :, 2].mean() / 255
        g_mean = image[:, :, 1].mean() / 255

        return np.array([b, c, r_mean, g_mean])

    def apply(self, image):
        # Step 1: extract global features → 4 numbers
        features = self.extract_features(image)

        # Step 2: quantum inference (only once!)
        q_value = float(self.q_feature(features))

        # Step 3: convert -1..1 → enhancement factor
        alpha = 1.0 + (q_value * 0.5)    # range: 0.5 → 1.5

        # Step 4: apply enhancement
        enhanced = cv2.convertScaleAbs(image, alpha=alpha, beta=0)

        return enhanced