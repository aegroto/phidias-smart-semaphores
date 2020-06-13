import sys

import time

import threading
import random

from enum import Enum

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

class Car(Belief): pass

class red(Belief): pass
class yellow(Belief): pass
class green(Belief): pass

class active(SingletonBelief): pass

class UPDATE_SEMSTATE(Reactor): pass

class next_state(Procedure): pass

class stop(Procedure): pass
class simulate(Procedure): pass

def_vars("SENDER", "SEMID", "CURRENT_STATE", "Sem1", "Sem2")

class SemaphoresStateUpdater(Sensor):
    TICK_FREQUENCY = 0.1 # 100 ms 

    STATE_CHANGE_TICKS = 10 # 100 ms * 10 -> state changes every second (red/yellow/green)

    def on_start(self, semaphore_ids):
        self.semaphore_ids = semaphore_ids.value

        # Set initial semaphore state
        for semid in self.semaphore_ids:
            self.assert_belief(UPDATE_SEMSTATE(semid)) 

        self.current_state_ticks = 0

        # Start the update's loop
        self.running = True

    def on_stop(self):
        # Stop the update's loop 
        self.running = False

    def sense(self):
        while self.running:
            # Tick sleep
            time.sleep(SemaphoresStateUpdater.TICK_FREQUENCY)

            self.current_state_ticks += 1
            if self.current_state_ticks == SemaphoresStateUpdater.STATE_CHANGE_TICKS:
                for semid in self.semaphore_ids:
                    # print("Updating semaphore {}'s  state...".format(semid))

                    self.assert_belief(UPDATE_SEMSTATE(semid))

                self.current_state_ticks = 0

                # print("State updated")

class semaphore(Agent):
    def main(self):
        +UPDATE_SEMSTATE()[{'from': SENDER}] >> [
            show_line("[", self.name(), "] Updating semaphore state (sender: ", SENDER, ")"),
            next_state(self.name())
        ]

        next_state(SEMID) / (red(SEMID)) >> [
            show_line("[", self.name(), "] Next state is green"),
            -red(SEMID),
            +green(SEMID)
        ]

        next_state(SEMID) / (green(SEMID)) >> [
            show_line("[", self.name(), "] Next state is yellow"),
            -green(SEMID),
            +yellow(SEMID)
        ]

        next_state(SEMID) / (yellow(SEMID)) >> [
            show_line("[", self.name(), "] Next state is red"),
            -yellow(SEMID),
            +red(SEMID)
        ]

        next_state(SEMID) >> [
            show_line("[", self.name(), "] Turning on to: red"),
            +red(SEMID)
        ]

        pass

# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):
        states_updater = SemaphoresStateUpdater(["Sem1", "Sem2"])

        simulate() >> [
            show_line("Starting simulation..."),
            +active(),
            states_updater.start
        ]

        stop() >> [
            show_line("Stopping simulation..."),
            -active()
        ]

        +UPDATE_SEMSTATE(SEMID) / active() >> [
            show_line("[", self.name(), "] Communicating semaphore ", SEMID, " to update its state"),
            +UPDATE_SEMSTATE()[{'to': SEMID}]
        ]

# start the actors
semaphore("Sem1").start()
semaphore("Sem2").start()
main().start()

# run the engine shell
PHIDIAS.shell(globals())