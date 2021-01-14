import ex8_helper as nonogram_helper
from collections import Counter

BLACK = 1
WHITE = 0
TBD = -1


def get_row_variations(row, block):
    # BAD BASE CASE: sum of all blocks is greater than the number length of row
    if (sum(block) + len(block) - 1) > len(row):
        return []

    # BAD BASE CASE: total block size is greater than possible TBD blocks
    if sum(block) > row.count(TBD) + row.count(BLACK):
        return []

    return get_row_variations_helper(row[:], block[:], block, row[:], [], [])


def get_row_variations_helper(sub_row, block, sub_block, variation, variation_list,
                              head_of_variation):
    # GOOD BASE CASE: the out_row has all the black blocks filled
    if variation.count(BLACK) == sum(block):
        # replace all TBD to WHITE since all the blacks are filled
        _replace_item_in_list(variation, TBD, WHITE)
        variation_list.append(variation)
        return variation_list

    # get rid of starting whites:
    whites, sub_row = _cut_first_white_blocks(sub_row)
    head_of_variation += whites

    # the first item is BLACK:
    if sub_row[0] == BLACK:
        if _first_black_fill(sub_row, sub_block):
            # reconsturct the variation
            variation = head_of_variation + sub_row
            # get rid of the black blocks
            blacks, sub_row = _cut_first_black_blocks(sub_row)
            head_of_variation += blacks
            # call recursivly on the sub row
            get_row_variations_helper(sub_row[:], block, sub_block[1:], variation[:],
                                      variation_list,
                                      head_of_variation[:])

    # the first item is TBD:
    elif sub_row[0] == TBD:
        # get copies of the variables
        sub_row_copy = sub_row[:]
        variation_copy = variation[:]

        # try put a BLACK in the beginning
        sub_row_copy[0] = BLACK
        # check if this assignment is possible
        if _first_black_fill(sub_row_copy, sub_block):
            # reconsturct the variation
            variation_copy = head_of_variation + sub_row_copy
            # get rid of the black blocks
            blacks, sub_row_copy = _cut_first_black_blocks(sub_row_copy)
            head_of_variation += blacks
            # call recursivly on the sub row
            get_row_variations_helper(sub_row_copy[:], block, sub_block[1:], variation_copy[:],
                                      variation_list,
                                      head_of_variation[:])

        sub_row_copy = sub_row[:]
        variation_copy = variation[:]
        if BLACK in head_of_variation and head_of_variation[-1] == BLACK:
            head_of_variation = head_of_variation[:-len(blacks)]

        sub_row_copy[0] = WHITE
        variation_copy[variation_copy.index(TBD)] = WHITE
        if variation_copy.count(TBD) + variation_copy.count(BLACK) < sum(block):
            return variation_list
        get_row_variations_helper(sub_row_copy, block, sub_block, variation_copy, variation_list,
                                  head_of_variation[:])

    return variation_list


def _first_black_fill(row, block):
    """
    given first block BLACK - fill all the rest if possible
    if possible - return True. otherwise - False
    :param row:
    :param block:
    :return:
    """
    # the block is greater than the whole row
    if block[0] > len(row):
        return False

    # the block is exactly as row
    elif block[0] == len(row):
        # check that the row doesn't have whites.
        if all(row):
            # fill the whole row with blacks, starting with the first TBD
            for j in range(len(row)):
                row[j] = BLACK
            return True

        # the row has a white - since it's as the same size as the block - no filling is possible
        else:
            return False

    # from here - the block is smaller than the row:

    # check that it's possible to put a white at the end to finnish the block
    if row.count(TBD) == 0:
        return True

    if row[block[0]] != BLACK:
        # since WHITE is 0, then "all" function return true when all the items in the list are BLACK or TBD
        if all(row[1:block[0]]) and block[0] > 1:
            # fill all the first indexes in BLACK, starting at the first TBD
            for j in range(row.index(TBD), block[0]):
                row[j] = BLACK

        # put the white at the end
        row[block[0]] = WHITE
        return True

    else:
        return False


def _cut_first_white_blocks(row):
    if BLACK in row and TBD in row:
        whites = min(row.index(BLACK), row.index(TBD))
    elif BLACK in row:
        whites = row.index(BLACK)
    elif TBD in row:
        whites = row.index(TBD)
    else:
        whites = len(row)
    return [WHITE] * whites, row[whites:]


def _cut_first_black_blocks(row):
    if WHITE in row and TBD in row:
        blacks = min(row.index(WHITE), row.index(TBD))
    elif WHITE in row:
        blacks = row.index(WHITE)
    elif TBD in row:
        blacks = row.index(TBD)
    else:
        blacks = len(row)
    return [BLACK] * blacks, row[blacks:]


def _replace_item_in_list(lst, to_be_replaced, replace_to):
    """
    replace method like on string
    :param lst: the mutable list
    :param to_be_replaced: the item that you want to replace
    :param replace_to: the item that will be instead
    """
    for i, item in enumerate(lst):
        if item == to_be_replaced:
            lst[i] = replace_to


def get_intersection_row(rows):
    intersection = []
    for i in range(len(rows[0])):
        if check_rows(rows, intersection, i):
            intersection.append(1 if rows[0][i] == 1 else 0)
    return intersection


def check_rows(rows, intersection, i):
    for j in range(len(rows) - 1):
        if rows[j][i] != rows[j + 1][i]:
            intersection.append(-1)
            return False
    return True


def fill_row_with_whites(board_row):
    for i in range(len(board_row)):
        board_row[i] = WHITE


def fill_whole_row(board_row, row_constraint):
    pass


def fill_common_indexes(common_indexes, board_row):
    for index in common_indexes:
        board_row[index] = BLACK


def conclude_from_constraints(board, constraints):
    row_constraints = constraints[0]
    column_constraints = constraints[1]

    last_index_of_row = len(board[0]) - 1

    for row_index, board_row in enumerate(board):
        row_constraint = row_constraints[row_index]
        if not row_constraint:  # if constraint is [] then the whole row is white
            fill_row_with_whites(board_row)
        elif (sum(row_constraint) + len(row_constraint) - 1) == len(board_row):
            fill_whole_row(board_row, row_constraint)
        else:
            for block_index, block in enumerate(row_constraint):
                forward_indexes = []

                # get suspected indexes to be colored forward
                if block_index == 0:
                    forward_indexes += [x for x in range(block)]
                else:
                    slice_start_to_index = row_constraint[1:block_index]
                    # calculates where the index should start
                    start_index = row_constraint[0] + sum(slice_start_to_index) + \
                                  len(slice_start_to_index) + 1
                    forward_indexes += [x for x in range(start_index, start_index + block)]

                # get common indexes backwards
                common_indexes = []
                if block_index == len(row_constraint) - 1:
                    range_backwards = range(last_index_of_row, last_index_of_row - block, -1)
                    common_indexes += [x for x in range_backwards if x in forward_indexes]
                else:
                    slice_end_to_index = row_constraint[block_index + 1:-1]
                    # calculates where the index should start
                    start_index = last_index_of_row - row_constraint[-1] - \
                                  sum(slice_end_to_index) - len(slice_end_to_index) - 1
                    common_indexes += [x for x in range(start_index, start_index - block, -1)
                                       if x in forward_indexes]

                fill_common_indexes(common_indexes, board_row)



# block = [4]
# print(_first_black_fill(a, block))
# print("a is ", a)
#
# a = [1, -1, -1, -1]
# block = [3]
# print(_first_black_fill(a, block))
# print("a is ", a)
#
# a = [1]
# print(_first_black_fill(a, block))
# print("a is ", a)
#
# a = [1, -1, -1, -1, -1, 0, 1, -1]
# block = [3]
# print(_first_black_fill(a, block))
# print("a is ", a)

# row = [0, 0, -1, -1, -1, -1, -1, 0, 1, -1, 0, -1]
# block = [2, 2, 1]
# print(get_row_variations(row, block))
# #
# row = [-1, -1, -1]
# block = [1]
# print(get_row_variations(row, block))
#
# row = [1, 1, -1, 0]
# block = [3]
# print(get_row_variations(row, block))
#
# row = [-1, 0, 1, 0, -1, 0]
# block = [1, 1]
# print(get_row_variations(row, block))
#
# row = [0, 0, 0]
# block = [1]
# print(get_row_variations(row, block))
#
# row = [0, 0, -1, 1, 0]
# block = [2]
# print(get_row_variations(row, block))
#
# row = [0, 0, 1, 1, 0]
# block = [2]
# print(get_row_variations(row, block))

# rows = [[0, 1, 0], [0, 1, 1], [0, 1, -1], [1, 1, 0], [-1, -1, -1]]
# print(get_intersection_row(rows))

# board = [[-1] * 12]
# constraints = [[[2, 1, 2, 3]], []]
# conclude_from_constraints(board, constraints)

board = [[-1] * 12]
constraints = [[[]], []]
conclude_from_constraints(board, constraints)