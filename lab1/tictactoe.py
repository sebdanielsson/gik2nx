import asyncio
from calendar import c
import os
from tabnanny import check
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from dotenv import load_dotenv

def new_board():
    return [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "],
    ]

def print_board(board):
    for row in board:
        print("|", end="")
        for cell in row:
            print(cell, end="|")
        print()

def check_turn(board):
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == "X":
                x_count += 1
            elif cell == "O":
                o_count += 1
    if x_count == o_count:
        return "X"
    else:
        return "O"

def check_winning(board):
    line=0
    if board[0][0]==board[0][1] and board[0][1]==board[0][2] and board[0][0]!=0:
        line=board[0][0]
    if board[1][0]==board[1][1] and board[1][1]==board[1][2] and board[1][0]!=0:
        line=board[1][0]
    if board[2][0]==board[2][1] and board[2][1]==board[2][2] and board[2][0]!=0:
        line=board[2][0]
        
    if board[0][0]==board[1][0] and board[1][0]==board[2][0] and board[0][0]!=0:
        line=board[0][0]
    if board[0][1]==board[1][1] and board[1][1]==board[2][1] and board[0][1]!=0:
        line=board[0][1]
    if board[0][2]==board[1][2] and board[1][2]==board[2][2] and board[0][2]!=0:
        line=board[0][2]

    if board[0][0]==board[1][1] and board[1][1]==board[2][2] and board[0][0]!=0:
        line=board[0][0]
    if board[0][2]==board[1][1] and board[1][1]==board[2][0] and board[0][2]!=0:
        line=board[0][2]  
    return line

def check_board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_move_valid(board, row, col):
    if row < 0 or row > 2 or col < 0 or col > 2:
        return False
    elif board[row][col] != " ":
        return False
    else:
        return True

load_dotenv()

XMPP_JID = os.getenv('XMPP_JID', 'test@localhost')
XMPP_PASSWORD = os.getenv('XMPP_PASSWORD', 'password')

# FSM State names
START, PLAYER1_TURN, PLAYER2_TURN, CHECK_WIN, END_GAME, EXIT = "START", "PLAYER1_TURN", "PLAYER2_TURN", "CHECK_WIN", "END_GAME", "EXIT"

class TicTacToeAgent(Agent):
    def __init__(self, jid, password, verify_security=False):
        super().__init__(jid, password, verify_security)
        self.board = new_board()   # Initialize the board
        self.current_player = "X"  # Player X starts

    async def setup(self):
        fsm = FSMBehaviour()
        fsm.add_state(name=START, state=StartState(), initial=True)
        fsm.add_state(name=PLAYER1_TURN, state=Player1TurnState())
        fsm.add_state(name=PLAYER2_TURN, state=Player2TurnState())
        fsm.add_state(name=CHECK_WIN, state=CheckWinState())
        fsm.add_state(name=END_GAME, state=EndGameState())
        fsm.add_state(name=EXIT, state=ExitState())

        fsm.add_transition(START, PLAYER1_TURN)
        fsm.add_transition(PLAYER1_TURN, CHECK_WIN)
        fsm.add_transition(PLAYER2_TURN, CHECK_WIN)
        fsm.add_transition(CHECK_WIN, PLAYER1_TURN)  # Default transition
        fsm.add_transition(CHECK_WIN, PLAYER2_TURN)  # Will be chosen in CHECK_WIN if needed
        fsm.add_transition(CHECK_WIN, END_GAME)      # Will be chosen in CHECK_WIN if game over
        fsm.add_transition(END_GAME, EXIT)

        self.add_behaviour(fsm)

class StartState(State):
    async def run(self):
        print("Game started! Player X begins.\n")
        self.set_next_state(PLAYER1_TURN)

class Player1TurnState(State):
    async def run(self):
        board = self.agent.board
        print("Player X's turn.\n")
        print_board(board)
        move = input("Enter your move (row, column): ")
        row, col = map(int, move.split(","))
        valid_move = check_move_valid(board, row, col)
        while valid_move == False:
            print("Invalid move, try again")
            move = input("Enter your move (row, column): ")
            row, col = map(int, move.split(","))
            valid_move = check_move_valid(board, row, col)
        board[row][col] = "X"
        self.set_next_state(CHECK_WIN)

class Player2TurnState(State):
    async def run(self):
        board = self.agent.board
        print("Player O's turn.\n")
        print_board(board)
        move = input("Enter your move (row, column): ")
        row, col = map(int, move.split(","))
        valid_move = check_move_valid(board, row, col)
        while valid_move == False:
            print("Invalid move, try again")
            move = input("Enter your move (row, column): ")
            row, col = map(int, move.split(","))
            valid_move = check_move_valid(board, row, col)
        board[row][col] = "O"
        self.set_next_state(CHECK_WIN)

class CheckWinState(State):
    async def run(self):
        board = self.agent.board
        line = check_winning(board)
        if line == "X":
            print("Player X wins!")
            self.set_next_state(END_GAME)
        elif line == "O":
            print("Player O wins!")
            self.set_next_state(END_GAME)
        elif check_board_full(board):
            print("It's a tie!")
            self.set_next_state(END_GAME)
        else:
            # Game is not over, so change turn
            if check_turn(board) == "X":
                self.set_next_state(PLAYER1_TURN)
            else:
                self.set_next_state(PLAYER2_TURN)

class EndGameState(State):
    async def run(self):
        board = self.agent.board
        print_board(board)
        print("Game Over.\n")
        # Display the result and clean up
        self.set_next_state(EXIT)

class ExitState(State):
    async def run(self):
        print("Exiting game.\n")
        await self.agent.stop()

# Main execution
async def main():
    tic_tac_toe_agent = TicTacToeAgent(XMPP_JID, XMPP_PASSWORD)
    await tic_tac_toe_agent.start()
    # The agent is now started, and you can add further logic if needed

    try:
        while tic_tac_toe_agent.is_alive():
            await asyncio.sleep(1)  # Sleep for a while before checking again
    except KeyboardInterrupt:
        await tic_tac_toe_agent.stop()
    print("Agent stopped")

if __name__ == "__main__":
    asyncio.run(main())
