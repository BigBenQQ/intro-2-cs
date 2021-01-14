import coordinate as c

RADIUS = 1
MAX_AMMO = 10


class Ship:
    """

    """

    def __init__(self, location: c.Coordinate, speed_vec: c.Coordinate = c.Coordinate(),
                 direction=0):
        self.__location = location
        self.__speed_vec = speed_vec
        self.__direction = direction
        self.__shots_fired = 0

    def get_location(self):
        """

        :return:
        """
        return self.__location

    def set_location(self, location: c.Coordinate):
        """

        :param location:
        :return:
        """
        self.__location = location

    # def set_location(self, x, y):
    #     """
    #
    #     :param x:
    #     :param y:
    #     :return:
    #     """
    #     self.__location.set_x(x)
    #     self.__location.set_y(y)

    def get_speed(self):
        """

        :return:
        """
        return self.__speed_vec

    def set_speed(self, speed_vec: c.Coordinate):
        self.__speed_vec = speed_vec

    # def set_speed(self, speed_x, speed_y):
    #     """
    #
    #     :param speed_x:
    #     :param speed_y:
    #     :return:
    #     """
    #     self.__speed_vec.set_x(speed_x)
    #     self.__speed_vec.set_y(speed_y)

    def get_direction(self):
        """

        :return:
        """
        return self.__direction

    def set_direction(self, direction):
        """
        sets the direction (degrees) of the ship
        :param direction: Integer, the current degrees of the direction of the ship
        :return: None
        """
        self.__direction = direction

    def get_radius(self):
        return RADIUS

    def fire(self):
        self.__shots_fired += 1

    def decrement_torpedoes_shots(self):
        self.__shots_fired -= 1

    def max_torpedo_reached(self):
        return True if self.__shots_fired >= MAX_AMMO else False

