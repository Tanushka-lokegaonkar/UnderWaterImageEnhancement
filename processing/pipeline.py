from .white_balance import WhiteBalance
from .clahe import CLAHEEnhancer
from .gamma import GammaCorrection
from .sharpen import Sharpen
from .SimpleSeaThru import StableSeaThru
import numpy as np
import cv2

from .wcid import WCID
from .dcp import DCP
from .dct import DCT

from .contrast_maximization import contrast_maximization
from .homomorphic_filtering import homomorphic_filter
from .guided_filtering import guided_filter_enhancement
from .hist_equalization import histogram_equalization

class EnhancementPipeline:

    def __init__(self, gamma=1.2, clip_limit=2.0):

        self.white_balance = WhiteBalance()
        self.clahe = CLAHEEnhancer(clip_limit)
        self.gamma = GammaCorrection(gamma)
        self.sharpen = Sharpen()
        self.seathru = StableSeaThru()

        self.wcid = WCID()
        self.dcp = DCP()
        self.dct = DCT()

    # def process(self, image, mode="standard"):

    #     if mode == "standard":
    #         image = self.white_balance.apply(image)
    #         image = self.clahe.apply(image)
    #         image = self.gamma.apply(image)
    #         image = self.sharpen.apply(image)

    #     elif mode == "wcid":
    #         image = self.wcid.apply(image)

    #     elif mode == "dcp":
    #         image = self.dcp.apply(image)

    #     elif mode == "dct":
    #         image = self.dct.apply(image)

    #     elif mode == "contrast":
    #         image = contrast_maximization(image)

    #     elif mode == "homomorphic":
    #         image = homomorphic_filter(image)
    #         image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    #     elif mode == "guided":
    #         image = guided_filter_enhancement(image)

    #     elif mode == "histogram":
    #         image = histogram_equalization(image)

    #     elif mode == "seathru":
    #         image = self.seathru.apply(image)

    #     return image

    def process(self, image, techniques):
        output = image.copy()

        for tech in techniques:

            if tech == "white_balance":
                output = self.white_balance.apply(output)

            elif tech == "gamma":
                output = self.gamma.apply(output)

            elif tech == "clahe":
                output = self.clahe.apply(output)

            elif tech == "sharpen":
                output = self.sharpen.apply(output)

            elif tech == "wcid":
                output = self.wcid.apply(output)

            elif tech == "dcp":
                output = self.dcp.apply(output)

            elif tech == "dct":
                output = self.dct.apply(output)

            elif tech == "contrast":
                output = contrast_maximization(output)

            elif tech == "homomorphic":
                h = homomorphic_filter(output)
                output = cv2.cvtColor(h, cv2.COLOR_GRAY2BGR)

            elif tech == "guided":
                output = guided_filter_enhancement(output)

            elif tech == "histogram":
                output = histogram_equalization(output)

            elif tech == "seathru":
                output = self.seathru.apply(output)

            elif tech == "fusion":
                # (Optional: if you don't have fusion yet, use this)
                output = self.white_balance.apply(output)
                output = self.clahe.apply(output)

        return output