from tkinter import *
from tkinter import messagebox

import blinker as blnkr  # message passing between MVC


class View:
    """
    This is the class that deals with the UI
    """
    MAIN_FRAME_COLOR = "#FF9046"
    BUTTON_FRAME_COLOR = '#7ab8f5'
    TEXT_FRAME_COLOR = "#9046FF"
    DEFAULT_TIME_LEFT = "3:00"  # default timer

    def __init__(self, parent):
        """
        inits the class instance with all the widgets and configure theirs layout
        :param parent: The main frame
        """
        self.__finished = True

        # these are the play/pause/resume configurations
        self.PLAY_CONFIG = {
            "text": "PLAY",
            "command": self.start_game
        }

        self.PAUSE_CONFIG = {
            "text": "PAUSE",
            "command": self.pause_game
        }

        self.RESUME_CONFIG = {
            "text": "RESUME",
            "command": self.resume_game
        }

        parent.title("Boggle")
        self.__container = parent  # set the main frame as a class variable

        self._setup()  # crates and configure the layout
        self.__current_widget = None
        self.__timer_job = None

    def _setup(self):
        """
        This creates and places the UI objects
        """
        self._create_widgets()
        self._setup_layout()
        # self._binding_events()

    def _create_widgets(self):
        """
        create all the widgets as class varibles
        :return:
        """
        # create frames
        self._create_frames()

        # create letter buttons
        self._create_letter_buttons()

        # create game flow buttons
        self._create_game_buttons()

        # create labels
        self._create_labels()

        self.words_scrollbar = Scrollbar(self.words_frame)
        self.words_text_box = Text(self.words_frame, state=DISABLED, width=10,
                                   height=17, yscrollcommand=self.words_scrollbar.set)  # this is the listbox
        self.words_scrollbar.config(command=self.words_text_box.yview)

    def _setup_layout(self):
        """
        places all widgets in their frames
        :return:
        """
        # layout frames
        self._frame_layout()

        self.title.grid(row=0, column=0)

        # layout buttons
        self._letter_buttons_layout()

        # layout game flow buttons
        self._game_buttons_layout()

        # layout labels
        self._labels_layout()

        # layout text box
        self.words_text_box.grid(row=0, column=0)
        self.words_scrollbar.grid(row=0, column=1, sticky=NS)

    def _create_frames(self):
        """
        creates the frame widgets
        :return:
        """
        self.__container.config(bg=View.MAIN_FRAME_COLOR)
        self.buttons_frame = Frame(self.__container, bg=View.BUTTON_FRAME_COLOR, relief=RIDGE, bd=5)
        self.text_frame = Frame(self.__container, padx=4, bg=View.TEXT_FRAME_COLOR,
                                relief=RIDGE, bd=3)
        self.game_flow_frame = Frame(self.__container, bg="green", pady=3)
        self.timer_frame = Frame(self.text_frame)
        self.score_frame = Frame(self.text_frame)
        self.words_frame = Frame(self.text_frame)

    def _frame_layout(self):
        """
        |           BOGGLE            |
        ------------------------------|
        |  buttons frame |  text frame|
        |-----------------------------|
        |        game flow frame      |
        :return:
        """
        self.buttons_frame.grid(row=1, column=0, padx=5)
        self.text_frame.grid(row=1, column=1, padx=10)
        self.game_flow_frame.grid(row=2, columnspan=2, column=0, sticky=N)

        self.timer_frame.grid(row=0, column=0, pady=10)
        self.score_frame.grid(row=1, column=0, pady=10)
        self.words_frame.grid(row=2, column=0, pady=10)

    def _create_labels(self):
        """
        creates all the label widgets
        """
        # create boggle title
        self.title = Label(self.__container, text="BOGGLE!")

        # timer label
        self.timer_lbl = Label(self.timer_frame, text="Time:")
        self.time_left_lbl = Label(self.timer_frame, anchor=W, text=self.DEFAULT_TIME_LEFT)
        # score label
        self.score_lbl = Label(self.score_frame, text="Score:")
        self.points_lbl = Label(self.score_frame, anchor=W, text="0")

    def _labels_layout(self):
        """
        configure labels places in their frame
        :return:
        """
        # layout timer labels
        self.timer_lbl.grid(row=0, column=0)
        self.time_left_lbl.grid(row=0, column=1)

        # layout score labels
        self.score_lbl.grid(row=0, column=0)
        self.points_lbl.grid(row=0, column=1)

    def _create_letter_buttons(self):
        """
        creates the letter buttons as a list of buttons
        """
        self.btn_lst = []
        for row in range(4):
            btn_row = []
            for column in range(4):
                btn_row.append(Button(self.buttons_frame, width=4, height=4, font=("Helvetica", 12)))
            self.btn_lst.append(btn_row)

    def _letter_buttons_layout(self):
        """
        configure buttons places in their frame
        :return:
        """
        for row_btn_index in range(len(self.btn_lst)):
            for col_btn_index in range(len(self.btn_lst[0])):
                self.btn_lst[row_btn_index][col_btn_index].grid(row=row_btn_index,
                                                                column=col_btn_index,
                                                                padx=10,
                                                                pady=10)

    def set_letters(self, board):
        """
        populate the button texts according to the board
        :param board: the board
        :return:
        """
        for row in range(len(board)):
            for column in range(len(board[0])):
                self.btn_lst[row][column].config(text=board[row][column])

    def btn_released(self, event):
        """
        this happens upon release of left mouse button
        :param event: the event. event.widget is the button that caused the event
        """
        for btn_row in self.btn_lst:
            for btn in btn_row:
                btn.config(relief=RAISED)  # raise all the buttons
        blnkr.signal("btn_released").send()  # notify controller that the button released
        ## addedd this line  I fixed the problem 
        self.__current_widget = None


    def add_letter(self, event):
        """
        this function is invoked upon the movement of the mouse while the left mouse button is pressed
        if the widget under the mouse is not the same as the last one, invoke <<B1-Enter>> event manually
        :param event: the event, event.widget is the mouse coordinates
        :return:
        """
        widget = event.widget.winfo_containing(event.x_root,
                                               event.y_root)  # gets the widget under the mouse
        if self.__current_widget != widget:
            self.__current_widget = widget
            if widget:
                self.__current_widget.event_generate("<<B1-Enter>>")

    def on_enter(self, event):
        """
        this function is invoked upon entering a button while the left mouse button is pressed
        :param event: the event.widget is the button that is currently underneath the mouse
        :return:
        """
        blnkr.signal("mouse_over_btn").send(
            event.widget)  # notify controller that the mouse is over a button

    def sunk_btn(self, btn: Button):
        """
        make the given button to look like it's pressed
        :param btn: the button
        :return:
        """
        btn["relief"] = SUNKEN

    def _on_click(self, event):
        event.widget['relief'] = SUNKEN
        return 'break'

    def _bind_letter_btns_events(self):
        """
        binds all the buttons to the game events
        :return:
        """
        for btn_row in self.btn_lst:
            for btn in btn_row:
                # this bind prevents the button to raise after click
                btn.bind('<Button-1>', self._on_click)
                btn.bind("<B1-Motion>", self.add_letter)
                btn.bind("<<B1-Enter>>", self.on_enter)
                btn.bind("<ButtonRelease-1>", self.btn_released)

    def _unbind_letter_btns_events(self):
        """
        unbinds all the buttons from the game events
        :return:
        """
        for btn_row in self.btn_lst:
            for btn in btn_row:
                btn.bind('<Button-1>')
                btn.unbind("<B1-Motion>")
                btn.unbind("<<B1-Enter>>")
                btn.unbind("<<B1-Leave>>")
                btn.unbind("<ButtonRelease-1>")

    def add_word(self, word):
        """
        add to the text box the given word
        :param word: the word
        :return:
        """
        self.words_text_box["state"] = NORMAL
        self.words_text_box.insert(END, word + "\n")
        self.words_text_box.yview_moveto(1)
        self.words_text_box["state"] = DISABLED

    def update_score(self, score):
        """
        updates the score label to the given score
        :param score: the score
        :return:
        """
        self.points_lbl["text"] = score

    def _create_game_buttons(self):
        """
        creates the game flow buttons
        """
        self.play_pause_btn = Button(self.game_flow_frame, **self.PLAY_CONFIG)
        self.exit_btn = Button(self.game_flow_frame, text="EXIT",
                               command=sys.exit)

    def _game_buttons_layout(self):
        """
        configure game flow buttons
        :return:
        """
        self.play_pause_btn.grid(row=0, column=0, padx=5)
        self.exit_btn.grid(row=0, column=1, padx=5)

    def start_game(self):
        """
        this function is invoked upon clicking on the start button
        :return:
        """
        blnkr.signal("UI_ready_to_load").send()  # blink the controller to get a new board
        self._bind_letter_btns_events()  # bind all the buttons to theirs event handlers
        self.__container.after(1000, self._run_timer)  # start the timer
        self.play_pause_btn.config(
            **self.PAUSE_CONFIG)  # switch the play/pause button to pause configuration
        self.__finished = False

    def pause_game(self):
        """
        this function is invoked upon clicking on the pause button
        :return:
        """
        self.__container.after_cancel(self.__timer_job)  # pause the timer
        self._unbind_letter_btns_events()  # unbind all the letters from their event
        self._hide_letters()  # hide all the letters
        self.play_pause_btn.config(
            **self.RESUME_CONFIG)  # switch the play/pause button to resume configuration

    def resume_game(self):
        """
        this function is invoked upon clicking on the resume button
        :return:
        """
        if not self.__finished:
            self._bind_letter_btns_events()  # re-binding the buttons
            self._run_timer()  # run update timer
            blnkr.signal("UI_ready_to_load").send()  # blink the controller to get the letters
            self.play_pause_btn.config(
                **self.PAUSE_CONFIG)  # switch the play/pause button to resume configuration

    def _hide_letters(self):
        """
        conceal the letters from the buttons
        """
        for btn_row in self.btn_lst:
            for btn in btn_row:
                btn["text"] = " "

    def _run_timer(self):
        """
        runs the timer
        :return:
        """
        blnkr.signal("1_second_passed").send()
        if not self.__finished:
            self.__timer_job = self.__container.after(1000, self._run_timer)

    def display_time(self, time):
        """
        updates the timer label
        :param time: the new label string
        :return:
        """
        self.time_left_lbl["text"] = time

    def game_over(self):
        """
        this function is invoked when the timer is done.
        :return:
        """
        self.__finished = True
        self._unbind_letter_btns_events()  # unbind the buttons
        self.play_pause_btn["command"] = lambda *x: "break"  # disable the play/pause functionality
        if messagebox.askyesno("GAME OVER",
                               "Do you want to play again?"):  # raise a message box to play again
            blnkr.signal("new_game").send()
        else:
            sys.exit()


"""
# for testing puposes
if __name__ == '__main__':
    mainwin = tk.Tk()
    WIDTH = 800
    HEIGHT = 600
    mainwin.geometry("%sx%s" % (WIDTH, HEIGHT))
    # mainwin.resizable(0, 0)
    mainwin.title("Boggle")

    view = View(mainwin)
    mainwin.mainloop()
"""
