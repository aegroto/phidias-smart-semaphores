import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

from modules.state_updater import SemaphoresStateUpdater

from modules.environment import *

# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):
        states_updater = SemaphoresStateUpdater(["Sem1", "Sem2"], 1.0, 10)

        # Debug procedures
        populate()['all'] >> [
            show_line("Populating the road..."),
            +INCOMING_CAR(0)[{'to': 'Sem1'}]
        ]

        cars_at(SEMID)['all'] / car(C, SEMID) >> [
            show_line(C)
        ]

        # Simulation procedures
        simulate() >> [
            show_line("Starting simulation..."),
            +active(),
            states_updater.start
        ]

        stop() >> [
            show_line("Stopping simulation..."),
            -active()
        ]

        +SWITCH_SEMSTATE(SEMID) / (active()) >> [
            show_line("[", self.name(), "] Communicating semaphore ", SEMID, " to switch its state"),
            +SWITCH_SEMSTATE()[{'to': SEMID}]
        ]

        +UPDATE(SEMID) / active() >> [
            show_line("[", self.name(), "] Communicating semaphore ", SEMID, " to update its state"),
            +UPDATE()[{'to': SEMID}],
        ]