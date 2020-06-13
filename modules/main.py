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