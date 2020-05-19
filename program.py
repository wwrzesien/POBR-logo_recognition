"""
Rozpoznawanie loga firmy FedEx.

Dozwolone funkcje:
imread, imwrite, Mat, _Mat, imshow, waitKey
"""

import cv2
import numpy as np
from recognition import Recognizer

PATH = './images/'


def main() -> int:
    """Główna funkcja."""

    # filename = 'fedex_1.jpg'
    filename = 'fedex_2.jpg'
    # filename = 'fedex_3.jpg'
    # filename = 'fedex_4.jpg'
    # filename = 'tresholding.jpg'

    # Read images
    image = cv2.imread(PATH + filename, 1)

    # Resize image ()
    if filename == 'fedex_1.jpg':
        image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

    logo_recog = Recognizer(image, filename)
    logo_recog.recognize()

    # Shwo image in the window
    # cv2.imshow('FedEx', image)

    cv2.waitKey(0)
    cv2.destroyWindow('FedEx')
    return 0


if __name__ == "__main__":
    main()
