# FILE: wave_editor.py
# WRITERS: Ben Mendel, ben.mendel AND
#          Sarah Wolicki, sarahwolicki
# EXERCISE: intro2sc1 ex6 2019-2020
# DESCRIPTION: This is an audio file editor. Can handle wav files
# and manipulate them in several different ways.
# Also, this program can compose an audio file out of a composition text file

import math
import wave_helper as wave_helper
import screen_handler as screen_handler
import input_handler as input_handler

EDIT = "1"
COMPOSE = "2"
EXIT_INPUT_MAIN = "3"

REVERSE = "1"
SPEED_UP = "2"
SLOW_DOWN = "3"
VOL_UP = "4"
VOL_DOWN = "5"
LPF = "6"
SAVE_FILE = "7"

DEFAULT_SAMPLE_RATE = 2000
DEFAULT_CHANGE_VOL_MULTIPLIER = 1.2
MAX_VOLUME = 32767
MIN_VOLUME = -32768
NOTES = {"A": 440,
         "B": 494,
         "C": 523,
         "D": 587,
         "E": 659,
         "F": 698,
         "G": 784,
         "Q": 0
         }


def _average(*args):
    """
    This function does an arithmetical average for n args.
    :param args: All the addends
    :return: The arithmetical average
    """
    return int(sum(args) / len(args))


def run_edit_mode(audio_data, filename, frame_rate):
    """
    This function runs the selected function and applies it to the audio data
    :param audio_data: The audio data
    :param filename: The name of the saved edited wav file
    :param frame_rate: The frame rate
    :return: None
    """
    while True:
        screen_handler.display_edit_menu()
        edit_answer = input_handler.get_edit_menu_answer()

        if edit_answer == REVERSE:
            audio_data = reverse_file(audio_data)
        elif edit_answer == SPEED_UP:
            audio_data = speed_up_file(audio_data)
        elif edit_answer == SLOW_DOWN:
            audio_data = slow_down_file(audio_data)
        elif edit_answer == VOL_UP:
            vol_up_file(audio_data)
        elif edit_answer == VOL_DOWN:
            vol_down_file(audio_data)
        elif edit_answer == LPF:
            audio_data = low_pass_filter_file(audio_data)
        elif edit_answer == SAVE_FILE:
            save_file(frame_rate, audio_data, filename)
            break


def parse_composition_to_audio_data(composition_filename):
    """
    This function Parses the composition text to audio data
    :return: A list of tuples each containing a note and it's duration
    """
    with open(composition_filename, "r") as file:
        data = file.read()

    # Makes a list of notes and durations, discarding whitespaces and newlines
    data_lst = data.split()

    sample_lst = []
    # Loop though only the notes. so data_lst[i] = note, data_lst[i+1] = duration
    for i in range(0, len(data_lst) - 1, 2):
        j = 0
        note, duration = data_lst[i], int(data_lst[i+1])
        # Every duration unit is 125 samples
        while j < duration * 125:
            if NOTES[note] == 0:
                sample_lst.append([0, 0])
            else:
                samples_per_cycle = DEFAULT_SAMPLE_RATE / NOTES[note]
                sample = int(MAX_VOLUME * math.sin(math.pi * 2 * (j / samples_per_cycle)))
                sample_lst.append([sample, sample])
            j += 1

    return sample_lst


def reverse_file(audio_data):
    """
    This function reverses the audio data entered.
    :param audio_data: The audio data
    :return: The audio data after being reversed
    """
    audio_data = list(reversed(audio_data))
    print("The audio has been reversed.")

    return audio_data


def speed_up_file(audio_data):
    """
    This function speeds up the audio data.
    :param audio_data: The input audio data
    :return: The audio data sped up
    """
    new_audio_data = []

    for i in range(len(audio_data)):
        if (i % 2) == 0:
            new_audio_data.append(audio_data[i])

    print("The audio has been sped up.")
    return new_audio_data


def slow_down_file(audio_data):
    """
    This function slows down the audio data.
    :param audio_data: The input audio data
    :return: The audio data slowed down
    """
    new_audio_data = []

    for i in range(len(audio_data) - 1):
        new_audio_data.append(audio_data[i])
        new_audio_data.append([int((audio_data[i][0] + audio_data[i + 1][0]) / 2),
                               int(audio_data[i][1] + audio_data[i + 1][1] / 2)])
    new_audio_data.append(audio_data[-1])

    print("The audio has been slowed down.")
    return new_audio_data


def vol_up_file(audio_data: list):
    """
    This function increases the volume of the audio data
    :param audio_data: Input audio data
    :return: The audio data with increased volume
    """
    for bit in audio_data:

        bit[0] *= DEFAULT_CHANGE_VOL_MULTIPLIER
        bit[1] *= DEFAULT_CHANGE_VOL_MULTIPLIER

        bit[0] = int(bit[0])
        bit[1] = int(bit[1])

        if bit[0] > MAX_VOLUME:
            bit[0] = MAX_VOLUME
        if bit[1] > MAX_VOLUME:
            bit[1] = MAX_VOLUME

    print("Volume is higher")


def vol_down_file(audio_data: list):
    """
    This function decrease the volume of the audio data
    :param audio_data: Input audio data
    :return: The audio data with decreased volume
    """
    for bit in audio_data:

        bit[0] /= DEFAULT_CHANGE_VOL_MULTIPLIER
        bit[1] /= DEFAULT_CHANGE_VOL_MULTIPLIER

        bit[0] = int(bit[0])
        bit[1] = int(bit[1])

        if bit[0] < MIN_VOLUME:
            bit[0] = MIN_VOLUME
        if bit[1] < MIN_VOLUME:
            bit[1] = MIN_VOLUME

    print("Volume is lower")


def low_pass_filter_file(audio_data: list):
    """
    This function applies low pass filter to the audio data.
    :param audio_data: Input audio data
    :return: The dimmed audio data
    """
    new_audio_data = list()
    new_audio_data.append([_average(audio_data[0][0], audio_data[1][0]),
                           _average(audio_data[0][1], audio_data[1][1])])

    for i in range(1, len(audio_data) - 1):
        new_audio_data.append(
            [_average(audio_data[i - 1][0], audio_data[i][0], audio_data[i + 1][0]),
             _average(audio_data[i - 1][1], audio_data[i][1], audio_data[i + 1][1])])

    last_index_of_audio_file = len(audio_data) - 1
    new_audio_data.append(
        [_average(audio_data[last_index_of_audio_file][0],
                  audio_data[last_index_of_audio_file - 1][0]),
         _average(audio_data[last_index_of_audio_file][1],
                  audio_data[last_index_of_audio_file - 1][1])])

    print("The volume dimmed")

    return new_audio_data


def save_file(frame_rate, audio_data, src_filename):
    """
    This function uses wave_helper to save the wav file
    :param frame_rate: The frame rate of the output file
    :param audio_data: The audio data to save
    :param src_filename: The name of the wav file
    :return: None
    """
    screen_handler.display_save_message(src_filename)
    wave_filename = input_handler.get_wav_output_filename()

    wave_helper.save_wave(frame_rate, audio_data, wave_filename)


def main():
    """
    The main function
    :return: None
    """
    is_composition_mode = False
    out_filename = ""
    answer = EDIT

    screen_handler.display_logo()

    while True:
        if not is_composition_mode:
            screen_handler.display_main_menu()
            answer = input_handler.get_main_menu_answer()

        if answer == EDIT:
            if is_composition_mode:
                frame_rate, audio_data = wave_helper.load_wave(out_filename)
                run_edit_mode(audio_data, out_filename, frame_rate)

            else:
                wav_filename = input_handler.get_wav_filename()
                frame_rate, audio_data = wave_helper.load_wave(wav_filename)
                run_edit_mode(audio_data, wav_filename, frame_rate)

            is_composition_mode = False

        elif answer == COMPOSE:
            is_composition_mode = True

            composition_filename = input_handler.get_composition_filename()
            sample_lst = parse_composition_to_audio_data(composition_filename)
            out_filename = input_handler.get_wav_output_filename()
            wave_helper.save_wave(DEFAULT_SAMPLE_RATE, sample_lst, out_filename)
            answer = EDIT

        elif answer == EXIT_INPUT_MAIN:
            return


if __name__ == '__main__':
    main()
