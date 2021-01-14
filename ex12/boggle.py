##############################################################################
# FILE : boggle.py
# WRITERS :
# Ben Mendel, ben.mendel
# Avraham Zvi Schochet, azvischo
# EXERCISE : intro2cs1 ex12 2019-2020
# DESCRIPTION: the boggle game
#
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PA
#
#
# GES I USED:
# NOTES:
#
#
#
##############################################################################

from boggleView import View
from boggleModel import Model
from tkinter import *
import blinker as blnkr


class Controller:
    """
    The controller part in the MVC design pattern.
    This class connects the UI with the logic parts
    """
    def __init__(self, parent):
        """
        starts the object that controls the game
        :param parent: the main window
        """
        self.__parent = parent
        self.__model = Model()
        self.__view = View(parent)

        # View => Model
        blnkr.signal("mouse_over_btn").connect(self._add_letter)
        blnkr.signal("btn_released").connect(self._btn_released)
        blnkr.signal("UI_ready_to_load").connect(self._get_board)
        blnkr.signal("1_second_passed").connect(self._update_time)
        blnkr.signal("new_game").connect(self._reset_model)

        # Model => View
        blnkr.signal("board_ready").connect(self._set_board)
        blnkr.signal("word_added").connect(self._new_word)
        blnkr.signal("update_score").connect(self._update_score)
        blnkr.signal("sunk_btn").connect(self._sunk_btn)
        blnkr.signal("time_updated").connect(self._time_updated)
        blnkr.signal("game_over").connect(self._game_over)

    def _add_letter(self, btn: Button):
        """
        sends the model the button that was pressed
        :param btn: a button on the board
        :return:
        """
        self.__model.add_letter(btn)

    def _btn_released(self, sender):
        """
        sends the model a message telling that the mouse was unpressed
        :param sender:
        :return:
        """
        self.__model.add_word()

    def _set_board(self, sender, board):
        """
        sends view the board that was randomized in the model
        :param sender:
        :param board: the board of the game
        :return:
        """
        self.__view.set_letters(board)

    def _get_board(self, sender):
        """
        sends the model a message to randomize the board
        :param sender:
        :return:
        """
        self.__model.load_board()

    def _new_word(self, sender, word):
        """
        sends view a word to add to the word list
        :param sender:
        :param word: a word that was found
        :return:
        """
        self.__view.add_word(word)

    def _update_score(self, sender, score):
        """
        sends view the updated score
        :param sender:
        :param score:
        :return:
        """
        self.__view.update_score(score)

    def _sunk_btn(self, event, btn: Button):
        """
        sends view a button that was presses telling that it is valid
        :param event:
        :param btn: a button
        :return:
        """
        self.__view.sunk_btn(btn)

    def _update_time(self, sender):
        """
        tells the model that a second passed
        :param sender:
        :return:
        """
        self.__model.update_timer()

    def _time_updated(self, event, time: str):
        """
        sends view the current time remaining, to display
        :param event:
        :param time: a string with the current time remaining
        :return:
        """
        self.__view.display_time(time)

    def _game_over(self, event):
        """
        tells view that the game is over
        :param event:
        :return:
        """
        self.__view.game_over()

    def _reset_model(self, sender):
        """
        resets the game so it can be played again
        :param sender:
        :return:
        """
        self.__model = Model()
        self.__view = View(self.__parent)


# entry point of the program


if __name__ == "__main__":
    # Create an instance of Tk. equivalent to what commonly used as "root"
    mainwin = Tk()
    WIDTH = 500
    HEIGHT = 500
    mainwin.geometry(f"{WIDTH}x{HEIGHT}")
    mainwin.resizable(False, False)
    mainwin.columnconfigure(0, weight=1)

    game_app = Controller(mainwin)

    mainwin.mainloop()
