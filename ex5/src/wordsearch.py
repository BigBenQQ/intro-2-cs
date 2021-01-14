#####################################################
# FILE: wordsearch.py
# WRITER: Ben Mendel, ben.mendel, 312437130
# EXERCISE: intro2sc1 ex5 2019-2020
# DESCRIPTION:
#####################################################
import os.path
import sys

WRONG_DIRECTIONS_INPUT = "Wrong directions input. you may only enter a combination of:"

WORD_FILE_CONTAINS_WHITESPACE = "You have a whitespace in your word file"
LAST_CHARACTER_IS_NOT_NEWLINE_MSG = "The last character is not \\n"
DOES_NOT_EXIST_MSG = "File {} does not exist"
NEWLINE = "\n"
WHITESPACE = " "
UP = "u"
DOWN = "d"
LEFT = "l"
RIGHT = "r"
UP_RIGHT = "w"
UP_LEFT = "x"
DOWN_RIGHT = "y"
DOWN_LEFT = "z"
ALL_DIRECTIONS = UP + DOWN + LEFT + RIGHT + UP_RIGHT + UP_LEFT + DOWN_RIGHT + DOWN_LEFT


def _valid_file_format(filename):
    """
    Check that the file given doesn't have whitespaces and every line ends
    with a newline
    :param filename: The path of the file to be checked
    :return: If file is valid - return True. Otherwise - Error message
    """
    if not os.path.isfile(filename):
        return DOES_NOT_EXIST_MSG.format(filename)

    with open(filename, "r") as file:
        words = file.read()
        if words[-1] != NEWLINE:
            return LAST_CHARACTER_IS_NOT_NEWLINE_MSG
        elif WHITESPACE in words:
            return WORD_FILE_CONTAINS_WHITESPACE
    return True


def _valid_len_of_args(len_of_args):
    """
    Checks that the user entered exactly 4 arguments
    :param len_of_args: The amount of args that the user entered
    :return: True if number of arguments is exactly 4. otherwise - error message
    """
    if len_of_args != 5:
        return f"You have entered {len_of_args - 1} arguments instead of 4"
    else:
        return True


def _valid_directions(direction_str):
    """
    Checks if all of the directions symbols entered are valid
    :param direction_str: The direction string argument
    :return: True if directions are valid. otherwise - Error message
    """
    if all((c in ALL_DIRECTIONS) for c in direction_str):
        return True
    return f"{WRONG_DIRECTIONS_INPUT} {ALL_DIRECTIONS}"


def _find_r(matrix, word, word_occurrences_dict):
    """
    Find word when searching to the right.
    Updates the dictionary.
    :param matrix: The matrix to search upon
    :param word: the word to search
    :param word_occurrences_dict: The dictionary of the found words
    :return: None
    """
    # run through the matrix
    for i in range(len(matrix)):
        j = 0
        while j < len(matrix[i]) - len(word) + 1:
            index_of_occurrence = "".join(matrix[i]).find(word, j)
            # the word is in the matrix row at least once
            if index_of_occurrence != -1:
                _add_occurrence(word, word_occurrences_dict)
                # move iterator to the character right after the start index of the found word
                j += index_of_occurrence + 1
            else:
                break


def _find_l(matrix, word, word_occurrences_dict):
    """
    Find word when searching to the left.
    Updates the dictionary.
    :param matrix: The matrix to search upon
    :param word: the word to search
    :param word_occurrences_dict: The dictionary of the found words
    :return: None
    """
    # run through the matrix
    for i in range(len(matrix)):
        j = 0
        while j < len(matrix[i]) - len(word) + 1:
            index_of_occurrence = "".join(matrix[i])[::-1].find(word, j)
            # the word is in the matrix row at least once
            if index_of_occurrence != -1:
                _add_occurrence(word, word_occurrences_dict)
                # move iterator to the character right after the start index of the found word
                j += index_of_occurrence + 1
            else:
                break


def _find_d(matrix, word, word_occurrences_dict):
    """
    Find word when searching downwards.
    Updates the dictionary.
    :param matrix: The matrix to search upon
    :param word: the word to search
    :param word_occurrences_dict: The dictionary of the found words
    :return: None
    """
    # run through the matrix
    for j in range(len(matrix[0])):
        i = 0
        while i < len(matrix) - len(word) + 1:
            index_of_occurrence = "".join([row[j] for row in matrix]).find(word, i)
            # the word is in the matrix row at least once
            if index_of_occurrence != -1:
                _add_occurrence(word, word_occurrences_dict)
                # move iterator to the character right after the start index of the found word
                i += index_of_occurrence + 1
            else:
                break


def _find_u(matrix, word, word_occurrences_dict):
    """
    Find word when searching upwards.
    Updates the dictionary.
    :param matrix: The matrix to search upon
    :param word: the word to search
    :param word_occurrences_dict: The dictionary of the found words
    :return: None
    """
    # run through the matrix
    for j in range(len(matrix[0])):
        i = 0
        while i < len(matrix) - len(word) + 1:
            index_of_occurrence = "".join([row[j] for row in matrix])[::-1].find(word, i)
            # the word is in the matrix row at least once
            if index_of_occurrence != -1:
                _add_occurrence(word, word_occurrences_dict)
                # move iterator to the character right after the start index of the found word
                i += index_of_occurrence + 1
            else:
                break


def _find_down_right(matrix, word, word_occurrences_dict):
    """
    Find word when searching diagonally downwards and to the right.
    Updates the dictionary.
    :param matrix: The matrix to search upon
    :param word: the word to search
    :param word_occurrences_dict: The dictionary of the found words
    :return: None
    """
    # run through the matrix
    diagonals = _get_down_right_diagonal_from_mat(matrix)
    _find_r(diagonals, word, word_occurrences_dict)


def _find_up_right(matrix, word, word_occurrences_dict):
    """
    Find word when searching diagonally upwards and to the right.
    Updates the dictionary.
    :param matrix: The matrix to search upon
    :param word: the word to search
    :param word_occurrences_dict: The dictionary of the found words
    :return: None
    """
    # run through the matrix
    diagonals = _get_up_right_diagonal_from_mat(matrix)
    _find_r(diagonals, word, word_occurrences_dict)


def _find_up_left(matrix, word, word_occurrences_dict):
    """
    Find word when searching diagonally upwards and to the left.
    Updates the dictionary.
    :param matrix: The matrix to search upon
    :param word: the word to search
    :param word_occurrences_dict: The dictionary of the found words
    :return: None
    """
    # run through the matrix
    diagonals = _get_down_right_diagonal_from_mat(matrix)
    _find_l(diagonals, word, word_occurrences_dict)


def _find_down_left(matrix, word, word_occurrences_dict):
    """
    Find word when searching diagonally downwards and to the left.
    Updates the dictionary.
    :param matrix: The matrix to search upon
    :param word: the word to search
    :param word_occurrences_dict: The dictionary of the found words
    :return: None
    """
    # run through the matrix
    diagonals = _get_up_right_diagonal_from_mat(matrix)
    _find_l(diagonals, word, word_occurrences_dict)


def _get_down_right_diagonal_from_mat(matrix):
    """
    Get all the diagonals (downwards and to the right) values from a given matrix
    :param matrix: The matrix
    :return: A list of the diagonals
    :rtype: list([str])
    """
    i = len(matrix)
    j = len(matrix[0])
    # gets all the right-down diagonal from the matrix
    # where q is the index along the diagonal
    # and p is the index of the diagonal (there are i+j+1 diagonals)
    return [[matrix[i - p + q - 1][q]
             for q in range(max(p - i + 1, 0), min(p + 1, j))]
            for p in range(i + j - 1)]


def _get_up_right_diagonal_from_mat(matrix):
    """
    Get all the diagonals (upwards and to the right) values from a given matrix
    :param matrix: The matrix
    :return: A list of the diagonals
    :rtype: list([str])
    """
    i = len(matrix)
    j = len(matrix[0])
    # gets all the right-up diagonal from the matrix
    # where q is the index along the diagonal
    # and p is the index of the diagonal (there are i+j+1 diagonals)
    return [[matrix[p - q][q]
             for q in range(max(p - i + 1, 0), min(p + 1, j))]
            for p in range(i + j - 1)]


def _add_occurrence(key, dictionary_to_update):
    """
    If the key isn't in the dictionary - adds in with a starting value of 1
    otherwise - increment the value of the given key
    :param key: The given key
    :param dictionary_to_update: The dictionary that is updated
    :return: None
    """
    if key not in dictionary_to_update:
        dictionary_to_update[key] = 1
    else:
        dictionary_to_update[key] += 1


def check_input_args(args):
    """
    check the validity of the arguments entered
    :param args: arg[0]: The script name (not input arg)
                 arg[1]: The word list filename
                 arg[2]: The matrix filename
                 arg[3]: The output filename (not input arg)
                 arg[4]: The directions string
    :return: Error message if one of the arguments aren't valid. otherwise - None
    """
    # Check that the user entered exactly 4 arguments
    is_valid_len_of_args = _valid_len_of_args(len(args))
    if type(is_valid_len_of_args) == str:
        return is_valid_len_of_args

    # check validity of both word list and matrix files
    for i in range(1, 3):
        if type(_valid_file_format(args[i])) == str:
            return _valid_file_format(args[i])

    # check validity of directions argument
    is_valid_directions = _valid_directions(args[4])
    if type(is_valid_directions) == str:
        return is_valid_directions


def read_wordlist_file(filename):
    """
    Gets the word list text
    :param filename: The path of the word list
    :return: A list of the words
    :rtype: list(str)

    """
    with open(filename, 'r') as file:
        return file.read().split("\n")[:-1]


def read_matrix_file(filename):
    """
    Gets the matrix text file
    :param filename: The path of the matrix
    :return: A list of list of the characters within the matrix, where every list
    of list represent a row in the matrix, and every index in the list of list represent column
    format - [['r','o','w','1'], ['r','o','w','2']...['r','o','w','n']]
    :rtype: list([str])

    """
    with open(filename, 'r') as file:
        # words_lst is the list of words from the matrix without commas
        # looks like - ['apple', 'agodo']
        words_lst = file.read().replace(",", "").split("\n")[:-1]

        # enter each word into a list
        # looks like [['apple], ['agodo']]
        for i in range(len(words_lst)):
            words_lst[i] = list(words_lst[i])
        return words_lst


def find_words_in_matrix(word_list, matrix, directions):
    """
    This is the main function.
    This function search each word within the word list the number of
    occurrences in the matrix, according to the directions string.
    :param word_list: A list of the word to search in the matrix
    :param matrix: The matrix to search upon
    :param directions: A string of directions which indicates in what directions
    the words should be searched
    :return: A list of all the occurrences of the words found in the matrix
    :rtype: list(tuple)
    """
    word_occurrences_dict = dict()
    for word in word_list:
        if RIGHT in directions:
            _find_r(matrix, word, word_occurrences_dict)

        if LEFT in directions:
            _find_l(matrix, word, word_occurrences_dict)

        if DOWN in directions:
            _find_d(matrix, word, word_occurrences_dict)

        if UP in directions:
            _find_u(matrix, word, word_occurrences_dict)

        if DOWN_RIGHT in directions:
            _find_down_right(matrix, word, word_occurrences_dict)

        if UP_RIGHT in directions:
            _find_up_right(matrix, word, word_occurrences_dict)

        if DOWN_LEFT in directions:
            _find_down_left(matrix, word, word_occurrences_dict)

        if UP_LEFT in directions:
            _find_up_left(matrix, word, word_occurrences_dict)

    word_score_lst = []
    for key in word_occurrences_dict:
        word_score_lst.append((key, word_occurrences_dict[key]))
    return word_score_lst


def write_output_file(results, output_filename):
    """
    Writes to a given path a list of word/count pairs in the format: "word,count"
    :param results: The pairs of the found results
    :type results: list(tuple)
    :param output_filename: The path and name of the output file
    :return: None
    """
    with open(output_filename, 'w') as file:
        for pair in results:
            file.write(f"{pair[0]},{pair[1]}\n")


def main():
    words = read_wordlist_file(sys.argv[1])
    mat = read_matrix_file((sys.argv[2]))
    key_values = find_words_in_matrix(words, mat, sys.argv[4])
    write_output_file(key_values, sys.argv[3])


if __name__ == '__main__':
    args_error_msg = check_input_args(sys.argv)
    if args_error_msg is None:
        main()

