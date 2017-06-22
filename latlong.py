from math import ceil
from type_check import *


class Point():
    @type_check
    def __init__(self, lat: (int, float), lng: (int, float), num: (int, float)) -> None:
        self.lat = lat
        self.lng = lng
        self.num = num

    @type_check
    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        return self.num == other.num

    @type_check
    def __repr__(self) -> str:
        return "Point( 0x" + str("{:010x}".format(self.num)) + " )"

    @type_check
    def __str__(self) -> str:
        return "Point( lat=" + "{:+07.3f}".format(self.lat) + ", long=" + "{:+08.3f}".format(self.lng) + " )"


@type_check
def encodeCoords(pts: str) -> int:
    # returns encoded decimal value of all points
    if len(pts.split(" ")) % 2:
        raise ValueError("Incomplete point")

    @type_check
    def lat(num: float) -> int:
        if num < -90 or num > 90:
            raise ValueError("Invalid latitude: " + str(num))
        num += 90
        num /= 180
        num *= 2**19 - 1
        # don't combine to << 39, as rounding has to occur between operations
        return round(num) << 20

    @type_check
    def lng(num: float) -> int:
        if num < -180 or num > 180:
            raise ValueError("Invalid longitude: " + str(num))
        num += 180
        num /= 360
        num *= 2**20 - 1
        return round(num)

    pts = pts.split(" ")
    encoded = 0

    for i in range(0, len(pts), 2):
        lt = lat(float(pts[i]))
        lg = lng(float(pts[i + 1]))

        encoded <<= 39  # first point is leftmost bits
        encoded += lt + lg

    return encoded


@type_check
def decodeCoords(bits: int) -> [Point]:
    if bits < 0:
        raise ValueError("Invalid value " + str(bits))

    @type_check
    def lat(num: int) -> float:
        num /= 2**19 - 1
        num *= 180
        return num - 90

    @type_check
    def lng(num: int) -> float:
        num /= 2**20 - 1
        num *= 360
        return num - 180

    pts = []
    bitPts = []

    # break into array of points # |1 is for special case of (-90,-180)
    for i in range(ceil(bits.bit_length() / 39) | 1):
        # right shift 39*i bits, then AND last 39 bits
        bitPts.insert(0, (bits >> (39 * i)) & (2**39 - 1))

    for pt in bitPts:
        lt = pt >> 20
        lg = pt & (2**20 - 1)
        pts.insert(0, Point(lat(lt), lng(lg), pt))

    return pts
