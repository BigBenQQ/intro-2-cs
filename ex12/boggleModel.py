from tkinter import *
from boggle_board_randomizer import randomize_board
import blinker as blnkr
import sched


class Model:
    """
    this class deals with the logic of the game and sends things to the
    controller
    """
    MINUTES_OF_GAME = 3
    SECONDS_OF_GAME = 0

    def __init__(self):
        """
        creates the object of the game
        """
        self.__board = randomize_board()
        self.__button_pressed = set()
        self.__location_in_grid = []
        self.__word = ""
        self.__word_list = set()
        self.__score = 0

        self.__seconds = Model.SECONDS_OF_GAME
        self.__minutes = Model.MINUTES_OF_GAME

        with open("boggle_dict.txt") as file:
            self.__boggle_valid_words = file.readlines()
            self.__boggle_valid_words = \
                [x.strip() for x in self.__boggle_valid_words]
            self.__boggle_valid_words = set(self.__boggle_valid_words)

    def load_board(self):
        """
        signals that the board is ready and sends the board to the controller
        :return:
        """
        blnkr.signal("board_ready").send(board=self.__board)

    def add_letter(self, btn: Button):
        """
        adds the letter pressed to the current word if it is in a valid place
        and if so sends a message to the controller
        :param btn: a button that the user pressed down with the mouse
        :return:
        """
        if id(btn) in self.__button_pressed:
            return
        self.__button_pressed.add(id(btn))

        if len(self.__location_in_grid) == 0:
            # insert first letter without conditions
            self.__location_in_grid.append(btn.grid_info())
            self.__word += btn["text"]
            blnkr.signal("sunk_btn").send(btn=btn)

        elif abs(self.__location_in_grid[-1]["row"]
                 - btn.grid_info()["row"]) <= 1\
                and abs(self.__location_in_grid[-1]["column"]
                        - btn.grid_info()["column"]) <= 1:
            self.__location_in_grid.append(btn.grid_info())
            self.__word += btn["text"]
            blnkr.signal("sunk_btn").send(btn=btn)

    def add_word(self):
        """
        adds the word to the list if it is in the dictionary and wasn't picked
        already
        and sends the word and the updated score to the controller
        :return:
        """
        self.__word = self.__word.upper()
        if self.__word in self.__boggle_valid_words:
            if self.__word not in self.__word_list:
                self.__word_list.add(self.__word)
                self._add_score(self.__word)
                # send message to controller to update the view
                blnkr.signal("word_added").send(word=self.__word)
                blnkr.signal("update_score").send(score=self.__score)

        self.__button_pressed = set()  # reset fields
        self.__location_in_grid = []
        self.__word = ""

    def _add_score(self, word):
        """
        adds the score of the current word to the total score
        :param word: a word that was found by the user
        :return:
        """
        self.__score += len(word) ** 2

    def update_timer(self):
        """
        updates the time that is left and sends it to the controller
        if the time is over sends a message to the controller to end the game
        :return:
        """
        if self.__seconds == 0:
            self.__seconds = 59
            self.__minutes -= 1
            if self.__minutes < 0:
                blnkr.signal("game_over").send()
                return
        else:
            self.__seconds -= 1
        blnkr.signal("time_updated").send(
            time=f"{self.__minutes}:{'{0:0=2d}'.format(self.__seconds)}")
