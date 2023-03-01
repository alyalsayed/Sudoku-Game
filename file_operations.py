from random import shuffle
import datetime
import sudoko


def print_file(board, file):
    """
    Print the given answer to the given file.
    :param answer: 2D list of numbers
    :param file: file to write to
    :return: None
    """

    for i in range(3):
        for j in range(3):
            file.write(" --------- ")

    for i in range(9):
        file.write(
            # " --------- "
            "\n"
            f"|         |" "          |""          |""|         |""          |""          |""|         |""          |""|         |"
            "\n"
            f"|         |" "          |""          |""|         |""          |""          |""|         |""          |""|         |"
            "\n"
            f"|    {board[i][0]}    |" f"    {board[i][1]}     |"f"    {board[i][2]}     |"
            f"|    {board[i][3]}    |"f"     {board[i][4]}    |"f"     {board[i][5]}    |"
            f"|    {board[i][6]}    |"f"     {board[i][7]}    |"f"|    {board[i][8]}    |"
            "\n"
            f"|         |" "          |""          |""|         |""          |""          |""|         |""          |""|         |"
            "\n"
            f"|         |" "          |""          |""|         |""          |""          |""|         |""          |""|         |"
            "\n"
            " --------- "" --------- "" --------- "" --------- "" --------- "" --------- "" --------- "" --------- "" --------- ")


def get_answer():
    file = open('puzzle.txt', 'r', encoding='utf-8', errors='ignore')

    lines = file.read().splitlines()
    board = []
    user_sol = []
    for line in lines:
        for i in line:
            if i.isdigit() == True:
                user_sol.append(i)

    counter = 0
    templst = []
    while counter < 81:

        if (len(templst) == 9):
            templst = []
        for i in range(9):
            templst.append(int(user_sol[counter]))
            counter += 1
        board.append(templst)
    # print(board)
    return board


def main():
    """
    Sudoku game.
    main functtion.
    creates board and take input from user to decide how the game should be
    :return: None
    """
    board = [[0 for col in range(9)] for row in range(9)]

    try:
        difficulty = input(
            '\nPlease choose a difficulty (easy, medium, hard, insane) or Enter quit to exit game: ').strip().lower()

        if difficulty == 'easy' or difficulty == 'e':
            difficulty = 4
        elif difficulty == 'medium' or difficulty == 'm':
            difficulty = 5
        elif difficulty == 'hard' or difficulty == 'h':
            difficulty = 6
        elif difficulty == 'insane' or difficulty == 'i':
            difficulty = 7
        elif difficulty == 'quit' or difficulty == 'q':
            print('\nThanks for Playing!\n')
            return
        else:
            print(
                "\nInvalid difficulty. Please re-enter difficulty or type 'quit' to quit.")
            main()
            return

    except (KeyboardInterrupt):
        exit()

    sudoko.generate_board(board)
    solution = [x[:] for x in board]  # to copy the created board
    # to make the puzzle dependening on the difficulty
    sudoko.remove_cells(board, difficulty)

    try:
        start = str(input("please enter anykey to start the game:  "))
        file = open('puzzle.txt', 'w', encoding='utf-8', errors='ignore')
        print_file(board, file)
        # print the path of the file
        file.close()
        current_time1 = datetime.datetime.now()
    except (KeyboardInterrupt):
        exit()

    try:
        answer = []
        c = True
        while c:
            done = input(
                "please enter done or d after solving the game:  ").lower()

            if done == "d" or done == "done":
                current_time2 = datetime.datetime.now()
                answer = get_answer()
                c = False

    except KeyboardInterrupt:
        exit()

    if sudoko.check_sudoku(answer) == True:
        print("well done!!")
    else:
        print("wrong answer ):")
        try:
            sol = input("do you want the answer?  (y/n): ")
            if sol == "y" or sol == "yes":
                file = open('test.txt', 'w', encoding='utf-8', errors='ignore')
                print_file(solution, file)
                # print the path of the file
            elif sol == "n" or sol == "no":
                print("thanks for playing the game")
            else:
                print("invalid input")
        except (KeyboardInterrupt):
            exit()

    print("\n")
    print(current_time2 - current_time1)
    print("\n")


if __name__ == '__main__':

    main()
