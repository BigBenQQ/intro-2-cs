import coordinate as c

DEFAULT_RADIUS = 4  # torpedo default radius
MAX_LIFE_CYCLE = 200  # number of turns in which the torpedo should stay alive

class Torpedo:
    def __init__(self, location: c.Coordinate, speed_vec: c.Coordinate, direction):
        self.__location = location
        self.__speed_vec = speed_vec
        self.__direction = direction
        self.__radius = DEFAULT_RADIUS
        self.__turns_alive = 0


    def get_location(self):
        return self.__location

    # def set_location(self, location: c.Coordinate):
    #     self.__location = location
    #
    # def set_location(self, x, y):
    #     self.__location.set_x(x)
    #     self.__location.set_y(y)

    def get_speed(self):
        return self.__speed_vec

    # def set_speed(self, speed_vec: c.Coordinate):
    #     self.__speed_vec = speed_vec
    #
    # def set_speed(self, speed_x, speed_y):
    #     self.__speed_vec.set_x(speed_x)
    #     self.__speed_vec.set_y(speed_y)

    def get_direction(self):
        return self.__direction

    def set_location(self, location: c.Coordinate):
        """

        :param location:
        :return:
        """
        self.__location = location

    def get_radius(self):
        return self.__radius

    def is_dead(self):
        return True if self.__turns_alive >= MAX_LIFE_CYCLE else False

    def increment_turns_alive(self):
        self.__turns_alive += 1

