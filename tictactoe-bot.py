import copy

board = [" " for x in range(9)]

def print_board():
    row1 = "| {} | {} | {} |".format(board[0], board[1], board[2])
    row2 = "| {} | {} | {} |".format(board[3], board[4], board[5])
    row3 = "| {} | {} | {} |".format(board[6], board[7], board[8])

    print()
    print(row1)
    print(row2)
    print(row3)
    print()

def player_move(icon):
    if icon == "X":
        number = 1
    elif icon == "O":
        number = 2
    print("Your turn player {}".format(number))
    choice = int(input("Enter your move (1-9): ").strip())
    if board[choice - 1] == " ":
        board[choice - 1] = icon
    else:
        print()
        print("That space is already taken!")

def bot_move(icon):
    print("Bot's turn")
    best_score = -1000
    for i in range(len(board)):
        if board[i] == " ":
            board[i] = icon
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    board[move] = icon

def minimax(board, depth, isMaximizing):
    result = check_win()
    if result != None:
        if result == "X":
            return -1
        elif result == "O":
            return 1
        else:
            return 0

    if isMaximizing:
        best_score = -1000
        for i in range(len(board)):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for i in range(len(board)):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

def check_win():
    win_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for combination in win_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]] and board[combination[0]] != " ":
            return board[combination[0]]
    if " " not in board:
        return "tie"
    return None

while True:
    print_board()
    player_move("X")
    print_board()
    result = check_win()
    if result != None:
        if result == "X":
            print("Player X wins! Congratulations!")
        elif result == "O":
            print("Bot wins! Better luck next time.")
        elif result == "tie":
            print("Tie game!")
        break
    bot_move("O")
    result = check_win()
    if result != None:
        if result == "X":
            print("Player X wins! Congratulations!")
        elif result == "O":
            print("Bot wins! Better luck next time.")
        elif result == "tie":
            print("Tie game!")
        break