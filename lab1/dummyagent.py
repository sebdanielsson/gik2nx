import asyncio
import os
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from dotenv import load_dotenv

load_dotenv()

XMPP_JID = os.getenv('XMPP_JID', 'test@localhost')
XMPP_PASSWORD = os.getenv('XMPP_PASSWORD', 'password')

class DummyAgent(Agent):
    class MyBehav(CyclicBehaviour):
        async def on_start(self):
            print("Starting behaviour . . .")
            self.counter = 0

        async def run(self):
            print("Counter: {}".format(self.counter))
            self.counter += 1
            if self.counter > 3:
                self.kill(exit_code=10)
                return
            await asyncio.sleep(1)

        async def on_end(self):
            print("Behaviour finished with exit code {}.".format(self.exit_code))

    async def setup(self):
        print("Agent starting . . .")
        self.my_behav = self.MyBehav()
        self.add_behaviour(self.my_behav)

async def main():
    dummy = DummyAgent(XMPP_JID, XMPP_PASSWORD)
    await dummy.start()

    # wait until user interrupts with ctrl+C
    while not dummy.my_behav.is_killed():
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            break

    assert dummy.my_behav.exit_code == 10

    await dummy.stop()


if __name__ == "__main__":
        spade.run(main())
