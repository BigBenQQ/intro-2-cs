import ex8_helper as nonogram_helper

BLACK = 1
WHITE = 0
TBD = -1


def get_row_variations(row, block):
    # BAD BASE CASE: sum of all blocks is greater than the number length of row
    if (sum(block) + len(block) - 1) > len(row):
        return []

    return get_row_variations_helper(row, block, row[:], [], row[:], block[:])


def get_row_variations_helper(row, block, temp_row: list, variation_list: list, variation, sub_block):
    # GOOD BASE CASE: the out_row has all the black blocks filled
    if variation.count(BLACK) == sum(block):
        # replace all TBD to WHITE since all the blacks are filled
        _replace_item_in_list(variation, TBD, WHITE)
        variation_list.append(variation)
        return

    # gets the number of whites that has been cut off, and the new list starting with BLACK or TBD
    # num_of_blacks, sub_temp = _cut_first_black_blocks(temp_row)
    # sub_block[0] -= num_of_blacks
    num_of_whites, sub_temp = _cut_first_white_blocks(temp_row)

    if sub_temp[0] == BLACK:
        if _first_black_fill(sub_temp, sub_block) is not None:
            return sub_temp
        variation = sub_temp
        num_of_blacks, sub_temp = _cut_first_black_blocks(sub_temp)
        num_of_whites, sub_temp = _cut_first_white_blocks(sub_temp)
        get_row_variations_helper(row, block, sub_temp, variation_list, variation[:], block[1:])

    else:  # sub_temp[0] == TBD
        sub_temp_copy = sub_temp[:]
        variation_copy = variation[:]

        # try to put a black in the variation first place
        sub_temp_copy[0] = BLACK
        index_of_change = variation_copy.index(TBD)
        # fill the rest according to the block, if possible
        if _first_black_fill(sub_temp_copy, sub_block) is None:
            # fill the variation with black accordingly
            for i in range(index_of_change, index_of_change + sub_block[0]):
                variation_copy[i] = BLACK
            get_row_variations_helper(row, block, sub_temp_copy, variation_list, variation_copy[:], sub_block[1:])

        sub_temp_copy = sub_temp[:]
        variation_copy = variation[:]
        # try to put a white in the variation first place
        sub_temp_copy[0] = WHITE
        if sub_temp_copy.count(TBD) == 0 and sum(sub_block) != sub_temp_copy.count(BLACK):
            return variation_list
        variation_copy[index_of_change] = WHITE
        # if variation.count(TBD) == 0 and sum(block)
        get_row_variations_helper(row, block, sub_temp_copy, variation_list, variation_copy[:], sub_block)

    return variation_list


# TODO: maybe can be more efficient? start on the index of the TBD?
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


def _first_black_fill(row, block):
    """
    given a row that starts with white, and then black - fill all rest
    :param row:
    :param block:
    :param out_row:
    :return:
    """
    if block[0] > len(row):
        return False

    elif block[0] == len(row):
        if all(row):
            for j in range(row.index(TBD), len(row)):
                row[j] = BLACK
            # block[0] = 0
            return

        else:
            return False

    if block[0] == 1 and row[block[0]] != BLACK:
        row[block[0]] = WHITE
        return
        
    # since WHITE is 0, then "all" function return true when all the items in the list are BLACK or TBD
    # and also check if its possible to place a WHITE at the end
    if all(row[1:block[0]]) and row[block[0]] != BLACK:
        # fill all the first indexes in BLACK
        for j in range(row.index(TBD), block[0]):
            row[j] = BLACK
            # add a WHITE to a complete block
            if j == block[0] - 1:
                row[j + 1] = WHITE
        # since the first block is used, then zeroing it (mutable)
        # block[0] = 0

    else:
        return False


# TODO - this just clears the first white blocks, need to clear the whole complete block, including completed black
def _cut_first_white_blocks(row):
    if BLACK in row and TBD in row:
        whites = min(row.index(BLACK), row.index(TBD))
    elif BLACK in row:
        whites = row.index(BLACK)
    elif TBD in row:
        whites = row.index(TBD)
    else:
        whites = len(row)
    return whites, row[whites:]


def _cut_first_black_blocks(row):
    if WHITE in row and TBD in row:
        blacks = min(row.index(WHITE), row.index(TBD))
    elif WHITE in row:
        blacks = row.index(WHITE)
    elif TBD in row:
        blacks = row.index(TBD)
    else:
        blacks = len(row)
    return blacks, row[blacks:]


block = [3]
a = [1, 1, -1, 0]
print(get_row_variations(a, block))

block = [1]
a = [-1, -1, -1]
print(get_row_variations(a, block))

block = [3, 1]
a = [0, 0, 1, -1, -1, -1, 0, -1, -1]
print(get_row_variations(a, block))

block = [2]
a = [-1, -1, -1]
print(get_row_variations(a, block))
