import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

from modules.environment import *

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