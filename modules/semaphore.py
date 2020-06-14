import sys

import time

import threading
import random

from phidias.Types  import *
from phidias.Main import *
from phidias.Lib import *
from phidias.Agent import *

from modules.environment import *
from modules.roadpoint import RoadPoint

class Semaphore(RoadPoint):
    def main(self):
        # Change state
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
            show_line("[", self.name(), "] Turning on to: green"),
            -red(SEMID),
            -yellow(SEMID),
            +green(SEMID)
        ]

        +SWITCH_SEMSTATE()[{'from': SENDER}] >> [
            show_line("[", self.name(), "] Updating semaphore state (sender: ", SENDER, ")"),
            next_state(self.name())
        ]

        # # Update loop 
        # +UPDATE()[{'from': SENDER}] >> [
        #     show_line("[", self.name(), "] Running update tick (sender: ", SENDER, ")"),
        #     move_cars(),
        # ]

        move_cars() / (red(SEMID)) >> [
            # This should not do anything
        ]

        super().main()
