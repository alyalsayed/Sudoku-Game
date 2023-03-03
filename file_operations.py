import time
from sudoku import *


def save_sudoku(puzzle, filename='sudoku_game.txt'):
    try:
        with open(filename, 'w') as f:
            f.write(
                ' --------- --------- ---------  --------- --------- ---------  --------- --------- ---------\n')
            for i in range(0, 81, 9):
                f.write(
                    '|         |         |         ||         |         |         ||         |         |         |\n')
                f.write(
                    '|         |         |         ||         |         |         ||         |         |         |\n')
                f.write('|    {}    |    {}    |    {}    ||    {}    |    {}    |    {}    ||    {}    |    {}    |    {}    |\n'.format(
                    puzzle[i], puzzle[i+1], puzzle[i+2], puzzle[i+3], puzzle[i+4], puzzle[i+5], puzzle[i+6], puzzle[i+7], puzzle[i+8]))
                f.write(
                    '|         |         |         ||         |         |         ||         |         |         |\n')
                f.write(
                    '|         |         |         ||         |         |         ||         |         |         |\n')
                f.write(
                    ' --------- --------- ---------  --------- --------- ---------  --------- --------- ---------\n')
                if i == 18 or i == 45:
                    f.write(
                        ' --------- --------- ---------  --------- --------- ---------  --------- --------- ---------\n')
        print("done saving")
    except IOError:
        print('Error: File could not be saved')
    except:
        print('Error: Something went wrong')
        # print directory for user
    print('Sudoku saved to: {}'.format(
        __file__.replace("file_operations.py", filename)))


# write a function to read sudoku_game.txt and return 2d list of only digits
def read_file(filename):
    try:
        with open(filename, 'r') as f:
            puzzle = []
            for line in f:
                row = []
                for char in line:
                    if char.isdigit():
                        row.append(int(char))
                puzzle.append(row)
            # remove [] from list
            puzzle = [x for x in puzzle if x != []]
        return puzzle
    except IOError:
        print('Error: File could not be read')
    except:
        print('Error: Something went wrong')
        # print directory for user
    print('Sudoku read from: {}'.format(
        __file__.replace("file_operations.py", f.name)))


def convert_to_string(ans):
    ans = str(ans)
    ans = ans.replace("[", "")
    ans = ans.replace("]", "")
    ans = ans.replace(",", "")
    ans = ans.replace(" ", "")
    return ans


if __name__ == '__main__':
   
    # get the diffculty level from the user
    while True:
        try:
            level = input(
                "Enter the difficulty level ex (easy, medium, hard,extreme): ")
            assert level == "easy" or level == "medium" or level == "hard" or level == "extreme"
            break
        except AssertionError:
            print("Invalid input,try again")

    puzzle = create_board(level)  # string
    save_sudoku(puzzle)
    starting = input("enter any key to start the puzzle ")
    print("starting in 3 seconds")
    time.sleep(1)
    print("starting in 2 seconds")
    time.sleep(1)
    print("starting in 1 seconds")
    time.sleep(1)
    print("starting now")
    start_time = time.time()
    finish = input("enter a key to finish the puzzle ")
    end_time = time.time()
    time_taken = end_time - start_time
    print("time taken to solve the puzzle is: ", round(time_taken), " seconds")
    solution = solve(puzzle)
    answer = convert_to_string(read_file("sudoku_game.txt"))
    print(answer)
    if (check_solution(answer)):
        print("You solved it!")
    else:
        print("You failed!")

    while True:
        try:
            question = input(
                "Do you want the solution to be displayed? (y/n): ")
            assert question == "y" or question == "n"
            break
        except AssertionError:
            print("Invalid input,try again")

    if question == "y":

        # print(solution)
        display(solution)
        # save solution to file solution.txt
        solution_str = ''.join([*solution.values()])
        save_sudoku(solution_str, filename='solution.txt')

    else:
        print("Good luck! with next puzzles")
   
