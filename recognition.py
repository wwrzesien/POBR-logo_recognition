import numpy as np
import cv2


class Recognizer:
    """Image recognition handler."""

    def __init__(self, image):
        self.image = np.copy(image)

    def recognize(self):
        """Perform image recognition."""
        pass

    def segmentation(self):
        """Perform segmentation."""
        pass

    def recognition(self):
        """Perform recognition."""
        pass
