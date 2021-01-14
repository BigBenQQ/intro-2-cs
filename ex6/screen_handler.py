EXIT_MAIN = "3 for exit program"
COMPOSE_MENU = "2 for compose"
EDIT_MENU = "1 for edit"


def display_logo():
    """
    This displays out cool logo! :)
    :return: None
    """
    print(" _       __                    ______    ___ __            ")
    print("| |     / /___ __   _____     / ____/___/ (_) /_____  _____")
    print("| | /| / / __ `/ | / / _ \   / __/ / __  / / __/ __ \/ ___/")
    print("| |/ |/ / /_/ /| |/ /  __/  / /___/ /_/ / / /_/ /_/ / /    ")
    print("|__/|__/\__,_/ |___/\___/  /_____/\__,_/_/\__/\____/_/     ")


def display_main_menu():
    """
    This function prints the main menu on the screen.
    :return: None
    """
    print(EDIT_MENU)
    print(COMPOSE_MENU)
    print(EXIT_MAIN)


def display_edit_menu():
    """
    This function prints the edit menu on the screen.
    :return: None
    """
    print("Enter 1 to reverse the wav file")
    print("Enter 2 to speed up the wav file")
    print("Enter 3 to slow down the wav file")
    print("Enter 4 to make the volume of the wav file higher")
    print("Enter 5 to make the volume of the wav file lower")
    print("Enter 6 to apply low pass filter to the wav file")
    print("Enter 7 to save the file")


def display_save_message(src_filename):
    print("You are going to save your edited audio file.")
    print(f"The source file of your work is: {src_filename}")
