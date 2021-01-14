import os

EMPTY_NAME_ERROR_MSG = "You need to enter an output filename."

ENTER_A_WAV_FILE = "Please enter a .wav file: "
ENTER_A_COMPOSITION_FILE = "Please enter a composition file: "
ENTER_AN_OUTPUT_FILE = "Please name your output file: "

FILE_NOT_EXISTS = "The file does not exist."

NOT_VALID_INPUT_ERROR_MESSAGE = "You can only choose 1, 2 or 3."
DO_YOU_WANT_TO_DO = "What do you want to do? "

ALL_POSSIBLE_INPUTS_MAIN = [num for num in "123"]
ALL_POSSIBLE_INPUTS_EDIT = [num for num in "1234567"]


def get_main_menu_answer():
    """
    This function gets the user input to the main menu
    :return: The user input
    """
    answer = input(DO_YOU_WANT_TO_DO)
    while answer not in ALL_POSSIBLE_INPUTS_MAIN:
        print(NOT_VALID_INPUT_ERROR_MESSAGE)
        answer = input(DO_YOU_WANT_TO_DO)
    return answer


def get_edit_menu_answer():
    """
    This function gets the user input to the edit menu
    :return: The user input
    """
    answer = input(DO_YOU_WANT_TO_DO)
    while answer not in ALL_POSSIBLE_INPUTS_EDIT:
        print("You can only choose 1 to 7")
        answer = input(DO_YOU_WANT_TO_DO)
    return answer


def get_wav_filename():
    """
    This function gets the wave file from the user.
    :return:
    """
    wav_filename = input(ENTER_A_WAV_FILE)
    # wav_filename = ensure_wav_suffix(wav_filename)
    while True:
        if os.path.isfile(wav_filename):
            break
        else:
            print(FILE_NOT_EXISTS)
            wav_filename = input(ENTER_A_WAV_FILE)
    return wav_filename


def get_composition_filename():
    """
    This function gets the composition file from the user.
    :return:
    """
    composition_filename = input(ENTER_A_COMPOSITION_FILE)
    while not os.path.isfile(composition_filename):
        print(FILE_NOT_EXISTS)
        composition_filename = input(ENTER_A_COMPOSITION_FILE)
    return composition_filename


def get_wav_output_filename():
    """
    This function gets the name of the output file as wav file
    :return: The output filename
    """
    output_filename = input(ENTER_AN_OUTPUT_FILE)
    while output_filename == "":
        print(EMPTY_NAME_ERROR_MSG)
        output_filename = input(ENTER_AN_OUTPUT_FILE)
    return output_filename

# def ensure_wav_suffix(output_filename):
#     """
#     This function make sure that the output file ends with wav suffix
#     :param output_filename: The filename
#     :return: filename.wav
#     """
#     if not output_filename.endswith(".wav"):
#         output_filename = output_filename + ".wav"
#     return output_filename
