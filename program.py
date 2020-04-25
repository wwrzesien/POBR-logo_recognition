"""
Rozpoznawanie loga firmy FedEx.

Dozwolone funkcje:
imread, imwrite, Mat, _Mat, imshow, waitKey
"""

import cv2
import numpy as np
# from matplotlib import pyplot as plt

path = './images/'


def main() -> int:
    """Główna funkcja."""
    # Read images
    image = cv2.imread(path + 'fedex_1.jpg', 1)

    # Shwo image in the window
    cv2.imshow('FedEx', image)

    cv2.waitKey(0)
    cv2.destroyWindow('FedEx')

    return 0


if __name__ == "__main__":
    main()
