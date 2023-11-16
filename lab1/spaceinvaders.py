import asyncio
import os
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from dotenv import load_dotenv

load_dotenv()

XMPP_JID = os.getenv('XMPP_JID', 'test@localhost')
XMPP_PASSWORD = os.getenv('XMPP_PASSWORD', 'password')

# State names
START, TRAVEL, MINING, ENCOUNTER, RETURN, END = "START", "TRAVEL", "MINING", "ENCOUNTER", "RETURN", "END"

class GalacticMinerAgent(Agent):
    async def setup(self):
        fsm = FSMBehaviour()
        fsm.add_state(name=START, state=StartState(), initial=True)
        fsm.add_state(name=TRAVEL, state=TravelState())
        fsm.add_state(name=MINING, state=MiningState())
        fsm.add_state(name=ENCOUNTER, state=EncounterState())
        fsm.add_state(name=RETURN, state=ReturnState())
        fsm.add_state(name=END, state=EndState())

        fsm.add_transition(source=START, dest=TRAVEL)
        fsm.add_transition(source=TRAVEL, dest=MINING)
        fsm.add_transition(source=MINING, dest=ENCOUNTER)
        fsm.add_transition(source=ENCOUNTER, dest=RETURN)
        fsm.add_transition(source=RETURN, dest=END)

        self.add_behaviour(fsm)

class StartState(State):
    async def run(self):
        print("Game Starting... Preparing your space journey!")
        self.set_next_state(TRAVEL)

class TravelState(State):
    async def run(self):
        print("Traveling to a new planet...")
        # Add logic for traveling
        self.set_next_state(MINING)

class MiningState(State):
    async def run(self):
        print("Mining resources...")
        # Add mining logic
        self.set_next_state(ENCOUNTER)

class EncounterState(State):
    async def run(self):
        print("Oh no, an encounter with space hazards!")
        # Add encounter logic
        self.set_next_state(RETURN)

class ReturnState(State):
    async def run(self):
        print("Returning to home planet with resources.")
        # Add return logic
        self.set_next_state(END)

class EndState(State):
    async def run(self):
        print("Game Over. Thank you for playing Galactic Miner!")
        if self.agent is not None:
            await self.agent.stop()

# Main execution
async def main():
    galactic_miner = GalacticMinerAgent(XMPP_JID, XMPP_PASSWORD)
    await galactic_miner.start()
    # Here you can add more logic if needed after the agent starts

if __name__ == "__main__":
    asyncio.run(main())
