import asyncio
from dotenv import load_dotenv
from os import getenv
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State

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
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != " ":
            return board[i][0]

        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != " ":
            return board[0][i]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]

    return 0

def check_board_full(board):
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True

def check_move_valid(board, row, col):
    if board[row][col] == " ":
        return True
    else:
        return False

load_dotenv()

XMPP_JID = getenv('XMPP_JID', 'test@localhost')
XMPP_PASSWORD = getenv('XMPP_PASSWORD', 'password')

# FSM State names
START, PLAYER1_TURN, PLAYER2_TURN, CHECK_WIN, END_GAME, EXIT = "START", "PLAYER1_TURN", "PLAYER2_TURN", "CHECK_WIN", "END_GAME", "EXIT"

class TicTacToeAgent(Agent):
    def __init__(self, jid, password, verify_security=False):
        super().__init__(jid, password, verify_security)
        self.board = new_board()   # Initialize the board

    async def setup(self):
        fsm = FSMBehaviour()
        fsm.add_state(name=START, state=StartState(self), initial=True)
        fsm.add_state(name=PLAYER1_TURN, state=Player1TurnState(self))
        fsm.add_state(name=PLAYER2_TURN, state=Player2TurnState(self))
        fsm.add_state(name=CHECK_WIN, state=CheckWinState(self))
        fsm.add_state(name=END_GAME, state=EndGameState(self))
        fsm.add_state(name=EXIT, state=ExitState(self))

        fsm.add_transition(START, PLAYER1_TURN)
        fsm.add_transition(PLAYER1_TURN, CHECK_WIN)
        fsm.add_transition(PLAYER2_TURN, CHECK_WIN)
        fsm.add_transition(CHECK_WIN, PLAYER1_TURN)
        fsm.add_transition(CHECK_WIN, PLAYER2_TURN)
        fsm.add_transition(CHECK_WIN, END_GAME)
        fsm.add_transition(END_GAME, START)
        fsm.add_transition(END_GAME, EXIT)

        self.add_behaviour(fsm)

    def reset_board(self):
        self.board = new_board()

class StartState(State):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent

    async def run(self):
        print("Game started! Player X begins.")
        print_board(self.agent.board)
        self.set_next_state(PLAYER1_TURN)

class Player1TurnState(State):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent

    async def run(self):
        print("\nPlayer X's turn.")
        move = input("Enter your move (row, column): ")
        row, col = map(int, move.split(","))
        row -= 1
        col -= 1
        valid_move = check_move_valid(self.agent.board, row, col)
        while valid_move == False:
            print("Invalid move, try again")
            move = input("Enter your move (row, column): ")
            row, col = map(int, move.split(","))
            row -= 1
            col -= 1
            valid_move = check_move_valid(self.agent.board, row, col)
        self.agent.board[row][col] = "X"
        self.set_next_state(CHECK_WIN)

class Player2TurnState(State):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent

    async def run(self):
        print("\nPlayer O's turn.")
        move = input("Enter your move (row, column): ")
        row, col = map(int, move.split(","))
        row -= 1
        col -= 1
        valid_move = check_move_valid(self.agent.board, row, col)
        while valid_move == False:
            print("Invalid move, try again")
            move = input("Enter your move (row, column): ")
            row, col = map(int, move.split(","))
            row -= 1
            col -= 1
            valid_move = check_move_valid(self.agent.board, row, col)
        self.agent.board[row][col] = "O"
        self.set_next_state(CHECK_WIN)

class CheckWinState(State):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent

    async def run(self):
        print_board(self.agent.board)
        line = check_winning(self.agent.board)
        if line in ["X", "O"]:
            print(f"\nPlayer {line} wins!")
            self.set_next_state(END_GAME)
        elif check_board_full(self.agent.board):
            print("\nIt's a tie!")
            self.set_next_state(END_GAME)
        else:
            if check_turn(self.agent.board) == "X":
                self.set_next_state(PLAYER1_TURN)
            else:
                self.set_next_state(PLAYER2_TURN)

class EndGameState(State):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent

    async def run(self):
        choice = input("\nWould you like to play again? (y/n): ").lower()
        while choice not in ["y", "n"]:
            print("Invalid choice, try again")
            choice = input("Would you like to play again? (y/n): ").lower()
        if choice == 'y':
            print("Starting a new game.")
            self.agent.reset_board()  # Reset the board in the agent
            self.set_next_state(START)
        elif choice == 'n':
            print("Exiting game.\n")
            if self.agent is not None:
                await self.agent.stop()
            self.set_next_state(EXIT)

class ExitState(State):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent

    async def run(self):
        await self.agent.stop()

# Main execution
async def main():
    tic_tac_toe_agent = TicTacToeAgent(XMPP_JID, XMPP_PASSWORD)
    await tic_tac_toe_agent.start()

    try:
        while tic_tac_toe_agent.is_alive():
            await asyncio.sleep(1)  # Sleep for a while before checking again
    except KeyboardInterrupt:
        await tic_tac_toe_agent.stop()
    print("Agent stopped")

if __name__ == "__main__":
    asyncio.run(main())
