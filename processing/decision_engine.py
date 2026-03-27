class DecisionEngine:
    """
    Hybrid Decision Engine:
    1. Uses features to shortlist candidate modes
    2. Removes duplicates
    3. Ensures strong fallback methods
    """

    def __init__(self):
        pass

    # -----------------------------
    # Feature-based candidate selection
    # -----------------------------
    def get_candidate_modes(self, features):

        candidates = []

        r = features['r']
        g = features['g']
        b = features['b']
        brightness = features['brightness']
        contrast = features['contrast']
        entropy = features['entropy']

        # -----------------------------
        # COLOR CAST (Underwater blue dominance)
        # -----------------------------
        if b > r + 0.05:
            candidates += ["dcp", "seathru", "standard"]

        # -----------------------------
        # LOW CONTRAST
        # -----------------------------
        if contrast < 0.4:
            candidates += ["contrast", "histogram", "standard"]

        # -----------------------------
        # LOW BRIGHTNESS
        # -----------------------------
        if brightness < 0.5:
            candidates += ["gamma", "homomorphic", "standard"]

        # -----------------------------
        # LOW DETAIL (LOW ENTROPY)
        # -----------------------------
        if entropy < 0.7:
            candidates += ["sharpen", "guided", "standard"]

        # -----------------------------
        # ALWAYS INCLUDE STRONG METHODS
        # -----------------------------
        candidates += ["standard", "wcid", "fusion"]

        # Remove duplicates
        candidates = list(set(candidates))

        return candidates


    # -----------------------------
    # Optional: Priority Sorting (BONUS)
    # -----------------------------
    def rank_modes(self, features, candidates):
        """
        Assign simple priority scores to candidate modes
        (Not final decision — just ordering)
        """

        scores = {}

        brightness = features['brightness']
        contrast = features['contrast']
        entropy = features['entropy']
        r = features['r']
        b = features['b']

        for mode in candidates:

            if mode == "dcp":
                scores[mode] = (b - r) + (1 - contrast)

            elif mode == "seathru":
                scores[mode] = (b - r) + (1 - brightness)

            elif mode == "clahe":
                scores[mode] = (1 - contrast)

            elif mode == "gamma":
                scores[mode] = (1 - brightness)

            elif mode == "sharpen":
                scores[mode] = (1 - entropy)

            elif mode == "homomorphic":
                scores[mode] = (1 - brightness) + (1 - contrast)

            elif mode == "contrast":
                scores[mode] = (1 - contrast)

            elif mode == "histogram":
                scores[mode] = (1 - contrast)

            else:
                scores[mode] = 0.5  # neutral

        # Sort descending
        ranked = sorted(scores, key=scores.get, reverse=True)

        return ranked, scores


    # -----------------------------
    # FINAL METHOD (USED IN PIPELINE)
    # -----------------------------
    def get_final_candidates(self, features):

        # Step 1: Get candidates
        candidates = self.get_candidate_modes(features)

        # Step 2: Rank them (optional but useful)
        ranked, scores = self.rank_modes(features, candidates)

        # Step 3: Limit to top N (for speed)
        top_candidates = ranked[:5]

        return top_candidates, scores