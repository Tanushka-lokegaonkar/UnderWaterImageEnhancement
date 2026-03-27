from .white_balance import WhiteBalance
from .clahe import CLAHEEnhancer
from .gamma import GammaCorrection
from .sharpen import Sharpen
from .sharpen2 import Sharpen2
from .SimpleSeaThru import StableSeaThru
from .quantum_enhancer import QuantumEnhancer

from .wcid import WCID
from .dcp import DCP
from .dct import DCT

from .contrast_maximization import contrast_maximization
from .homomorphic_filtering import homomorphic_filter
from .guided_filtering import guided_filter_enhancement
from .hist_equalization import histogram_equalization

from processing.feature_extractor import extract_features
from processing.decision_engine import DecisionEngine

from metrics.entropy import calculate_entropy

import numpy as np
import cv2


class EnhancementPipeline:

    def __init__(self, gamma=1.2, clip_limit=2.0):

        # Stronger defaults for visible output
        self.white_balance = WhiteBalance(percent=2)
        self.clahe = CLAHEEnhancer(clip_limit)
        self.gamma = GammaCorrection(gamma)
        self.sharpen = Sharpen(strength=2.0)
        self.sharpen2 = Sharpen2()

        self.seathru = StableSeaThru()
        self.quantum = QuantumEnhancer()

        self.wcid = WCID()
        self.dcp = DCP()
        self.dct = DCT()

        self.engine = DecisionEngine()

    # -----------------------------
    # EXISTING MODES (UNCHANGED)
    # -----------------------------
    def process(self, image, mode):

        if mode == "auto":
            return self.auto_process(image)

        if mode == "standard":
            image = self.white_balance.apply(image)
            image = self.clahe.apply(image)
            image = self.gamma.apply(image)
            image = self.sharpen2.apply(image)

        elif mode == "quantum_enhance":
            image = self.quantum.apply(image)

        elif mode == "wcid":
            image = self.wcid.apply(image)

        elif mode == "dcp":
            image = self.dcp.apply(image)

        elif mode == "dct":
            image = self.dct.apply(image)

        elif mode == "contrast":
            image = contrast_maximization(image)

        elif mode == "homomorphic":
            image = homomorphic_filter(image)
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        elif mode == "guided":
            image = guided_filter_enhancement(image)

        elif mode == "histogram":
            image = histogram_equalization(image)

        elif mode == "seathru":
            image = self.seathru.apply(image)

        return image

    # -----------------------------
    # AUTO MODE (FINAL HYBRID)
    # -----------------------------
    def auto_process(self, image):

        # STEP 1: Feature extraction
        features = extract_features(image, debug=True)

        # STEP 2: Get smart candidates
        candidates, scores = self.engine.get_final_candidates(features)

        print("\nCandidates:", candidates)

        best_score = -1
        best_output = image
        best_mode = None

        # STEP 3: Evaluate candidates
        for mode in candidates:
            try:
                temp = self.process(image.copy(), mode)

                # Metrics
                entropy = calculate_entropy(temp)
                contrast = np.std(cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY))
                brightness = np.mean(cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY))

                # Combined score (balanced)
                score = entropy + 0.4 * contrast + 0.2 * brightness

                print(f"{mode} → score: {score:.2f}")

                if score > best_score:
                    best_score = score
                    best_output = temp
                    best_mode = mode

            except Exception as e:
                print(f"{mode} failed:", e)

        print("\n✅ Best mode selected:", best_mode)

        return best_output, best_mode