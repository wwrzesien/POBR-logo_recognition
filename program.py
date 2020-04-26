"""
Rozpoznawanie loga firmy FedEx.

Dozwolone funkcje:
imread, imwrite, Mat, _Mat, imshow, waitKey
"""

import cv2
import numpy as np
from recognition import Recognizer


path = './images/'


def main() -> int:
    """Główna funkcja."""

    filename = 'fedex_2.jpg'

    # Read images
    image = cv2.imread(path + filename, 1)

    # Resize image ()
    # half = cv2.resize(image, (0, 0), fx=0.7, fy=0.7)

    logo_recog = Recognizer(image)
    logo_recog.recognize()

    # Shwo image in the window
    cv2.imshow('FedEx', image)

    cv2.waitKey(0)
    cv2.destroyWindow('FedEx')
    return 0


if __name__ == "__main__":
    main()
