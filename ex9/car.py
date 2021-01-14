class Car:
    """
    Add class description here
    """
    VERTICAL = 0
    HORIZONTAL = 1

    LEFT = "l"
    RIGHT = "r"
    UP = "u"
    DOWN = "d"
    ALL_DIRECTIONS = [LEFT, RIGHT, UP, DOWN]

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's butt (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # However, is not part of the API for general car types.
        # implement your code and erase the "pass"
        self.__name = name
        if length > 0 and type(length) == int:
            self.__length = length
        else:
            self.__length = 1
        self.__location = location
        self.__orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        coordinates = []
        if self.__orientation == self.HORIZONTAL:
            for i in range(self.__location[1], self.__location[1] + self.__length):
                coordinates.append((self.__location[0], i))

        else:
            for i in range(self.__location[0], self.__location[0] + self.__length):
                coordinates.append((i, self.__location[1]))

        return coordinates

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        # For this car type, keys are from 'udrl'
        # The keys for vertical cars are 'u' and 'd'.
        # The keys for horizontal cars are 'l' and 'r'.
        # You may choose appropriate strings.
        # implement your code and erase the "pass"
        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        # A car returning this dictionary supports the commands 'f','d','a'.

        if self.__orientation == self.HORIZONTAL:
            # can, at most, go left and right
            return {
                "r": "drive right",
                "l": "drive left"
                    }
        else:
            # can, at most, go up and down
            return {
                "u": "drive up",
                "d": "drive down"
            }

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        # For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        # be empty in order to move down (with a key 'd').

        # if list(movekey) not in self.ALL_DIRECTIONS: #TODO - check how to make this checking work
        #     return

        cur_location = list(self.__location)
        requirements_lst = []

        if self.__orientation == self.HORIZONTAL:
            if self.RIGHT in movekey:
                cur_location[1] += self.__length
                requirements_lst.append(tuple(cur_location))
                cur_location = list(self.__location)

            if self.LEFT in movekey:
                cur_location[1] -= 1
                requirements_lst.append(tuple(cur_location))

        else:
            if self.DOWN in movekey:
                cur_location[0] += self.__length
                requirements_lst.append(tuple(cur_location))
                cur_location = list(self.__location)

            if self.UP in movekey:
                cur_location[0] -= 1
                requirements_lst.append(tuple(cur_location))

        return requirements_lst

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        # if movekey in self.ALL_DIRECTIONS:
        #     pass

        requirements = self.movement_requirements(movekey)
        if self.__orientation == self.HORIZONTAL:
            if movekey == self.RIGHT:
                new_loc = list(self.__location)
                new_loc[1] += 1
                self.__location = tuple(new_loc)

            elif movekey == self.LEFT:
                new_loc = list(self.__location)
                new_loc[1] -= 1
                self.__location = tuple(new_loc)

            else:
                return False

        elif self.__orientation == self.VERTICAL:
            if movekey == self.DOWN:
                new_loc = list(self.__location)
                new_loc[0] += 1
                self.__location = tuple(new_loc)

            elif movekey == self.UP:
                new_loc = list(self.__location)
                new_loc[0] -= 1
                self.__location = tuple(new_loc)

            else:
                return False

        else:
            return False

        return True

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name
