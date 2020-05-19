import numpy as np
import cv2
import random
from moments import Part

# RGB
# BLUE_MIN = [60, 10, 50]
# BLUE_MAX = [110, 50, 70]
# RED_MIN = [0, 30, 130]
# RED_MAX = [40, 95, 220]

# fedex 1
# BLUE_MIN = [125, 122, 75]
# BLUE_MAX = [135, 230, 128]
# RED_MIN = [10, 170, 115]
# RED_MAX = [18, 243, 180]

# HSV fedex 2
# BLUE_MIN = [110, 122, 76]
# BLUE_MAX = [135, 150, 105]
# RED_MIN = [0, 200, 200]
# RED_MAX = [2, 230, 230]

# HSV fedex 3
# PUR_MIN = [138, 163, 71]
# PUR_MAX = [140, 230, 84]
# RED_MIN = [4, 242, 191]
# RED_MAX = [6, 255, 217]

# fedex 4
# BLUE_MIN = [115, 38, 76]
# BLUE_MAX = [145, 102, 160]
# RED_MIN = [0, 125, 153]
# RED_MAX = [7, 200, 255]

BLUE_MIN = [110, 122, 71]
BLUE_MAX = [144, 230, 105]
RED_MIN = [0, 200, 191]
RED_MAX = [6, 255, 230]



class Recognizer:
    """Image recognition handler."""

    def __init__(self, image, filename):
        self.image = np.copy(image)
        self.filename = filename

        self.fuzzy_image = None
        self.hsv_image = None
        self.thresh_image = None
        self.segmen_image = None
        self.recog_image = None

        self.rows = image.shape[0]
        self.cols = image.shape[1]
        self.parts = []  # Fed, E, x

    def recognize(self):
        """Perform image recognition."""
        norm = 10
        # Filtr usredniajacy
        conv = [
                [1/norm, 1/norm, 1/norm],
                [1/norm, 2/norm, 1/norm],
                [1/norm, 1/norm, 1/norm]
            ]

        self.fuzzy_image = self.convolution(conv)
        cv2.imwrite("conv.jpg", self.fuzzy_image)

        # # Convert BGR to HSV
        self.hsv_image = cv2.cvtColor(self.fuzzy_image, cv2.COLOR_BGR2HSV)

        self.thresholding()
        cv2.imwrite("tresholding.jpg", self.thresh_image)
        cv2.imshow('FedEx', self.thresh_image)

        self.segmentation()
        cv2.imwrite("segmen.jpg", self.segmen_image)

        self.calculate_moments()
        self.recognition()

        cv2.imshow('FedEx', self.image)
        cv2.imwrite("results/" + self.filename, self.image)

    def thresholding(self):
        """Create black-white image."""
        self.thresh_image = np.copy(self.image)

        for row in range(self.rows):
            for col in range(self.cols):
                if (self.detect_blue(self.hsv_image[row, col])) or (self.detect_red(self.hsv_image[row, col])):
                    self.thresh_image[row, col] = [255, 255, 255]
                else:
                    self.thresh_image[row, col] = [0, 0, 0]

    def segmentation(self):
        """Perform segmentation."""
        self.segmen_image = np.copy(self.thresh_image)
        i = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.segmen_image[row, col, 0] == 255 and self.segmen_image[row, col, 1] == 255 and self.segmen_image[row, col, 2] == 255:
                    # cv2.floodFill(self.segmen_image, None, (y, x), color[i])

                    color = self.get_color(i)
                    self.parts.append(Part(color))

                    self.flood_fill((row, col), color)
                    i += 1
        self.remove_small_parts()
        print(len(self.parts))

        #     # Invert floodfilled image
        # im_floodfill_inv = cv2.bitwise_not(image)
        #
        # # Combine the two images to get the foreground.
        # im_out = image | im_floodfill_inv
        # return seg_imag

    def calculate_moments(self):
        """Calculate moments for parts."""
        for part in self.parts:
            part.count_moments()
            print("Color, NM1, NM2, NM7")
            print(part.color, part.NM1, part.NM2, part.NM7)
            print(len(part.word_index))

    def recognition(self):
        """Perform recognition."""
        self.recog_image = np.copy(self.segmen_image)
        Fed = []
        E = []
        x = []
        start_line = 0
        end_line = 0

        Fed_line = {
            "min": [],
            "max": [],
        }
        x_line = {
            "min": [],
            "max": [],
        }

        for part in self.parts:
            if self.is_Fed(part):
                Fed.append(part)
            elif self.is_E(part):
                E.append(part)
            elif self.is_x(part):
                x.append(part)
            else:
                for pixel in part.word_index:
                    self.recog_image[pixel[0], pixel[1], 0] = 0
                    self.recog_image[pixel[0], pixel[1], 1] = 0
                    self.recog_image[pixel[0], pixel[1], 2] = 0

        for part in Fed:
            row_min = np.copy(self.rows)
            col_min = np.copy(self.cols)
            row_max = col_max = 0
            for pixel in part.word_index:
                if pixel[0] > row_max:
                    row_max = np.copy(pixel[0])
                if pixel[0] < row_min:
                    row_min = np.copy(pixel[0])
                if pixel[1] > col_max:
                    col_max = np.copy(pixel[1])
                if pixel[1] < col_min:
                    col_min = np.copy(pixel[1])
            Fed_line["min"].append((row_min, col_min))
            Fed_line["max"].append((row_max, col_max))

        for part in x:
            row_min = np.copy(self.rows)
            col_min = np.copy(self.cols)
            row_max = col_max = 0
            for pixel in part.word_index:
                if pixel[0] > row_max:
                    row_max = np.copy(pixel[0])
                if pixel[0] < row_min:
                    row_min = np.copy(pixel[0])
                if pixel[1] > col_max:
                    col_max = np.copy(pixel[1])
                if pixel[1] < col_min:
                    col_min = np.copy(pixel[1])
            x_line["min"].append((row_min, col_min))
            x_line["max"].append((row_max, col_max))

        for i, value in enumerate(Fed_line["min"]):
            row_min = x_line["min"][i][0] if (Fed_line["min"][i][0] > x_line["min"][i][0]) else Fed_line["min"][i][0]
            row_max = Fed_line["max"][i][0] if (Fed_line["max"][i][0] > x_line["max"][i][0]) else x_line["max"][i][0]
            col_min = Fed_line["min"][i][1]
            col_max = x_line["max"][i][1]
            start_line = (col_min, row_min)
            end_line = (col_max, row_max)

            print(start_line)
            print(end_line)

            cv2.rectangle(self.image, start_line, end_line, (0, 100, 0), 1)

    def flood_fill(self, position, part_color):
        """Divide image into separate parts."""
        position_queue = []
        position_queue.append(position)

        while position_queue:
            current = position_queue[0]
            position_queue.pop(0)

            self.segmen_image[current[0], current[1], 0] = part_color[0]
            self.segmen_image[current[0], current[1], 1] = part_color[1]
            self.segmen_image[current[0], current[1], 2] = part_color[2]

            self.parts[-1].word_index.append(current)

            # current[1] -> x , current[0] -> y in coordinate system
            # in image: row -> y, col -> x

            left = (current[0], current[1]-1)
            right = (current[0], current[1]+1)
            top = (current[0]-1, current[1])
            bottom = (current[0]+1, current[1])

            if left[1] >= 0 and self.segmen_image[left[0], left[1], 0] == 255:
                if self.segmen_image[left[0], left[1], 1] == 255:
                    if self.segmen_image[left[0], left[1], 2] == 255:
                        if left not in position_queue:
                            position_queue.append(left)

            if right[1] < self.cols and self.segmen_image[right[0], right[1], 0] == 255:
                if self.segmen_image[right[0], right[1], 1] == 255:
                    if self.segmen_image[right[0], right[1], 2] == 255:
                        if right not in position_queue:
                            position_queue.append(right)

            if top[0] >= 0 and self.segmen_image[top[0], top[1], 0] == 255:
                if self.segmen_image[top[0], top[1], 1] == 255:
                    if self.segmen_image[top[0], top[1], 2] == 255:
                        if top not in position_queue:
                            position_queue.append(top)

            if bottom[0] < self.rows and self.segmen_image[bottom[0], bottom[1], 0] == 255:
                if self.segmen_image[bottom[0], bottom[1], 1] == 255:
                    if self.segmen_image[bottom[0], bottom[1], 2] == 255:
                        if bottom not in position_queue:
                            position_queue.append(bottom)

    def convolution(self, filtr):
        """Perform convolution."""
        def cut(vector):
            for index, value in enumerate(vector):
                if value >= 255:
                    vector[index] = 255
                elif value <= 0:
                    vector[index] = 0
            return vector

        img = np.copy(self.image)

        for row in range(1, self.rows-1):
            for col in range(1, self.cols-1):
                tmp = [0, 0, 0]
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        tmp[0] += self.image[row+k, col+l, 0] * filtr[1+k][1+l]
                        tmp[1] += self.image[row+k, col+l, 1] * filtr[1+k][1+l]
                        tmp[2] += self.image[row+k, col+l, 2] * filtr[1+k][1+l]
                img[row, col] = cut(tmp)
        return img

    def detect_blue(self, pixel):
        """Detect blue color."""
        if (pixel[0] >= BLUE_MIN[0] and pixel[0] <= BLUE_MAX[0]):
            if (pixel[1] >= BLUE_MIN[1] and pixel[1] <= BLUE_MAX[1]):
                if (pixel[2] >= BLUE_MIN[2] and pixel[2] <= BLUE_MAX[2]):
                    return True
        return False

    def detect_red(self, pixel):
        """Detect red color."""
        if (pixel[0] >= RED_MIN[0] and pixel[0] <= RED_MAX[0]):
            if (pixel[1] >= RED_MIN[1] and pixel[1] <= RED_MAX[1]):
                if (pixel[2] >= RED_MIN[2] and pixel[2] <= RED_MAX[2]):
                    return True
        return False

    def remove_small_parts(self):
        """Remove parts with area less than 10px."""
        to_remove = []
        for index, part in enumerate(self.parts):
            if len(part.word_index) < 30:
                for pixel in part.word_index:
                    self.segmen_image[pixel[0], pixel[1], 0] = 0
                    self.segmen_image[pixel[0], pixel[1], 1] = 0
                    self.segmen_image[pixel[0], pixel[1], 2] = 0
                self.parts.remove(part)

        # for index in to_remove:
        #     print(index)
        #     self.parts.pop(index)

    def get_color(self, i):
        """Get color for part."""
        color = [
            [255, 0, 0],
            [0, 255, 0],
            [0, 0, 255],
        ]

        for n in range(500):
            b = random.randint(0, 255)
            g = random.randint(0, 255)
            r = random.randint(0, 255)
            color.append([b, g, r])

        return color[i]

    def is_Fed(self, part):
        """Check whether part is Fed element."""
        if part.NM1 >= 0.4 and part.NM1 <= 0.5:
            if part.NM2 >= 0.09 and part.NM2 <= 0.11:
                if part.NM7 >= 0.02 and part.NM7 <= 0.27:
                    return True
        return False

    def is_E(self, part):
        """Check whether part is E element."""
        if part.NM1 >= 0.28 and part.NM1 <= 0.31:
            if part.NM2 >= 0.033 and part.NM2 <= 0.038:
                if part.NM7 >= 0.012 and part.NM7 <= 0.016:
                    return True
        return False

    def is_x(self, part):
        """Check whether part is x element."""
        if part.NM1 >= 0.24 and part.NM1 <= 0.25:
            if part.NM2 >= 0.00008 and part.NM2 <= 0.00016:
                if part.NM7 >= 0.014 and part.NM7 <= 0.016:
                    return True
        return False
