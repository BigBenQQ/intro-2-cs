import random
import math
from screen import *
from ship import *
from asteroid import *
from torpedo import *
from coordinate import *
import sys

DEFAULT_ASTEROIDS_NUM = 5
DEFAULT_LIVES = 3


class GameRunner:
    """
    this is the main class that manages the game flow
    """

    # messages constants
    QUIT_HEAD = "QUIT"
    QUIT_MSG = "Bye Bye!"
    WIN_HEAD = "HURRAY!"
    WIN_MSG = "You WON!"

    def __init__(self, asteroids_amount):
        """
        on initialization - create a screen object, ship object, asteroid object list and
        empty torpedoes list. then genearte the first asteroids and then drawing the object on the
        screen
        :param asteroids_amount:
        """
        self.__screen = Screen()
        self.__lives = DEFAULT_LIVES
        # Initializing Parameters:
        # Screen coordinates:
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        # Screen dimensions:
        self.__screen_height = Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y
        self.__screen_width = Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X

        self.__asteroid_list = list()
        self.__torpedoes_list = list()

        # Initializing score:
        self.__score = 0

        # Initializing the ship and set it's location randomly:
        self.__ship = Ship(self._get_random_starting_location())

        # Initializing the asteroids according to the given Integer in function argument:
        self._generate_first_asteroids(asteroids_amount)

        # draw objects:
        # draw ship
        self.__screen.draw_ship(self.__ship.get_location().get_x(),
                                self.__ship.get_location().get_y(),
                                self.__ship.get_direction())

        # register and then draw the asteroids
        self._register_asteroids()
        self._draw_asteroids()

    def _generate_first_asteroids(self, asteroids_amount):
        """
        generates the asteroid list
        :param asteroids_amount: the amount of asteroids
        :return: None
        """
        for __num in range(asteroids_amount):
            # generate speed:
            __speed_x = self._get_random_speed_value()
            __speed_y = self._get_random_speed_value()
            __speed = Coordinate(__speed_x, __speed_y)

            # generate location:
            __rand_location = self._get_random_starting_location()
            # create an asteroid:
            __asteroid = Asteroid(__rand_location, __speed)

            # check if it is intersecting with the ship, if so - generate new location:
            while __asteroid.has_intersection(self.__ship):
                __rand_location = self._get_random_starting_location()
                __asteroid.set_location(__rand_location)

            self.__asteroid_list.append(__asteroid)

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _get_random_speed_value(self):
        """
        returns a random speed value between -4 to -1 or 1 to 4
        :return: the random number between -4 to -1 or 1 to 4
        """
        __r_num1 = random.randint(-4, -1)
        __r_num2 = random.randint(1, 4)
        __random_num = random.choice([__r_num1, __r_num2])
        return __random_num

    def _register_asteroids(self):
        """
        registers the asteroids to your system
        :return: None
        """
        for __asteroid in self.__asteroid_list:
            self.__screen.register_asteroid(__asteroid, __asteroid.get_size())

    def _register_torpedo(self):
        """
        registers a torpedo to your system
        :return: None
        """
        self.__screen.register_torpedo(self.__torpedoes_list[-1])

    def _draw_asteroids(self):
        """
        draw asteroids one by one to the screen
        :return: None
        """
        for __asteroid in self.__asteroid_list:
            self.__screen.draw_asteroid(__asteroid, __asteroid.get_location().get_x(),
                                        __asteroid.get_location().get_y())

    def _draw_torpedoes(self):
        """
        draw torpedoes one by one to the screen
        :return: None
        """
        for __torpedo in self.__torpedoes_list:
            self.__screen.draw_torpedo(__torpedo, __torpedo.get_location().get_x(),
                                       __torpedo.get_location().get_y(),
                                       __torpedo.get_direction())

    def _get_random_starting_location(self):
        """
        :return: a random coordinate object
        """
        return Coordinate(random.randint(self.__screen_min_x, self.__screen_max_x),
                          random.randint(self.__screen_min_y, self.__screen_max_y))

    def _do_loop(self):
        # You should not to change this method!

        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _accelerate_ship(self):
        """
        accelerates the ship object by changing it's speed vector
        :return: None
        """
        __speed_x = self.__ship.get_speed().get_x() + math.cos(
            math.radians(self.__ship.get_direction()))
        __speed_y = self.__ship.get_speed().get_y() + math.sin(
            math.radians(self.__ship.get_direction()))
        self.__ship.set_speed(Coordinate(__speed_x, __speed_y))

    def _shoot(self):
        """
        fires a torpedo
        :return: None
        """
        # can't shoot any more torpedoes
        if self.__ship.max_torpedo_reached():
            return

        # inform the ship that it fires a torpedo,
        self.__ship.fire()
        # append a new torpedo object and registers it
        __speed = Coordinate(self.__ship.get_speed().get_x() + 2 * math.cos(
            math.radians(self.__ship.get_direction())),
                             self.__ship.get_speed().get_y() + 2 * math.sin(
                                 math.radians(self.__ship.get_direction())))
        self.__torpedoes_list.append(
            Torpedo(self.__ship.get_location(), __speed, self.__ship.get_direction()))
        self._register_torpedo()

    def _move_asteroids(self):
        """
        moves the asteroids to their new location
        :return: None
        """
        for __asteroid in self.__asteroid_list:
            __asteroid.set_location(
                self._get_new_loc(__asteroid.get_location(), __asteroid.get_speed()))

    def _check_intersection(self, objects: list):
        """
        checks whether an object list (ship or torpedo) is intersecting asteroid or not
        :return: the index of the hit asteroid and the index of the hitting object
        :type return: tuple
        """
        for index, __asteroid in enumerate(self.__asteroid_list):
            if len(objects) != 0:
                for obj in objects:
                    if __asteroid.has_intersection(obj):
                        return index, objects.index(obj)
        return -1, -1

    def _split_asteroid(self, asteroid: Asteroid, torpedo: Torpedo, size):
        """
        splitting the asteroid upon hit
        :param asteroid: the asteroid that been hit
        :type asteroid: Asteroid
        :param torpedo: the torpedo that hit the asteroid
        :type torpedo: Torpedo
        :param size: the size of the asteroid
        :return: None
        """
        # get the old asteroid and torpedo out of the list
        self._dispose_obj(asteroid)
        self._dispose_obj(torpedo)

        if size > 1:  # the size could be 2 or 3 in this case
            # calculate speed vectors for the new asteroids
            __speed_x = (torpedo.get_speed().get_x() + asteroid.get_speed().get_x()) / \
                        (math.sqrt(asteroid.get_speed().get_x() ** 2 +
                                   asteroid.get_speed().get_y() ** 2))

            __speed_y = (torpedo.get_speed().get_y() + asteroid.get_speed().get_y()) / \
                        (math.sqrt(asteroid.get_speed().get_x() ** 2 +
                                   asteroid.get_speed().get_y() ** 2))

            __speed_vec_pos = Coordinate(__speed_x, __speed_y)
            __speed_vec_neg = Coordinate(-__speed_x, -__speed_y)

            # append and register the new asteroids
            self.__asteroid_list.append(
                Asteroid(asteroid.get_location(), __speed_vec_pos, size - 1))
            self.__screen.register_asteroid(self.__asteroid_list[-1], size - 1)
            self.__asteroid_list.append(
                Asteroid(asteroid.get_location(), __speed_vec_neg, size - 1))
            self.__screen.register_asteroid(self.__asteroid_list[-1], size - 1)

    def _dispose_obj(self, obj):
        """
        disposes an object form the game
        :param obj: the object to dispose, could be an asteroid or a torpedo
        :type obj: Asteroid or Torpedo
        :return: the disposed object
        """
        if type(obj) == Asteroid:
            index = self.__asteroid_list.index(obj)
            popped_asteroid = self.__asteroid_list.pop(index)
            self.__screen.unregister_asteroid(popped_asteroid)
            return popped_asteroid

        elif type(obj) == Torpedo:
            self.__ship.decrement_torpedoes_shots()
            index = self.__torpedoes_list.index(obj)
            popped_torpedo = self.__torpedoes_list.pop(index)
            self.__screen.unregister_torpedo(popped_torpedo)
            return popped_torpedo

    def _update_score(self, __asteroid_size):
        """
        updates the score depending on the size of the hit asteroid
        :param __asteroid_size: the size of the asteroid, could be 1, 2 or 3
        :return: None
        """
        if __asteroid_size == 3:
            self.__score += 20
        elif __asteroid_size == 2:
            self.__score += 50
        elif __asteroid_size == 1:
            self.__score += 100
        self.__screen.set_score(self.__score)

    def _get_new_loc(self, old_loc: Coordinate, cur_speed: Coordinate):
        """
        calculates the new location of the ship considering
        the speed of it and the previous location
        :param old_loc: the old location coordinate
        :type old_loc: Coordinate
        :param cur_speed: the current speed vector coordinate
        :type cur_speed: Coordinate
        :return: the new location coordinate
        :rtype: Coordinate
        """
        new_x = self.__screen_min_x + \
                (old_loc.get_x() + cur_speed.get_x() - self.__screen_min_x) % self.__screen_width
        new_y = self.__screen_min_y + \
                (old_loc.get_y() + cur_speed.get_y() - self.__screen_min_y) % self.__screen_height
        return Coordinate(new_x, new_y)

    def _show_intersection_message(self, __asteroid_hit_index):
        """
        shows a message upon collision between the ship and an asteroid
        :param __asteroid_hit_index: the asteroid index that been hit by the ship
        :return: None
        """
        if self.__lives > 0:  # still got lives left
            self.__screen.show_message("Asteroid Hitting",
                                       f"you've hit an asteroid, now you have {str(self.__lives)} "
                                       f"more left")
            self.__screen.remove_life()
            # unregister the hit asteroid
            self.__screen.unregister_asteroid(self.__asteroid_list.pop(__asteroid_hit_index))

        elif self.__lives == 0:  # last life
            self.__screen.show_message("Asteroid Hitting",
                                       f"you've hit an asteroid, this is your last chance!")
            self.__screen.remove_life()
            # unregister the hit asteroid
            self.__screen.unregister_asteroid(self.__asteroid_list.pop(__asteroid_hit_index))

        else:  # game over
            self.__screen.show_message("Asteroid Hitting", "You Lost!")
            self.__screen.end_game()
            sys.exit()

    def update_torpedoes_location(self):
        """
        updates the torpedo location
        :return: None
        """
        if len(self.__torpedoes_list) != 0:  # check if there's any torpedo on the screen
            for __torpedo in self.__torpedoes_list:

                if __torpedo.is_dead():
                    self._dispose_obj(__torpedo)

                else:
                    __torpedo.increment_turns_alive()
                    __torpedo.set_location(
                        self._get_new_loc(__torpedo.get_location(), __torpedo.get_speed()))

    def _update_ship_parameters(self):
        # check if user pressed left in order to rotate the ship 7 degrees:
        if self.__screen.is_left_pressed():
            self.__ship.set_direction(self.__ship.get_direction() + 7)
        if self.__screen.is_right_pressed():
            self.__ship.set_direction(self.__ship.get_direction() - 7)
        if self.__screen.is_up_pressed():
            self._accelerate_ship()
        self.__ship.set_location(self._get_new_loc(self.__ship.get_location(),
                                                   self.__ship.get_speed()))

    def _game_loop(self):
        """
        runs a single loop of the game
        :return:
        """

        # check exiting conditions
        if self.__screen.should_end():  # "q is pressed or "quit" button clicked
            self.__screen.show_message(self.QUIT_HEAD, self.QUIT_MSG)
            self.__screen.end_game()
            sys.exit()

        elif len(self.__asteroid_list) == 0:  # no asteroids left
            self.__screen.show_message(self.WIN_HEAD, self.WIN_MSG)
            self.__screen.end_game()
            sys.exit()

        # objects movement section
        self._update_ship_parameters()

        self._move_asteroids()

        if self.__screen.is_space_pressed():
            self._shoot()

        self.update_torpedoes_location()

        # intersection section
        __asteroid_hit_index = self._check_intersection([self.__ship])[0]
        if __asteroid_hit_index != -1:  # means that intersection did happened
            self.__lives -= 1  # decrement lives
            self._show_intersection_message(__asteroid_hit_index)

        __asteroid_hit_index, __hitting_torpedo_index = self._check_intersection(
            self.__torpedoes_list)
        if __asteroid_hit_index != -1:  # means that intersection did happened
            __asteroid_size = self.__asteroid_list[__asteroid_hit_index].get_size()
            self._update_score(__asteroid_size)
            self._split_asteroid(self.__asteroid_list[__asteroid_hit_index],
                                 self.__torpedoes_list[__hitting_torpedo_index], __asteroid_size)

        # screen drawing section
        self.__screen.draw_ship(self.__ship.get_location().get_x(),
                                self.__ship.get_location().get_y(),
                                self.__ship.get_direction())
        self._draw_asteroids()

        self._draw_torpedoes()


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
