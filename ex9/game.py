import helper as helper
import car as c
import board as b
import sys




class Game:
    """
    Add class description here
    """
    ALL_LEGAL_COLORS = ["Y", "B", "O", "G", "W", "R"]
    ALL_LEGAL_MOVES = ["l", "u", "d", "r"]

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board
        print(board)

    def __single_turn(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. 

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what 
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional 
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        """
        pass

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while True:
            color_direction = input("type \"color,direction\": ")
            if color_direction == "!":
                exit()

            color, direction = color_direction.split(",")
            if color not in self.ALL_LEGAL_COLORS:
                print("Not in color list.")
                continue

            if direction not in self.ALL_LEGAL_MOVES:
                print("Not in move list.")
                continue

            if not board.move_car(color, direction):
                print("Illegal move")
                continue

            if board.cell_content(board.END_COORDINATE) is not None:
                return

            print(self.__board)




def generate_car_list(cars: dict):
    color_lst = [color for color in cars]
    data_lst = [data for data in cars.values()]
    car_lst = []
    for i in range(len(color_lst)):
        car_lst.append(c.Car(color_lst[i], data_lst[i][0],
                             tuple(data_lst[i][1]), data_lst[i][2]))
    return car_lst


def populate_board_with_cards(board: b.Board, car_lst: list):
    for car in car_lst:
        board.add_car(car)


if __name__ == "__main__":
    # Your code here
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.
    if len(sys.argv) == 2:
        cars = helper.load_json(sys.argv[1])
        car_lst = generate_car_list(cars)
        board = b.Board()
        populate_board_with_cards(board, car_lst)
        game_obj = Game(board)
        game_obj.play()
