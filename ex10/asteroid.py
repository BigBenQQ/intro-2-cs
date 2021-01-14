import coordinate as c
import math


class Asteroid:
    """
    the Asteroid class
    """

    def __init__(self, location: c.Coordinate, speed_vec: c.Coordinate, size: int = 3):
        """
        constructor
        :param location: the location of the asteroid
        :type location: c.Coordinate
        :param speed_vec: the speed vector of the asteroid
        :type speed_vec: c.Coordinate
        :param size: the asteroid size, default size is 3
        :type size: int
        """
        self.__location = location
        self.__speed_vec = speed_vec
        self.__size = size

    def get_location(self):
        """
        location getter
        :return: asteroid's location
        """
        return self.__location

    def get_speed(self):
        """
        speed vector getter
        :return: asteroid's speed vector
        """
        return self.__speed_vec

    def get_size(self):
        """
        size getter
        :return: asteroid's size
        """
        return self.__size

    def get_radius(self):
        """
        radius getter
        :return: asteroid's radius
        """
        return self.__size * 10 - 5

    def set_location(self, location):
        """
        location setter
        :param location: the new location
        :return: None
        """
        self.__location = location

    def has_intersection(self, obj):
        """
        checks if other object hit the asteroid
        :param obj: the obj that might hit the asteroid
        :return: True if intersection happened, otherwise - False
        """
        __distance = math.sqrt(
            math.pow((obj.get_location().get_x() - self.__location.get_x()), 2) + math.pow(
                (obj.get_location().get_y() - self.__location.get_y()), 2))

        # check if intersected
        if __distance <= self.get_radius() + obj.get_radius():
            return True

        return False
