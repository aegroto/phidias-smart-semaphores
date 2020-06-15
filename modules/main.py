import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

from modules.state_updater import *

from modules.environment import *
from modules.car_spawner import *

# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):
        # Debug procedures
        # populate()['all'] >> [
        #     show_line("Populating the road..."),
        #     +INCOMING_CAR(0)[{'to': 'Sem1'}]
        # ]

        # cars_at(SEMID)['all'] / car(C, SEMID) >> [
        #     show_line(C),
        # ]

        # Simulation procedures
        simulate() >> [
            show_line("Starting simulation..."),
            +active(),
            RoadStateUpdater(["A", "B"], ["Sem1", "Sem2"], 1.0, 10).start,
            CarSpawner(0.1, 0.1, "A").start
        ]

        stop() >> [
            show_line("Stopping simulation..."),
            -active()
        ]

        +SWITCH_SEMSTATE(SEMID) / (active() & eq(SEMID, SEMID)) >> [
            # show_line("[", self.name(), "] Communicating semaphore ", SEMID, " to switch its state"),
            +SWITCH_SEMSTATE(SEMID)[{'to': SEMID}]
        ]

        +UPDATE(SEMID) / (active() & eq(SEMID, SEMID)) >> [
            # show_line("[", self.name(), "] Communicating semaphore ", SEMID, " to update its state"),
            +UPDATE(SEMID)[{'to': SEMID}],
        ]

        +SPAWN_CAR(C, L) / active() >> [
            show_line("[", self.name(), "] Spawning car ", C, " at location ", L),
            +INCOMING_CAR(C)[{'to': L}],
        ]