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
    def on_start(self, semaphore_ids, tick_frequency, state_change_ticks):
        self.semaphore_ids = semaphore_ids.value
        self.tick_frequency = tick_frequency.value
        self.state_change_ticks = state_change_ticks.value

        # Set initial semaphore state
        for semid in self.semaphore_ids:
            self.assert_belief(SWITCH_SEMSTATE(semid)) 

        self.current_state_ticks = 0

        # Start the update's loop
        self.running = True

    def on_stop(self):
        # Stop the update's loop 
        self.running = False

    def sense(self):
        while self.running:
            # Tick sleep
            time.sleep(self.tick_frequency)

            self.current_state_ticks += 1
            if self.current_state_ticks == self.state_change_ticks:
                for semid in self.semaphore_ids:
                    self.assert_belief(SWITCH_SEMSTATE(semid))

                self.current_state_ticks = 0
            else:
                for semid in self.semaphore_ids:
                    self.assert_belief(UPDATE(semid))