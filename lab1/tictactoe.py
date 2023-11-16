import asyncio
import os
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from dotenv import load_dotenv

load_dotenv()

XMPP_JID = os.getenv('XMPP_JID', 'test@localhost')
XMPP_PASSWORD = os.getenv('XMPP_PASSWORD', 'password')

# FSM State names
START, PLAYER1_TURN, PLAYER2_TURN, CHECK_WIN, END_GAME, EXIT = "START", "PLAYER1_TURN", "PLAYER2_TURN", "CHECK_WIN", "END_GAME", "EXIT"

class TicTacToeAgent(Agent):
    def __init__(self, jid, password, verify_security=False):
        super().__init__(jid, password, verify_security)
        self.board = [" " for _ in range(9)]  # 3x3 tic-tac-toe board
        self.current_player = "X"  # Player X always starts

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
        fsm.add_transition(CHECK_WIN, END_GAME)     # Will be chosen in CHECK_WIN if game over
        fsm.add_transition(END_GAME, EXIT)

        self.add_behaviour(fsm)

class StartState(State):
    async def run(self):
        print("Game started! Player X begins.")
        self.set_next_state(PLAYER1_TURN)

class Player1TurnState(State):
    async def run(self):
        print("Player X's turn.")
        # Implement Player 1's turn logic here
        # Update self.agent.board and current_player
        self.set_next_state(CHECK_WIN)

class Player2TurnState(State):
    async def run(self):
        print("Player O's turn.")
        # Implement Player 2's turn logic here
        # Update self.agent.board and current_player
        self.set_next_state(CHECK_WIN)

class CheckWinState(State):
    async def run(self):
        print("Checking if game is over...")
        # Implement logic to check if a player has won or if it's a tie
        # Determine the next state based on the game status
        pass

class EndGameState(State):
    async def run(self):
        print("Game Over.")
        # Display the result and clean up
        self.set_next_state(EXIT)

class ExitState(State):
    async def run(self):
        print("Exiting game.")
        if self.agent is not None:
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
