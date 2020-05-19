
class Part:
    """Moments handler."""

    def __init__(self, color):
        self.color = color
        self.word_index = []

        self._i = 0
        self._j = 0

        self.m00 = 0  # area
        self.m01 = 0
        self.m10 = 0
        self.m11 = 0
        self.m02 = 0
        self.m20 = 0
        self.m21 = 0
        self.m12 = 0
        self.m03 = 0
        self.m30 = 0

        self.M00 = 0
        self.M01 = 0
        self.M10 = 0
        self.M11 = 0
        self.M20 = 0
        self.M02 = 0
        self.M21 = 0
        self.M12 = 0
        self.M30 = 0
        self.M03 = 0

        self.NM1 = 0
        self.NM2 = 0
        self.NM7 = 0


    def geom_moment(self, p, q):
        """p - rows, q - cols"""
        moment = 0
        for pixel in self.word_index:
            moment += pixel[0]**p * pixel[1]**q
        return moment

    def count_moments(self):
        self.m00 = self.geom_moment(0, 0)
        self.m01 = self.geom_moment(0, 1)
        self.m10 = self.geom_moment(1, 0)
        self.m11 = self.geom_moment(1, 1)
        self.m02 = self.geom_moment(0, 2)
        self.m20 = self.geom_moment(2, 0)
        self.m21 = self.geom_moment(2, 1)
        self.m12 = self.geom_moment(1, 2)
        self.m03 = self.geom_moment(0, 3)
        self.m30 = self.geom_moment(3, 0)

        self._i = self.m10 / self.m00
        self._j = self.m01 / self.m00

        self.M00 = self.m00
        self.M01 = self.m01 - (self.m01 / self.m00) * self.m00
        self.M10 = self.m10 - (self.m10 / self.m00) * self.m00
        self.M11 = self.m11 - self.m10 * self.m01 / self.m00
        self.M20 = self.m20 - self.m10**2 / self.m00
        self.M02 = self.m02 - self.m01**2 / self.m00
        self.M21 = self.m21 - 2 * self.m11 * self._i - self.m20 * self._j + 2 * self.m01 * self._i**2
        self.M12 = self.m12 - 2 * self.m11 * self._j - self.m02 * self._i + 2 * self.m10 * self._j**2
        self.M30 = self.m30 - 3 * self.m20 * self._i + 2 * self.m10 * self._i**2
        self.M03 = self.m03 - 3 * self.m02 * self._j + 2 * self.m01 * self._j**2

        self.NM1 = (self.M20 + self.M02) / (self.m00**2)
        self.NM2 = ((self.M20 - self.M02)**2 + 4 * self.M11**2) / (self.m00**4)
        self.NM7 = (self.M20 * self.M02 - self.M11**2) / (self.m00**4)
