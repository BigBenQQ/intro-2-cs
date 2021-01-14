def is_name_in_car_list(name, car_list):
    for car in car_list:
        if car.get_name() == name:
            return car
    return False


class Board:
    """
    Add a class description here.
    Write briefly about the purpose of the class
    """
    BOARD_ROWS = 7
    BOARD_COLS = 7

    END_COORDINATE = (3, 7)

    BORDER = "*"
    EMPTY_SPACE = "_"
    ESCAPE = "E"

    MOVES = {
        "l": "left",
        "r": "right",
        "u": "up",
        "d": "down"
    }

    def __init__(self):
        # implement your code and erase the "pass"
        # Note that this function is required in your Board implementation.
        # However, is not part of the API for general board types.
        self.__rows = self.BOARD_ROWS
        self.__cols = self.BOARD_COLS

        # (coordinate: tuple, name: str)
        self.__coordinates_map = dict()
        for i in range(self.BOARD_ROWS):
            for j in range(self.BOARD_COLS):
                self.__coordinates_map[(i, j)] = self.EMPTY_SPACE
                if i == 3 and j == 6:
                    self.__coordinates_map[self.END_COORDINATE] = self.EMPTY_SPACE
        self.__car_lst = list()

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # The game may assume this function returns a reasonable representation
        # of the board for printing, but may not assume details about it.
        out_str = ""

        out_str += self.BORDER * (self.BOARD_ROWS + 2) + "\n"

        for row in range(self.BOARD_ROWS):
            out_str += self.BORDER
            for col in range(self.BOARD_COLS):
                content = self.cell_content((row, col))
                if content is None:
                    out_str += self.EMPTY_SPACE
                else:
                    out_str += content
            if row == 3:
                out_str += self.ESCAPE + "\n"
            else:
                out_str += self.BORDER + "\n"

        out_str += self.BORDER * (self.BOARD_ROWS + 2) + "\n"
        return out_str

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)

        return [x for x in self.__coordinates_map.keys()]

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        move_list = []
        if len(self.__car_lst) != 0:
            # run through all cars
            for car in self.__car_lst:
                # check each possible direction
                for direction in list("lrud"):
                    requirement = car.movement_requirements(direction)
                    if len(requirement) == 0:
                        continue

                    # if the requirement is out of cols range
                    if requirement[0][1] < 0 or requirement[0][1] >= self.__cols:
                        continue

                        # if the requirement is out of rows range
                    if (not requirement[0] == list(self.END_COORDINATE)) and \
                            (requirement[0][0] < 0 or requirement[0][0] >= self.__rows):
                        continue

                    # if the car can go the this coordinate
                    if self.cell_content(tuple(requirement[0])) is None:
                        move_list.append((car.get_name(), direction,
                                          f"{car.get_name()} can drive {self.MOVES[direction]}"))
                    else:
                        continue
        return move_list

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        return self.END_COORDINATE

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        if self.__coordinates_map[coordinate] == self.EMPTY_SPACE:
            return None
        return self.__coordinates_map[coordinate]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"

        # if car already exists
        if car.get_name() in self.__coordinates_map.values():
            return False

        # TODO - check double code
        temp_dict = dict()
        for car_coordinate in car.car_coordinates():
            car_coordinate = tuple(car_coordinate)
            # coordinate is in the board region
            if car_coordinate not in self.__coordinates_map:
                return False
            # on empty space
            if self.__coordinates_map[car_coordinate] != self.EMPTY_SPACE:
                return False

            # TODO - think of more bad cases
            temp_dict[car_coordinate] = car.get_name()

        self.__coordinates_map.update(temp_dict)
        self.__car_lst.append(car)
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        cur_car = is_name_in_car_list(name, self.__car_lst)
        # name not found in car list
        if cur_car is False:
            return False

        old_coordinates = cur_car.car_coordinates()
        if not self._is_next_move_valid(cur_car, movekey):
            return False

        cur_car.move(movekey)
        new_coordinates = cur_car.car_coordinates()

        if movekey == "r" or movekey == "d":
            to_empty = tuple(min(old_coordinates))
            to_car = tuple(max(new_coordinates))
            changed_coord = {
                to_empty: self.EMPTY_SPACE,
                to_car: cur_car.get_name()
            }

        else:  # if movekey == "l" or "u":
            to_empty = tuple(max(old_coordinates))
            to_car = tuple(min(new_coordinates))
            changed_coord = {
                to_empty: self.EMPTY_SPACE,
                to_car: cur_car.get_name()
            }

        self.__coordinates_map.update(changed_coord)
        return True

    def _is_next_move_valid(self, car, movekey: str):
        possible_moves_dict = car.possible_moves()
        if movekey not in possible_moves_dict:
            return False

        if movekey == "r":
            temp_coor = list(max(car.car_coordinates()))
            temp_coor[1] += 1
            if not self._is_in_range(temp_coor):
                return False
            content = self.cell_content(tuple(temp_coor))
            if (content is not None) and (content != self.ESCAPE):
                return False

        elif movekey == "d":
            temp_coor = list(max(car.car_coordinates()))
            temp_coor[0] += 1
            if not self._is_in_range(temp_coor):
                return False
            if self.cell_content(tuple(temp_coor)) is not None:
                return False

        elif movekey == "l":
            temp_coor = list(min(car.car_coordinates()))
            temp_coor[1] -= 1
            if not self._is_in_range(temp_coor):
                return False
            if self.cell_content(tuple(temp_coor)) is not None:
                return False

        elif movekey == "u":
            temp_coor = list(min(car.car_coordinates()))
            temp_coor[0] -= 1
            if not self._is_in_range(temp_coor):
                return False
            if self.cell_content(tuple(temp_coor)) is not None:
                return False

        else:
            return False

        return True

    def _is_in_range(self, coordinate):
        if tuple(coordinate) == self.END_COORDINATE:
            return True

        if (0 <= coordinate[0] < self.__rows) and \
                (0 <= coordinate[1] < self.__cols):
            return True

        else:
            return False
